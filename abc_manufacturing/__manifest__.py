{
    'name': 'abc_manufacturing',
    'version': '0.1.0',
    'category': 'Manufacturing/abc',
    'description': 'Manufacturing helper module',
    'depends': ['base', 'mrp'],
    'author': 'Simon Belete',
    'data': [
        'security/ir.model.access.csv',
        
        'views/in_product_template_only_form_view.xml',
        'views/in_mrp_bom_form_view.xml'
    ]
}