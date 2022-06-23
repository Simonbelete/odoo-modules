from odoo import api, fields, models

class City(models.Model):
    _name = 'stadia.city'

    name = fields.Char(required=True)