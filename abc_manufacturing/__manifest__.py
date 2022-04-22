{
    'name': 'abc_manufacturing',
    'version': '0.1.0',
    'category': 'Manufacturing/abc',
    'description': 'Manufacturing helper module',
    'depends': ['base', 'mrp'],
    'author': 'Simon Belete',
    'data': [
        'security/ir.model.access.csv',

        'report/production_report_templates.xml',
        'report/production_report_views.xml',
        
        'views/in_product_template_only_form_view.xml',
        'views/in_mrp_bom_form_view.xml',
        'views/in_mrp_production_form_view.xml'
    ]
}