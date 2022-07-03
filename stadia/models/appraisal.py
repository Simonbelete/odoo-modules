from odoo import fields, api, models

class Appraisal(models.Model):
    _name = 'stadia.appraisal'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    survey_id = fields.Many2one('survey.survey')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Done')
    ])


class AppraisalTemplate(models.Model):
    _name = 'stadia.appraisal.template'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(required=True)
    active = fields.Boolean(default=True)
    question_ids = fields.Many2many('stadia.appraisal.question')


class AppraisalQuestion(models.Model):
    _name = 'stadia.appraisal.question'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(required=True)
    sequence = fields.Integer(default=10)
    is_section = fields.Boolean('Is Section')
    weight = fields.Integer(required=True, default=0)
    answer_ids = fields.One2many('stadia.appraisal.answer', 'question_id')


class AppraisalAnsweres(models.Model):
    _name = 'stadia.appraisal.answer'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(required=True)
    description = fields.Text()
    weight = fields.Integer(required=True, default=0)
    sequence = fields.Integer(default=10)
    question_id = fields.Many2one('stadia.appraisal.question')