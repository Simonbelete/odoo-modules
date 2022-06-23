from odoo import api, fields, models

class ManpowerReport(models.AbstractModel):
    _name = 'report.stadia.manpower_report'
    
    @api.model
    def get_html(self):
        return self.env.ref('stadia.manpower_report_template')._render({})
