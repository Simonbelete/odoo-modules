from odoo import fields, api, models

class PromotionStage(models.Model):
    _name = 'stadia.promotion.stage'

    name = fields.Char('Stage Name', required=True)
    sequence = fields.Integer('Sequence', default=10)
    survey_id = fields.Many2one('survey.survey')