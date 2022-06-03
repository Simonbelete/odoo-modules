from email.policy import default
from odoo import fields, api, models
from datetime import datetime

class HrAttendance(models.Model):
    _inherit = 'hr_attendance'

    # Today date for day attendace calculation
    attendance_date = fields.Date(default=datetime.today())
    regularization = fields.Boolean(string="Regularization")