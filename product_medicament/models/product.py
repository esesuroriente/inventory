
from odoo import fields, models, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'


    is_medicament = fields.Boolean(tracking=True)

    active_component = fields.Char(tracking=True)
    storage = fields.Selection([
                            ('norm', 'Normal'),
                            ('cold', 'Cadena de frío')],
                            string='Storage',
                            tracking=True
                            )

    commercial_presentation = fields.Text(tracking=True)
    individual_presentation = fields.Text(tracking=True)
    composition = fields.Text(tracking=True)
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

    med_group_id = fields.Many2many('product.medicament.group'
                                    , string='Group'
                                    , tracking=True
                                    )


    @api.onchange('is_medicament')
    def onchange_tracking(self):
        if self.is_medicament:
            self.tracking = 'lot'
