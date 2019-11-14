from odoo import fields, models

class ProductMedicamentUse(models.Model):
    _description = 'Product Medicament Use'
    _name = 'product.medicament.use'
    _order = 'name'

    name = fields.Char(string='Medicament Use', required=True, translate=True)
    color = fields.Integer(string='Color Index')
    active = fields.Boolean(default=True, help="The active field allows you to hide the category without removing it.")

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Tag name already exists!"),
    ]
