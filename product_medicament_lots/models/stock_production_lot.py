
from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = 'stock.production.lot'

    laboratory = fields.Char(tracking=True)
    register_invima = fields.Char(tracking=True)
    cums = fields.Char(tracking=True)
    cums_consecutive = fields.Char(tracking=True)
    cums_status = fields.Selection([('vigente', 'Vigente'),
                                    ('vencido', 'Vencido'),
                                    ('tramite', 'Trámite de renovación'),
                                    ('pfuerza', 'Pérdida de fuerza'),
                                    ('otro', 'Otros estados')],
                                      string='cum status',
                                      tracking=True
                                )

    manufacturing_date = fields.Datetime(tracking=True)
