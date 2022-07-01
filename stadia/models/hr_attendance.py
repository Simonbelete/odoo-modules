from email.policy import default
from odoo import fields, api, models
from datetime import datetime
from odoo.exceptions import UserError

class HrAttendance(models.Model):
    _inherit = 'hr.attendance'

    active = fields.Boolean(default=True)
    # Today date for day attendance calculation
    attendance_date = fields.Date(default=datetime.today())
    regularization = fields.Boolean(string="Regularization")
    reason_for_change = fields.Char()

    def write(self, vals):
        if(not 'reason_for_change' in vals):
            raise UserError('Please enter the reason for changes')
        else:
            res = super(HrAttendance, self).write(vals)
            return res
