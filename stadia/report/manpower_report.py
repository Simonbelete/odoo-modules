from odoo import api, fields, models
from datetime import datetime

class ManpowerReport(models.AbstractModel):
    _name = 'report.stadia.hired_manpower_report'
    _inherit = 'report.report_xlsx.abstract'
    
    @api.model
    def get_html(self, date_from, date_to):
        data = self._get_report_data(date_from, date_to)
        return self.env.ref('stadia.manpower_report_template')._render(data)

    def generate_xlsx_report(self, workbook, data, partners):
        sheet = workbook.add_worksheet()

        # Set up some formats to use.
        bold = workbook.add_format({'bold': True})

        start_date = data['form']['date_from']
        end_date = data['form']['date_to']

        employees = self.env['hr.employee'].search([])

        sheet.write(0, 0, 'Name of Employe', bold)
        sheet.write(0, 1, 'Position', bold)
        sheet.write(0, 2, 'Basic Salary', bold)
        sheet.write(0, 3, 'Perdime', bold)
        sheet.write(0, 4, 'Desert Allowance', bold)
        sheet.write(0, 5, 'Project', bold)
        sheet.write(0, 6, 'Date of Hired', bold)

        col = 1
        for employee in employees:
            sheet.write(col, 0, employee.name)
            sheet.write(col, 1, employee.job_id.name)
            sheet.write(col, 2, employee.contract_id.wage)
            sheet.write(col, 3, employee.contract_id.perdime)
            sheet.write(col, 4, '')
            sheet.write(col, 5, employee.contract_id.work_place_id.name)
            col += 1


    # @api.model
    # def _get_report_data(self, date_from, date_to):
    #     new_hired_data = []
    #     promotion_data = []
    #     transfer_data = []
    #     if (date_from and date_to):
    #         start_date = datetime.now() #datetime.strptime(date_from, '%Y-%m-%d').date()
    #         end_date = datetime.strptime(date_to, '%Y-%m-%d').date()
    #         new_hired_data = self.env['hr.employee'].search([])
    #         # i.e contract signed stage
    #         last_stage_id = self.env['stadia.promotion.stage'].search([])
    #         last_stage_id = max(last_stage_id.mapped('sequence'))
    #         promotion_data = self.env['stadia.promotion'].search([('id', '=', last_stage_id), ('promotion_type', '=', 'promotion')])
    #         transfer_data = self.env['stadia.promotion'].search([('id', '=', last_stage_id), ('promotion_type', '=', 'transfer')])
            
    #     return {
    #         'hired': new_hired_data,
    #         'promoted': promotion_data,
    #         'transfer': transfer_data
    #     }