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


class LateralTransferManpowerReport(models.TransientModel):
    _name = 'lateral.transfer.manpower.report'

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
        return self.env.ref('stadia.lateral_transfer_manpower_report').report_action([], data=datas)

class PromotionManpowerReport(models.TransientModel):
    _name = 'promotion.manpower.report'

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
        return self.env.ref('stadia.promotion_abc_manpower_report').report_action([], data=datas)
