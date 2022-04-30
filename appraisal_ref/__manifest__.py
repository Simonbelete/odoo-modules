{
    'name': 'appraisal_ref',
    'version': '0.1.0',
    'category': 'Human Resources',
    'description': 'Appraisal Form',
    'depends': ['base', 'hr'],
    'author': 'Simon Belete',
    'data': [
        'security/ir.model.access.csv',
        'views/appraisal_template.xml',
        'views/appraisal_page_template.xml',
        'views/res_config_settings_views.xml',
        'views/appraisal_kanban_view.xml',
        'views/appraisal_views.xml',
        'views/appraisal_survey_views.xml',
        'views/appraisal_survey_views_question.xml',
        'views/appraisal_trait_views.xml',
        'views/appraisal_score_views.xml',
        'views/appraisal_menus.xml'
    ]
}