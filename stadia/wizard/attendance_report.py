from odoo import api, fields, models

class AttendanceReportWizard(models.TransientModel):
    _name = 'attendance.report'

    date_from = fields.Date(required=True)
    date_to = fields.Date(required=True)

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
        return self.env.ref('stadia.report_attendance_list').report_action(employees, data=datas)