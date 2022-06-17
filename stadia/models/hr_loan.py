from odoo import fields, api, models

class HrLoan(models.Model):
    _inherit = 'hr.loan'

    reason = fields.Text()
    guarantor_id = fields.Many2one('hr.employee')
