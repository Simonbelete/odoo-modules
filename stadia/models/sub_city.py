from odoo import models, api, fields

class SubCity(models.Model):
    _name = 'subcity'

    name = fields.Char(required=True)