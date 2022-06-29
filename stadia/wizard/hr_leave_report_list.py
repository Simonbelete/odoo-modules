from odoo import api, fields, models
from datetime import datetime

class HrLeaveReportList(models.TransientModel):
    _name = 'hr.leave.report.list'

    date_to = fields.Date(string="Date To", required=True, default=datetime.now())

    def print_report(self):
        self.ensure_one()
        [data] = self.read()
        data['emp'] = self.env.context.get('active_ids', [])
        employees = self.env['hr.employee'].browse(data['emp'])
        datas = {
            'ids': [],
            'model': 'hr.employee',
            'form': data
        }
        return self.env.ref('stadia.hr_leave_report_list_report').report_action(employees, data=datas)