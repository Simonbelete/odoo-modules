from email.policy import default
from odoo import fields, api, models
from datetime import datetime

class HrAttendance(models.Model):
    _inherit = 'hr.attendance'

    active = fields.Boolean(default=True)
    # Today date for day attendance calculation
    attendance_date = fields.Date(default=datetime.today())
    regularization = fields.Boolean(string="Regularization")