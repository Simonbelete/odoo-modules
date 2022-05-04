{
    'name': 'appraisal',
    'version': '0.1.0',
    'category': 'Human Resources',
    'description': 'Appraisal Manager',
    'depends': ['base', 'hr'],
    'author': 'Simon Belete',
    'data': [
        'security/ir.model.access.csv',
        'data/category_data.xml',
        'data/cron.xml',
        'views/res_config_settings_views.xml',
        'views/appraisal_template.xml',
        'views/hr_employee_views.xml',
        'views/appraisal_category_views.xml',
        'views/appraisal_survey_views.xml',
        'views/appraisal_survey_question.xml',
        'views/appraisal_appraisal_views.xml',
        'views/appraisal_score_selection_views.xml',
        'views/appraisal_menus.xml'
    ]
}