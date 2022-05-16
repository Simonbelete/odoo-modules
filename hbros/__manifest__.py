{
    'name': 'hbros',
    'version': '0.1.0',
    'category': 'Manufacturing',
    'depends': ['base', 'mrp'],
    'data': [
        'security/ir.model.access.csv',

        'data/uom_category_data.xml',
        'data/uom_uom_data.xml',
        'data/product_type_data.xml',
        'data/product_specification_data.xml',
        'data/product_category_data.xml',
        'data/product_template_data.xml',

        'views/product_template_views.xml',
    ]
}