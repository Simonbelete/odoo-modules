from odoo import models, fields

class InProductTemplate(models.Model):
    _inherit = 'product.template'

    product_type = fields.Many2one('product.type.model', string = 'Product Type', required = True)