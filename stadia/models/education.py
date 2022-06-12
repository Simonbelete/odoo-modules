from odoo import fields, api, models

class Education(models.Model):
    _name = 'stadia.education'

    name = fields.Char(required=True)