from odoo import fields, api, models


class EmployeeResumeDetail(models.Model):
    _inherit = 'hr.resume.line'
    organization = fields.Many2one('res.partner')
