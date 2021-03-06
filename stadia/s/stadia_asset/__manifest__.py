{
    'name': 'STADIA Asset',
    'version': '0.1.0',
    'category': 'Stadia',
    'author': '',
    'depends': [
        'hr',
        'om_account_asset'
    ],
    'data': [
        'security/ir.model.access.csv',

        'data/decimal_precision_data.xml',

        'views/account_asset_views.xml',
        'views/asset_specification_views.xml',
        'views/hr_employee_views.xml',
        'views/asset_request_views.xml',
        'views/asset_menus.xml'
    ]
}