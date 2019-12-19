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

    uom_po_id = fields.Many2one('uom.uom', 'PO UoM', readonly=True)
    uom_po_qty = fields.Float(string='PO Quantity', readonly=True)
    reference = fields.Char(string='Reference', readonly=True)
    movement_type = fields.Selection([
                          ('rote' , 'Rote')
                        , ('prest', 'Préstamo')
                        , ('devol', 'Devolución')],
                        string='Movement type',
                        readonly=True
                        )

    def init(self):
        tools.drop_view_if_exists(self._cr, 'report_stock_quantity_outputs')
        query = """
CREATE or REPLACE VIEW report_stock_quantity_outputs
    AS (

SELECT
    m.id,
    product_id,
    CASE
        WHEN (ls.usage = 'internal' AND ls.company_id IS NOT NULL) AND ld.usage = 'customer'  THEN 'out' -- v
        WHEN  ls.usage = 'customer' AND (ld.usage = 'internal' AND ld.company_id IS NOT NULL) THEN 'in'  -- v
    END AS state,
    date_expected::date AS date,
    CASE
        WHEN (ls.usage = 'internal' AND ls.company_id IS NOT NULL) AND ld.usage = 'customer'  THEN  product_qty
        WHEN  ls.usage = 'customer' AND (ld.usage = 'internal' AND ld.company_id IS NOT NULL) THEN -product_qty
    END AS product_qty,
    m.company_id,
    CASE
        WHEN (ls.usage = 'internal' AND ls.company_id IS NOT NULL) AND ld.usage = 'customer'  THEN  whs.id
        WHEN  ls.usage = 'customer' AND (ld.usage = 'internal' AND ld.company_id IS NOT NULL) THEN  whd.id
    END AS warehouse_id

    , CASE
--        WHEN (ls.usage = 'internal' AND ls.company_id IS NOT NULL) AND ld.usage = 'customer'  THEN  (m.product_qty * product_uom.factor)::decimal(16,2)
        WHEN (ls.usage = 'internal' AND ls.company_id IS NOT NULL) AND ld.usage = 'customer'  THEN  ROUND((m.product_qty * product_uom.factor)::decimal(16,1))
        WHEN  ls.usage = 'customer' AND (ld.usage = 'internal' AND ld.company_id IS NOT NULL) THEN -ROUND((m.product_qty * product_uom.factor)::decimal(16,1))
    END AS uom_po_qty
    , pt.uom_po_id

    , m.location_id
    , m.location_dest_id
    , m.reference
    , pt.categ_id
    , '' AS movement_type

FROM      stock_move m
LEFT JOIN stock_location   ls  ON (ls.id = m.location_id)
LEFT JOIN stock_location   ld  ON (ld.id = m.location_dest_id)
LEFT JOIN stock_warehouse  whs ON ls.parent_path like concat('%/', whs.view_location_id, '/%')
LEFT JOIN stock_warehouse  whd ON ld.parent_path like concat('%/', whd.view_location_id, '/%')
LEFT JOIN product_product  pp  ON pp.id = m.product_id
LEFT JOIN product_template pt  ON pt.id = pp.product_tmpl_id
LEFT JOIN uom_uom product_uom  ON product_uom.id = pt.uom_po_id

WHERE
    pt.type = 'product'
    AND product_qty != 0
    AND  (((ls.usage = 'internal' AND ls.company_id IS NOT NULL) AND ld.usage = 'customer')
 	    OR
 	    (ls.usage = 'customer' AND (ld.usage = 'internal' AND ld.company_id IS NOT NULL)) )
    AND m.state = 'done'

        UNION

SELECT
    m.id,
    product_id,
    CASE
        WHEN (ls.usage = 'transit' AND ls.company_id IS NOT NULL) AND ld.usage = 'internal'  THEN 'in'
        WHEN  ls.usage = 'internal' AND (ld.usage = 'transit' AND ld.company_id IS NOT NULL) THEN 'out'
    END AS state,
    date_expected::date AS date,
    CASE
	WHEN  ls.usage = 'internal' AND (ld.usage = 'transit' AND ld.company_id IS NOT NULL) THEN 0
        WHEN (ls.usage = 'transit'  AND ls.company_id IS NOT NULL) AND ld.usage = 'internal' AND movement_type = 'rote'  THEN 0
        WHEN (ls.usage = 'transit'  AND ls.company_id IS NOT NULL) AND ld.usage = 'internal' AND movement_type = 'prest' THEN product_qty
        WHEN (ls.usage = 'transit'  AND ls.company_id IS NOT NULL) AND ld.usage = 'internal' AND movement_type = 'devol' THEN product_qty
        ELSE 0
    END AS product_qty,
    m.company_id,

    CASE
	WHEN  ls.usage = 'internal' AND (ld.usage = 'transit' AND ld.company_id IS NOT NULL) THEN whs.id
        WHEN (ls.usage = 'transit'  AND ls.company_id IS NOT NULL) AND ld.usage = 'internal' AND movement_type = 'rote'  THEN whd.id
        WHEN (ls.usage = 'transit'  AND ls.company_id IS NOT NULL) AND ld.usage = 'internal' AND movement_type = 'prest' THEN whd.id
        WHEN (ls.usage = 'transit'  AND ls.company_id IS NOT NULL) AND ld.usage = 'internal' AND movement_type = 'devol' THEN whd.id
    END AS warehouse_id ,

    CASE
	WHEN  ls.usage = 'internal' AND (ld.usage = 'transit' AND ld.company_id IS NOT NULL) THEN 0
        WHEN (ls.usage = 'transit'  AND ls.company_id IS NOT NULL) AND ld.usage = 'internal' AND movement_type = 'rote'  THEN 0
        WHEN (ls.usage = 'transit'  AND ls.company_id IS NOT NULL) AND ld.usage = 'internal' AND movement_type = 'prest' THEN ROUND((m.product_qty * product_uom.factor)::decimal(16,1))
        WHEN (ls.usage = 'transit'  AND ls.company_id IS NOT NULL) AND ld.usage = 'internal' AND movement_type = 'devol' THEN ROUND((m.product_qty * product_uom.factor)::decimal(16,1))
    END AS uom_po_qty

    , pt.uom_po_id

    , m.location_id
    , m.location_dest_id
    , m.reference
    , pt.categ_id
    , spc.movement_type
FROM
    stock_move m
LEFT JOIN stock_picking   spc ON (m.picking_id = spc.id)
LEFT JOIN stock_location  ls  ON (ls.id = m.location_id)
LEFT JOIN stock_location  ld  ON (ld.id = m.location_dest_id)
LEFT JOIN stock_warehouse whs ON ls.parent_path like concat('%/', whs.view_location_id, '/%')
LEFT JOIN stock_warehouse whd ON ld.parent_path like concat('%/', whd.view_location_id, '/%')
LEFT JOIN product_product pp  ON pp.id = m.product_id
LEFT JOIN product_template pt ON pt.id = pp.product_tmpl_id
LEFT JOIN uom_uom product_uom ON product_uom.id = pt.uom_po_id

WHERE
    pt.type = 'product'
    AND product_qty != 0
    AND  (  ((ls.usage = 'transit'  AND ls.company_id IS NOT NULL) AND ld.usage = 'internal')
 	    OR
 	    (ls.usage = 'internal' AND (ld.usage = 'transit' AND ld.company_id IS NOT NULL))  )
    AND m.state = 'done'
 --   AND (whs.id != 0 AND  whd.id != 0)

);
"""
        self.env.cr.execute(query)
