# -*- coding: utf-8 -*-
from odoo import fields, models, api


class ProductTemplate(models.Model):
    _inherit = 'stock.picking'

    vendor_remission_date = fields.Date()
    vendor_remission_number = fields.Char()
