from odoo import api, fields, models

class ManpowerReport(models.AbstractModel):
    _name = 'report.stadia.manpower_report'
    
    @api.model
    def get_html(self):
        return self.env.ref('stadia.manpower_report_template')._render({})

    @api.model
    def _get_report_data(self, date_from, date_to):
        hired_report = []
        promoted_report = []
        transfered_report = []
        if date_from and date_to:
