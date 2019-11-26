# -*- coding: utf-8 -*-
from odoo import fields, models, api


class ProductTemplate(models.Model):
    _inherit = 'stock.picking'

    movement_type = fields.Selection([
                              ('rote' , 'Rote')
                            , ('prest', 'Préstamo')
                            , ('devol', 'Devolución')],
                            string='Movement type',
                            )
