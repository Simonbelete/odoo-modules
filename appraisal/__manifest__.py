{
    'name': 'appraisal',
    'version': '0.1.0',
    'category': 'Human Resources',
    'description': 'Appraisal Form',
    'depends': ['base', 'hr'],
    'author': 'Simon Belete',
    'data': [
        'security/ir.model.access.csv',
        'views/res_config_settings_views.xml',
        'views/appraisal_kanban_view.xml',
        'views/appraisal_views.xml',
        'views/appraisal_menus.xml'
    ]
}