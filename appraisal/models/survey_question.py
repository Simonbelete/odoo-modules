from odoo import models, fields

class SurveyQuestion(models.Model):
    """ Questions that will be asked in a survey. """
    _name = 'appraisal.survey.question'
    _description = 'Survery Question'
    _rec_name = 'title'

    title = fields.Char('Title', required=True)
    description = fields.Html(
        'Description', sanitize=True,
        help="Use this field to add additional explanations about your question"
    )
    sequence = fields.Integer('Sequence', default=10)
    category_id = fields.Many2one('appraisal.category')