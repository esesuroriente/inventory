# -*- coding: utf-8 -*-
from odoo import fields, models, api


class ProductTemplate(models.Model):
    _inherit = 'stock.picking'

    vendor_invoice_date = fields.Date()
    vendor_invoice_number = fields.Char()
