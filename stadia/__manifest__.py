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
        'hr_contract',
        'hr_attendance',
        'hr_payroll_community',
        'oh_employee_documents_expiry',
        'oh_appraisal',
        'ohrms_loan',
        'prt_report_attachment_preview',
        'report_xlsx'
    ],
    'data': [
        'views/stadia_template.xml',

        'security/acquisition_security.xml',
        'security/security.xml',
        'security/ir.model.access.csv',
        
        'data/mail_data.xml',
        'data/ir_mail_server_data.xml',
        'data/res_user_data.xml',
        'data/resource_calendar_data.xml',
        'data/hr_department_data.xml',
        'data/hr_job_data.xml',
        'data/promotion_data.xml',
        'data/hr_salary_rule_category_data.xml',
        'data/hr_salary_rule_data.xml',
        'data/education_data.xml',
        'data/workplace_data.xml',

        'report/hr_employee_badge.xml',
        'report/hr_contract_employee_badge.xml',
        'report/header_template.xml',
        'report/stamp_logo_template.xml',
        'report/acquisition_job_spec.xml',
        'report/asset_report.xml',
        'report/acquisition_format.xml',
        'report/hiring_promotion_template.xml',
        'report/contract_agreement.xml',
        'report/lateral_transfer.xml',

        'views/hr_recruitment_views.xml',
        'views/promotion_views.xml',
        'views/promotion_stage_views.xml',
        'views/acquisition_views.xml',
        'views/hr_employee_views.xml',
        'views/hr_hob_views.xml',
        'views/hr_applicant_views.xml',
        'views/regularization_views.xml',
        'views/hr_contract_views.xml',
        'views/asset_movement_views.xml',
        'views/account_asset_views.xml',
        'views/acquisition_menus.xml',
        'views/promotion_menus.xml',
        'views/regularization_menus.xml',
        'views/asset_menus.xml'
    ],
    'qweb': [
        'static/src/xml/asset.xml'
    ]
}