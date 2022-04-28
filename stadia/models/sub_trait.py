from odoo import models, fields

class SubTrait(models.Model):
    _name = 'stadia.appraisal.sub.trait'

    definition = fields.Text()
    trait_id = fields.Many2one('stadia.appraisal.trait', required = True)