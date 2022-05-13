{
    'name': 'stadia',
    'version': '0.1.0',
    'category': 'Human Resources',
    'author': '',
    'depends': [
        'base',
        'hr',
        'hr_recruitment'
    ],
    'data': [
        'security/ir.model.access.csv',

        'data/hr_job_data.xml',
        'data/hr_department_data.xml',

        'views/hr_job_views.xml',
        'views/internal_applicant_view.xml',
        'views/hr_recruitment_menu.xml'
    ]
}