from odoo import fields, models

class ProductType(models.Model):
    """ Material's type eg ANGLE, ELECTROD ... """
    _name = 'hbros.product.type'
    _res_name = 'name'

    name = fields.Char(required=True)