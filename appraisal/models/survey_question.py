from odoo import models, fields

class SurveyQuestion(models.Model):
    _name = 'appraisal.survey.question'

    name = fields.Text(string = 'Question', required = True)
    trait_id = fields.Many2one('appraisal.trait', string="Category")
    survey_ids = fields.Many2many('appraisal.survey')