# -*- coding: utf-8 -*-
{
    'name': "stadia_contract",
    'sequence': 4,

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'om_account_asset'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/hr_employee_asset_view.xml',
        'views/hr_contract_state_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [

    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}