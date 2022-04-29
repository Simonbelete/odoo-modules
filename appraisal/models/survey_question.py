from odoo import models, fields

class SurveyQuestion(models.Model):
    _name = 'appraisal.survey.question'

    name = fields.Text(string = 'Question', required = True)
    type = fields.Selection([
        ('Text', 'Multiple line Text'),
        ('Char', 'Single Line Text Box'),
        ('Date', 'date')
    ])
    survey_ids = fields.Many2many('appraisal.survey')