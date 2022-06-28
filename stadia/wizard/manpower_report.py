from odoo import api, fields, models

class HiredManpowerReport(models.TransientModel):
    _name = 'hired.manpower.report'

    date_from = fields.Date(required=True)
    date_to = fields.Date(required=True)

    def print_report(self):
        self.ensure_one()
        [data] = self.read()
        datas = {
            'ids': [],
            'model': 'hr.employee',
            'form': data
        }
        return self.env.ref('stadia.hired_manpower_report').report_action([], data=datas)
