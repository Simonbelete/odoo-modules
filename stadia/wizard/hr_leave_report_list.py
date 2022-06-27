from odoo import api, fields, models
from datetime import datetime

class HrLeaveReportList(models.TransientModel):
    _name = 'hr.leave.report.list'

    date_to = fields.Date(string="Date To", required=True)