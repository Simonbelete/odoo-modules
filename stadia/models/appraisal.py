import uuid
from odoo import fields, api, models

class StadiaAppraisal(models.Model):
    _name = 'stadia.appraisal'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    def _get_default_token(self):
        return str(uuid.uuid4())

    employee_id = fields.Many2one('hr.employee', required=True)
    template_id = fields.Many2one('stadia.appraisal.template')
    # uuid for url parameter
    # instead of using id as a url parament we use generated uuid
    token = fields.Char('Token', default=lambda self: self._get_default_token(), copy=False)
    user_answer_ids = fields.One2many('stadia.user.appraisal.answer', 'appraisal_id')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Done')
    ])
    total_score = fields.Float(compute="_compute_total_score")
    total_average_score = fields.Float(compute="_compute_average_score")

    def _compute_total_score(self):
        self.ensure_one()
        total = 0
        count = 0
        for ans in self.user_answer_ids:
            total += ans.answer_selection_id.weight
            count += 1

        self.total_score = total
        self.total_average_score = total / count
        

    def action_start_appraisal(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_url',
            'name': 'Start Appraisal',
            'target': 'self',
            'url': '/appraisal/%s' % str(self.token)
        }

    @api.model
    def create(self, vals):
        """ Populate answers with the give template """
        res = super(StadiaAppraisal, self).create(vals)
        res.sudo()._populate_user_answers()   
        return res

    def _populate_user_answers(self):
        self.ensure_one()
        questions = self.template_id.question_ids

        user_answers = []
        for question in questions:
            val = {
                'appraisal_id': self.id,
                'question_id': question.id,
                'answer_selection_id': False
            }
            user_answers.append((0, False, val))

        self.write({'user_answer_ids': user_answers})

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
    description = fields.Html()
    sequence = fields.Integer(default=10)
    is_section = fields.Boolean('Is Section')
    # Selctions Answers
    answer_ids = fields.Many2many('stadia.appraisal.answer')


class AppraisalAnsweres(models.Model):
    """ Appraisal Questions's Selection """
    _name = 'stadia.appraisal.answer'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(required=True)
    description = fields.Text()
    weight = fields.Integer(required=True, default=0)
    sequence = fields.Integer(default=10)
    # question_id = fields.Many2many('stadia.appraisal.question')

class UserAppraisalAnser(models.Model):
    _name = 'stadia.user.appraisal.answer'

    appraisal_id = fields.Many2one('stadia.appraisal')
    question_id = fields.Many2one('stadia.appraisal.question')
    answer_selection_id = fields.Many2one('stadia.appraisal.answer')
    