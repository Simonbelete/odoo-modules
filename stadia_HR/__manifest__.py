# -*- coding: utf-8 -*-
{
    'name': "Stadia HR",
    'sequence': 1,

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
    'depends': ['base', 'hr', 'hr_skills', 'hr_contract', 'hr_holidays', 'hr_attendance', 'hr_recruitment',
                'web_notify', 'Stadia-Asset-Management', 'account'],

    # always loaded
    'data': [
        # security, data,views,wizard, reports
        # 'security/ir.model.access.csv',
        'security/user_group.xml',
        'security/ir.model.access.csv',
        'data/data1.xml',
        'report/record3.xml',
        'report/report_template3.xml',
        'report/record.xml',
        'report/report_template.xml',
        'report/record2.xml',
        'report/report_template2.xml',
        'views/views.xml',
        'views/templates.xml',
        'views/page_modify1.xml',
        'views/private_information_inherited.xml',
        'views/hr_skill_inherited_view.xml',
        'views/other_information.xml',
        'views/hr_skill_inehited_view2.xml',
        'views/resume_type.xml',
        'views/private_information_edite.xml',
        'views/training.xml',
        'views/payroll_contact_detail.xml',
        'views/hr_contract_invisible.xml',
        'views/smart_button.xml',
        'views/employee_manufacture_order.xml',
        'views/template_css.xml',
        'views/filter_by_asset.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,

}
