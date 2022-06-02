{
    'name': 'STADIA Acquisition',
    'version': '0.1.0',
    'category': 'Stadia',
    'author': '',
    'depends': [
        'hr_recruitment'
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',

        'data/hr_department_data.xml',
        'data/hr_job_data.xml',

        'views/acquisition_views.xml',
        'views/acquisition_menus.xml',
        'views/recommendation_views.xml',
        'views/hr_applicant_views.xml'
    ]
}