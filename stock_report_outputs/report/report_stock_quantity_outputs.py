# -*- coding: utf-8 -*-

from odoo import fields, models, tools


class ReportStockQuantityOutputs(models.Model):
    _name = 'report.stock.quantity.outputs'
    _auto = False
    _description = 'Quantity Report Stock Outputs'

    date = fields.Date(string='Date', readonly=True)
    product_tmpl_id = fields.Many2one('product.template',
        related='product_id.product_tmpl_id')
    product_id = fields.Many2one('product.product',
        string='Product', readonly=True)
    state = fields.Selection([
         ('in', 'In'),
         ('out', 'Out'),
     ], string='State', readonly=True)
    product_qty = fields.Float(string='Quantity', readonly=True)
    move_ids = fields.One2many('stock.move', readonly=True)
    company_id = fields.Many2one('res.company', readonly=True)
    warehouse_id = fields.Many2one('stock.warehouse', readonly=True)
    location_id = fields.Many2one('stock.location', 'From', check_company=True,
        required=True)
    location_dest_id = fields.Many2one('stock.location', 'To',
        check_company=True, required=True)
    categ_id = fields.Many2one('product.category', 'Product Category',
        readonly=True)

    def init(self):
        tools.drop_view_if_exists(self._cr, 'report_stock_quantity_outputs')
        query = """
CREATE or REPLACE VIEW report_stock_quantity_outputs AS (
SELECT
    m.id,
    product_id,
    CASE
        WHEN (ls.usage = 'internal' OR ls.usage = 'transit' AND ls.company_id IS NOT NULL) AND ld.usage = 'customer' THEN 'out' -- v
        WHEN  ls.usage = 'customer' AND (ld.usage = 'internal' OR ld.usage = 'transit' AND ld.company_id IS NOT NULL) THEN 'in'  -- v
    END AS state,
    date_expected::date AS date,
    CASE
        WHEN (ls.usage = 'internal' OR ls.usage = 'transit' AND ls.company_id IS NOT NULL) AND ld.usage = 'customer' THEN product_qty
        WHEN  ls.usage = 'customer' AND (ld.usage = 'internal' OR ld.usage = 'transit' AND ld.company_id IS NOT NULL) THEN -product_qty
    END AS product_qty,
    m.company_id,
    CASE
        WHEN (ls.usage = 'internal' OR ls.usage = 'transit' AND ls.company_id IS NOT NULL) AND ld.usage = 'customer' THEN whs.id
        WHEN  ls.usage = 'customer' AND (ld.usage = 'internal' OR ld.usage = 'transit' AND ld.company_id IS NOT NULL) THEN whd.id
    END AS warehouse_id
    , m.location_id AS location_id
    , m.location_dest_id
    , pt.categ_id
FROM
    stock_move m
LEFT JOIN stock_location ls   ON (ls.id = m.location_id)
LEFT JOIN stock_location ld   ON (ld.id = m.location_dest_id)
LEFT JOIN stock_warehouse whs ON ls.parent_path like concat('%/', whs.view_location_id, '/%')
LEFT JOIN stock_warehouse whd ON ld.parent_path like concat('%/', whd.view_location_id, '/%')
LEFT JOIN product_product pp  ON pp.id = m.product_id
LEFT JOIN product_template pt ON pt.id = pp.product_tmpl_id
-- LEFT JOIN product_category pc ON pc.id = pt.categ_id

WHERE
    pt.type = 'product'
    AND product_qty != 0
    AND  ((ls.usage = 'internal' OR ls.usage = 'transit' AND ls.company_id IS NOT NULL) AND ld.usage = 'customer'
	    OR ls.usage = 'customer' AND (ld.usage = 'internal' OR ld.usage = 'transit' AND ld.company_id IS NOT NULL) )
    AND m.state IN ('done')
);
"""
        self.env.cr.execute(query)
