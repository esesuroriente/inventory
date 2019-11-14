# -*- coding: utf-8 -*-
# Copyright 2019 - ESE SURORIENTE CAUCA < >
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Product Medicament Lots',
    'version': '13.0.1.0.0-beta.1',
    'author': 'ESE SURORIENTE CAUCA',
    'license': 'AGPL-3',
    'category': 'Product',
    'depends': [
        'stock',
    ],
    'data': [
        'security/ir.model.access.csv',
        
        'views/stock_production_lot_view.xml',
    ],
    'installable': True,
    'auto_install': False,
}
