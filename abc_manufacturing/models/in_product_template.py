from odoo import models, fields, api

class InProductTemplate(models.Model):
    _inherit = 'product.template'

    product_type = fields.Many2one('product.type.model', string = 'Product Type', required = True)
    measurement_uom_id = fields.Many2one('uom.uom', 'Product Unit Measurement')