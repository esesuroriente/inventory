# -*- coding: utf-8 -*-
# Copyright 2019 - ESE SURORIENTE CAUCA < >
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Report Stock Input Medicament',
    'version': '13.0.1.0.0-beta.2',
    'author': 'ESE SURORIENTE CAUCA',
    'license': 'AGPL-3',
    'category': 'Stock',
    'depends': [
        'stock',

        'product_medicament',
        'product_medicament_lots',
        'stock_picking_vendor_invoice_fields'
    ],
    'data': [
        'report/report_stock_input_medicament.xml',

        'security/ir.model.access.csv',
    ],
    'installable': True,
    'auto_install': False,
}
