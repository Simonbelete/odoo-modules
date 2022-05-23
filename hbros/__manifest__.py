{
    'name': 'hbros',
    'version': '0.1.0',
    'category': 'Manufacturing',
    'depends': ['base', 'mrp', 'om_hr_payroll'],
    'data': [
        'security/ir.model.access.csv',

        'data/hr_employee_data.xml',
        'data/uom_category_data.xml',
        'data/uom_uom_data.xml',
        'data/product_type_data.xml',
        'data/product_specification_data.xml',
        'data/product_category_data.xml',
        'data/product_template_raw_data.xml',
        'data/product_template_ac_data.xml',
        'data/product_template_part_data.xml',

        'views/product_template_views.xml',
        'views/mrp_production_views.xml',
        'views/mrp_bom_views.xml'
    ]
}