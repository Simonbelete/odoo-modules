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
        'hr_skills',
        'hr_payroll_community',
        'oh_employee_documents_expiry',
        'ohrms_loan',
        'prt_report_attachment_preview',
        'report_xlsx',
        'survey',
        'stock',
        'website'
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
        'data/sequence.xml',
        'data/decimal_precision.xml',
        'data/hr_department_data.xml',
        'data/hr_job_data.xml',
        'data/subcity_data.xml',
        'data/promotion_data.xml',
        'data/hr_holidays_data.xml',
        'data/hr_salary_rule_category_data.xml',
        'data/hr_salary_rule_data.xml',
        'data/education_data.xml',
        'data/workplace_data.xml',
        'data/city_data.xml',
        'data/appraisal_data.xml',
        'data/asset_data.xml',
        'data/hr_degree.xml',

        'data/employee_data/family_relation.xml',
        'data/employee_data/hr_employee_admin.xml',
        'data/employee_data/hr_employee_design.xml',
        'data/employee_data/hr_employee_project_for.xml',
        'data/employee_data/hr_employee_rcmd.xml',
        'data/employee_data/asset.xml',

        'wizard/hr_leave_report_list.xml',
        'wizard/manpower_report.xml',
        'wizard/asset_report_wizard.xml',
        'wizard/attendance_report.xml',

        'report/component_templates.xml',
        'report/hr_contract_employee_badge.xml',
        'report/header_template.xml',
        'report/asset_report.xml',
        'report/acquisition_format.xml',
        'report/hiring_promotion_template.xml',
        'report/contract_agreement.xml',
        'report/lateral_transfer.xml',
        'report/hr_experience_report_id.xml',
        'report/hr_experience_template.xml',
        'report/loan.xml',
        'report/guarantor_letter.xml',
        'report/employment_notification.xml',
        'report/acceptance_letter.xml',
        'report/promotion.xml',
        'report/manpower_report.xml',
        'report/hr_leave_report_list_report.xml',
        'report/attendance_report.xml',
        'report/employee_list_repot.xml',
        'report/payroll_repot.xml',
        
        'views/hr_recruitment_views.xml',
        'views/promotion_views.xml',
        'views/promotion_stage_views.xml',
        'views/acquisition_views.xml',
        'views/hr_hob_views.xml',
        'views/hr_applicant_views.xml',
        'views/regularization_views.xml',
        'views/hr_contract_views.xml',
        'views/asset_movement_views.xml',
        'views/account_asset_views.xml',
        'views/hr_loan_views.xml',
        'views/hr_attendance_view.xml',
        'views/acquisition_menus.xml',
        'views/promotion_menus.xml',
        'views/regularization_menus.xml',
        'views/hr_employee_views.xml',
        'views/work_place_views.xml',
        'views/asset_menus.xml',
        'views/hr_employee_menus.xml',
        'views/hr_resume_line_views.xml',
        'views/appraisal_views.xml',

        'website/appraisal_website.xml'
    ],
    'qweb': [
        'static/src/xml/asset.xml',
        'static/src/xml/manpower.xml'
    ]
}
