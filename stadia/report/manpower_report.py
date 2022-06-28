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
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = data['form']['date_to']
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

        # Get the employees from contract id

        employees = self.sudo().env['hr.employee'].search([('contract_id', '!=', False)])

        sheet.write(0, 0, 'Name of Employe', bold)
        sheet.write(0, 1, 'Position', bold)
        sheet.write(0, 2, 'Basic Salary', bold)
        sheet.write(0, 3, 'Perdime', bold)
        sheet.write(0, 4, 'Desert Allowance', bold)
        sheet.write(0, 5, 'Project', bold)
        sheet.write(0, 6, 'Date of Hired', bold)

        col = 1
        for employee in employees:             
            ## TODO: improve efficiency
            if(not employee.first_contract_date):
                continue
            print('999999999999999999999999')
            print(employee.first_contract_date)
            if(employee.first_contract_date >= start_date and employee.first_contract_date <= end_date):
                sheet.write(col, 0, employee.name)
                sheet.write(col, 1, employee.job_id.name)
                sheet.write(col, 2, employee.contract_id.wage)
                sheet.write(col, 3, employee.contract_id.perdime)
                sheet.write(col, 4, '')
                sheet.write(col, 5, employee.contract_id.work_place_id.name)
                sheet.write(col, 6, employee.first_contract_date.strftime('%m/%d/%Y'))
                col += 1