# -*- coding: utf-8 -*-

from odoo import fields, models, api, _

class ProductPharmacologicalGroup(models.Model):
    _description = 'Product Pharmacological Group    '
    _name = 'product.pharmacological.group'
    _order = 'complete_name'
    _rec_name = 'complete_name'

    name = fields.Char(string='Pharmacological group', index=True, required=True)
    complete_name = fields.Char(  'Complete Name'
                                , compute='_compute_complete_name'
                                , store=True )
    parent_id = fields.Many2one(  'product.pharmacological.group'
                                , 'Parent Group'
                                , index=True
                                , ondelete='cascade' )
    child_id = fields.One2many(   'product.pharmacological.group'
                                , 'parent_id'
                                , 'Child Group')

    active = fields.Boolean(default=True
    , help="The active field allows you to hide the category without removing it.")

    @api.depends('name', 'parent_id.complete_name')
    def _compute_complete_name(self):
        for category in self:
            if category.parent_id:
                category.complete_name = '%s / %s' % (category.parent_id.complete_name, category.name)
            else:
                category.complete_name = category.name

    @api.model
    def name_create(self, name):
        return self.create({'name': name}).name_get()[0]


    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Group already exists!"),
    ]
