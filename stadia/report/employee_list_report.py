from odoo import api, models

class EmployeeListReport(models.AbstractModel):
    _name = 'report.stadia.employees_list_report'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, partners):
        sheet = workbook.add_worksheet()

        bold = workbook.add_format({'bold': True})

        employee_ids = data['context']['active_ids']

        sheet.write(0, 0, 'No', bold)
        sheet.write(0, 1, 'Name of Employee', bold)
        sheet.write(0, 2, 'ID', bold)
        sheet.write(0, 3, 'Department', bold)
        sheet.write(0, 4, 'Project', bold)
        sheet.write(0, 5, 'Postion', bold)
        sheet.write(0, 6, 'Date of Employement', bold)
        sheet.write(0, 7, 'Mobile', bold)
        sheet.write(0, 8, 'Email', bold)
        sheet.write(0, 9, 'Sub City', bold)
        sheet.write(0, 10, 'Woreda', bold)
        sheet.write(0, 11, 'Tin Number', bold)
        sheet.write(0, 12, 'Pension Number', bold)
        sheet.write(0, 13, 'Bank Account Number', bold)
        sheet.write(0, 14, 'Gender', bold)
        sheet.write(0, 15, 'Marital Status', bold)
        sheet.write(0, 16, 'Date of Birth', bold)
        sheet.write(0, 17, 'Nationality', bold)
        sheet.write(0, 18, 'PIN Code', bold)

        sheet.set_column(0, 0,  5)
        sheet.set_column(0, 1,  30)
        sheet.set_column(0, 2,  20)
        sheet.set_column(0, 3,  20)
        sheet.set_column(0, 4,  20)
        sheet.set_column(0, 5,  20)
        sheet.set_column(0, 6,  20)
        sheet.set_column(0, 7,  20)
        sheet.set_column(0, 8,  20)
        sheet.set_column(0, 9,  20)
        sheet.set_column(0, 10,  20)
        sheet.set_column(0, 11,  20)
        sheet.set_column(0, 12,  20)
        sheet.set_column(0, 13,  20)
        sheet.set_column(0, 14,  20)
        sheet.set_column(0, 15,  20)
        sheet.set_column(0, 16,  20)
        sheet.set_column(0, 17,  20)
        sheet.set_column(0, 18,  20)

        row = 1
        c = 1
        for employee_id in employee_ids:
            employee = self.env['hr.employee'].search([('id', '=', employee_id)])
            sheet.write(row, 0, c)
            sheet.write(row, 1, employee.name)
            sheet.write(row, 2, employee.badge_id_no)
            sheet.write(row, 3, employee.department_id.name)
            sheet.write(row, 4, employee.job_id.name)
            if(employee.first_contract_date):
                sheet.write(row, 5, employee.first_contract_date.strftime('%m/%d/%Y'))
            else:
                sheet.write(row, 5, '')
            sheet.write(row, 6, employee.mobile_phone)
            sheet.write(row, 7, employee.work_email)
            sheet.write(row, 8, employee.sub_city_id.name)
            sheet.write(row, 9, employee.woreda)
            sheet.write(row, 10, employee.house_number)
            sheet.write(row, 11, employee.tin_no)
            sheet.write(row, 12, employee.pension_no)
            sheet.write(row, 13, employee.bank_account_id.acc_number)
            sheet.write(row, 14, employee.gender)
            sheet.write(row, 15, employee.marital)
            sheet.write(row, 16, employee.birthday)
            sheet.write(row, 17, employee.country_id.name)
            sheet.write(row, 18, employee.pin)
            row += 1
            c += 1
            