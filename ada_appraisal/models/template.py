from odoo import api, fields, models

class AppraisalTemplate(models.Model):
    """ Top Category for appraisal category """
    _name = 'ada.appraisal.template'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(required=True)
    active = fields.Boolean(default=True)
    question_ids = fields.One2many('ada.appraisal.question', 'template_id')