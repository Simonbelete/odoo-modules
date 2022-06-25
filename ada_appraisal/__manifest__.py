{
    'name': 'Appraisal',
    'version': '0.1.0',
    'category': 'All',
    'description': 'Manage Employee Appraisal',
    'author': 'Simon Belete',
    'depends': [
        'base',
        'website'
    ],
    'data': [
        'template/assets.xml',

        'security/ir.model.access.csv',

        'views/template_views.xml',
        'views/question_views.xml',
        'views/appraisal_menus.xml'
    ]
}