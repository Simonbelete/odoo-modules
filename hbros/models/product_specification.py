from odoo import fields, models

class ProductSpecification(models.Model):
    """ Product SPECF """
    _name = "hbros.product.specification"

    name = fields.Char()