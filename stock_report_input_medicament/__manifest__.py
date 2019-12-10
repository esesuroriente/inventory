# -*- coding: utf-8 -*-
# Copyright 2019 - ESE SURORIENTE CAUCA < >
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Report Stock Input Medicament',
    'version': '13.0.1.0.0-beta.2',
    'author': 'ESE SURORIENTE CAUCA',
    'license': 'AGPL-3',
    'category': 'Other',
    'depends': [
        'stock',

        'product_medicament',
        'product_medicament_lots',
        'stock_picking_vendor_remission_fields'
    ],
    'data': [
        'report/report_stock_input_medicament.xml',

        'data/stock_report_input_medicament_data.xml',

        'security/ir.model.access.csv',
    ],
    'installable': True,
    'auto_install': False,
}
