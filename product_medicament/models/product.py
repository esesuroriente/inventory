# -*- coding: utf-8 -*-

from odoo import fields, models, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'


    is_medicament = fields.Boolean(tracking=True)

    active_component = fields.Char(tracking=True)
    storage = fields.Selection([
                                    ('norm', 'Normal de 15ºC a 30ºC. Humedad entre 25% a 70%'),
                                    ('cold', 'Cadena de frío de 2ºC a 8ºC')],
                                    string='Storage',
                                    tracking=True
                                )

    commercial_presentation = fields.Text(tracking=True)
    individual_presentation = fields.Char(tracking=True)
    concentration = fields.Char(tracking=True)
    notes = fields.Text(tracking=True)
    special_condition = fields.Selection([
                                ('reg',  'Regulados'),
                                ('cont', 'Controlados'),
                                ('both', 'Ambos')],
                                string='Special Condition',
                                tracking=True
                            )

    med_use_id = fields.Many2many('product.medicament.use'
                                      , string='Medicament use'
                                      , tracking=True
                                 )

    med_group_id = fields.Many2many('product.pharmacological.group'
                                        , string='Pharmacological Group'
                                        , tracking=True
                                    )


    @api.onchange('is_medicament')
    def onchange_tracking(self):
        if self.is_medicament:
            self.tracking = 'lot'
