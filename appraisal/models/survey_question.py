from odoo import models, fields


class SurveyQuestionScoreSelection(models.Model):
    """ Score types with weight"""
    _name = 'appraisal.score.selection'
    _rec_name = 'value'

    value = fields.Char(required=True)
    description = fields.Text()
    weight = fields.Integer(required=True, default=0)

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
    score_method = fields.Selection([
        ('range', 'Range'),
        ('selection', 'Selection')
    ], default="selection", help="score method: refer to answer"
        "range refer to:- value between min and max"
        "selection refer to(selection => weight):- 1 => 1, 2 => 2, 3 => 10")
    score_selection_ids = fields.Many2many('appraisal.score.selection')
    score_min = fields.Integer()
    score_max = fields.Integer()

    # reference field
    survey_ids = fields.Many2many('appraisal.survey')