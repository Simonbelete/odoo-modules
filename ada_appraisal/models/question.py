from odoo import api, fields, models

class Question(models.Model):
    """ Template's questions with sections """
    _name = 'ada.appraisal.question'

    title = fields.Char()
    template_id = fields.Many2one('ada.appraisal.template')
    sequence = fields.Integer('Sequence', default=10)
    is_page = fields.Boolean('Is a page')
    # question_ids = fields.One2many('ada.appraisal.question')