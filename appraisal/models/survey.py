from odoo import models, fields

class Survey(models.Model):
    """ Stores Appraisal forms"""
    _name = 'appraisal.survey'
    _rec_name = 'title'

    title = fields.Char('Survey Title', required=True)
    description = fields.Html(
        "Description", sanitize=False,
        help="This message will be displayed on the top of appraisal"
    )
    question_ids = fields.Many2many('appraisal.survery.question', string="Questions",)