from odoo import api, fields, models
from datetime import datetime

class ManpowerReport(models.AbstractModel):
    _name = 'report.stadia.manpower_report'
    
    @api.model
    def get_html(self, date_from, date_to):
        data = self._get_report_data(date_from, date_to)
        return self.env.ref('stadia.manpower_report_template')._render(data)

    @api.model
    def _get_report_data(self, date_from, date_to):
        new_hired_data = []
        promotion_data = []
        transfer_data = []
        if (date_from and date_to):
            start_date = datetime.now() #datetime.strptime(date_from, '%Y-%m-%d').date()
            end_date = datetime.strptime(date_to, '%Y-%m-%d').date()
            new_hired_data = self.env['hr.employee'].search([])
            # i.e contract signed stage
            last_stage_id = self.env['stadia.promotion.stage'].search([])
            last_stage_id = max(last_stage_id.mapped('sequence'))
            promotion_data = self.env['stadia.promotion'].search([('id', '=', last_stage_id), ('promotion_type', '=', 'promotion')])
            transfer_data = self.env['stadia.promotion'].search([('id', '=', last_stage_id), ('promotion_type', '=', 'transfer')])
            
        return {
            'hired': new_hired_data,
            'promoted': promotion_data,
            'transfer': transfer_data
        }