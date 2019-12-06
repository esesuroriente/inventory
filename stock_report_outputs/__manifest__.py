# -*- coding: utf-8 -*-
# Copyright 2019 - ESE SURORIENTE CAUCA < >
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


{
    'name': 'Report Stock Quantity out',
    'version': '13.0.1.0.0-beta.2',
    'author': 'ESE SURORIENTE CAUCA, Odoo',
    'license': 'AGPL-3',
    'category': 'Stock',
    'depends': [
          'stock'
        , 'stock_picking_movement_type'
    ],
    'data': [
        'security/ir.model.access.csv',

        'report/report_stock_quantity_outputs.xml',

    ],
    'installable': True,
    'auto_install': False,
}
