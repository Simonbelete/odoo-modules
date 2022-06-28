from odoo import api, fields, models

class HiredManpowerReport(models.TransientModel):
    _name = 'hired.manpower.report'

    date_from = fields.Date()
    date_to = fields.Date()

    def print_report(self):
        self.ensure_one()
        return self.env.ref('stadia.hr_leave_report_list_report').report_action(employees, data=datas)
