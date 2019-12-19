# -*- coding: utf-8 -*-

{
    'name': "Warehouse Restrictions",

    'summary': """
         Warehouse and Stock Location Restriction on Users.""",

    'description': """
        This Module Restricts the User from Accessing Warehouse and Process
        Stock Moves other than allowed to Warehouses and Stock Locations.
    """,

    'author':  "ESE SURORIENTE, Techspawn Solutions",
    'website': " ",
    'license': 'AGPL-3',
    'category': 'Warehouse',
    'version': '13.0.1.0.0-beta.4',
    'images':  ['static/description/WarehouseRestrictions.jpg'],
    'depends': ['base'
                , 'stock'

                # Specific modules
                , 'stock_report_outputs'
                , 'purchase'
               ],
    'data': [
        'views/users_view.xml',

        'security/security.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
