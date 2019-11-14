
from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = 'stock.production.lot'

    laboratory = fields.Char(tracking=True)
    register_invima = fields.Text(tracking=True)
    cums = fields.Char(tracking=True)
    consecutive_cums = fields.Char(tracking=True)

    manufacturing_date = fields.Datetime(tracking=True)
