from odoo import models, fields

class Survey(models.Model):
    _name = 'appraisal.survey'

    name = fields.Text(string = 'Title', required = True)
    # survey_question_ids = fields.Many2many('appraisal.survey.question')