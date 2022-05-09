from odoo import fields, models, _, api


class InterviewStage(models.Model):
    _inherit = "hr.applicant"
    first_stage = fields.Char(string="First Stage")
    stage_name = fields.Char(related="stage_id.name", string="Sname")