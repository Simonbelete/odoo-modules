from odoo import models, fields

class AppraisalScore(models.Model):
    """ Assed employees appraisal result. """
    _name = 'appraisal.appraisal.score'

    appraisal_id = fields.Many2one('appraisal.appraisal')
    question_id = fields.Many2one('appraisal.survey.question')
    score = fields.Integer(required = True, default = 0)