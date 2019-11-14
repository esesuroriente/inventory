from odoo import fields, models

class ProductMedicamentGroup(models.Model):
    _description = 'Product Medicament Group    '
    _name = 'product.medicament.group'
    _order = 'name'

    name = fields.Char(string='Medicament group', required=True, translate=True)
    color = fields.Integer(string='Color Index')
    active = fields.Boolean(default=True, help="The active field allows you to hide the category without removing it.")

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Group already exists!"),
    ]
