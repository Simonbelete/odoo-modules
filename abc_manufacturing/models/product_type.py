from odoo import models, fields

class ProductType(models.Model):
    _name = 'product.type.model'

    name = fields.Char(required = True)