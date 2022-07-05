from odoo import api, fields, models

class PayrollReportWizard(models.TransientModel):
    _name = 'payroll.report.wizard'

    date_from = fields.Date(required=True)
    date_to = fields.Date(required=True)

    def print_report(self):
        self.ensure_one()
        [data] = self.read()
        data['payslip'] = self.env.context.get('active_ids', [])
        datas = {
            'ids': [],
            'model': 'hr.employee',
            'form': data
        }
        return self.env.ref('stadia.hr_leave_report_list_report').report_action(data=datas)
