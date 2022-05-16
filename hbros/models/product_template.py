from odoo import fields, models

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    product_type = fields.Many2one('hbros.product.type', string='Product Type')
    product_specification = fields.Many2one('hbros.product.specification', string='Product Specification')
    measurement_uom_id = fields.Many2one('uom.uom', 'Product Unit Measurement')