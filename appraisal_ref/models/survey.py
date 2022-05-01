from odoo import models, fields

class Survey(models.Model):
    _name = 'appraisal.survey'
    _rec_name = 'title'

    title = fields.Char('Survey Title', required=True)
    description = fields.Html(
        "Description", sanitize=False,
        help="This message will be displayed on the top of appraisal"
    )
    survey_question_ids = fields.Many2many('appraisal.survey.question', copy=True)

    # TODO: remove it
    name = fields.Text(string = 'Title', required = True)