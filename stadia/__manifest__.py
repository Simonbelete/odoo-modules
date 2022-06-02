{
    'name': 'STADIA Engineering Works Consultant PLC',
    'version': '0.1.0',
    'category': 'All',
    'author': '',
    'application': True,
    'depends': [
        'base',
        'hr',
        'hr_recruitment',
        'hr_contract'
    ],
    'data': [
        'security/acquisition_security.xml',
        'security/ir.model.access.csv',
        
        'data/ir_mail_server_data.xml',
        'data/res_user_data.xml',
        'data/hr_department_data.xml',
        'data/hr_job_data.xml',
        'data/promotion_data.xml',

        'views/acquisition_views.xml',
        'views/hr_employee_views.xml',
        'views/promotion_views.xml',
        'views/promotion_stage_views.xml',
        'views/hr_hob_views.xml',
        'views/hr_applicant_views.xml',
        'views/acquisition_menus.xml',
        'views/promotion_menus.xml'
    ]
}