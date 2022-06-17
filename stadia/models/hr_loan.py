from odoo import fields, api, models

class HrLoan(models.Model):
    _inherit = 'hr.loan'

    reason = fields.Text()