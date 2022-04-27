from odoo import models, fields

class Trait(models.Model):
    _name = "stadia.appraisal.trait"

    name = fields.Char(required = True)
    definition = fields.Text()
    sub_traits_ids = fields.One2many('stadia.appraisal.sub.trait', 'trait_id')