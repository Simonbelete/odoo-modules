{
    'name': 'STADIA Engineering Works Consultant PLC',
    'version': '0.1.0',
    'category': 'All',
    'author': '',
    'application': True,
    'depends': [
        'base',
        'hr',
        'hr_recruitment'
    ],
    'data': [
        'security/acquisition_security.xml',
        
        'data/ir_mail_server_data.xml',
        'data/res_user_data.xml',
        'data/hr_department_data.xml',
        'data/hr_job_data.xml',

        'views/acquisition_views.xml',
        'views/acquisition_menus.xml'
    ]
}