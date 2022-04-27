from odoo import models, fields

class Traits(models.Model):
    _name = "stadia.appraisal.traits"

    name = fields.Char(required = True)
    definition = fields.Text()