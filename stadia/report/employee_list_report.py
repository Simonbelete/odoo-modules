from odoo import api, models
import os
import math

class EmployeeListReport(models.AbstractModel):
    _name = 'report.stadia.employees_list_report'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, partners):
        sheet = workbook.add_worksheet()

        bold = workbook.add_format({'bold': True})

        employee_ids = data['context']['active_ids']

        header_format = workbook.add_format()
        header_format.set_font_size(15)
        header_format.set_bold()
        header_format.set_align('center')
        header_format.set_align('vcenter')
        header_format.set_border(style=1)
        date_format = workbook.add_format()
        date_format.set_font_size(10)
        date_format.set_bold()
        date_format.set_align('center')
        date_format.set_align('vcenter')
        date_format.set_border(style=1)

        max_col = 18
        max_row = 3
        left_cols = math.floor(max_col * 0.25)
        center_cols = math.ceil(max_col * 0.5)
        right_cols = math.floor(max_col * 0.25)

        dir_path = os.path.dirname(os.path.realpath(__file__))

        sheet.merge_range(0, 0, 0, left_cols - 1, '', header_format)
        sheet.merge_range(1, 0, 0, left_cols - 1, '', header_format)
        sheet.merge_range(2, 0, 0, left_cols - 1, '', header_format)
        sheet.insert_image(0, 0, '%s/stadia_plain_logo.png' % dir_path, {'x_scale': 0.6, 'y_scale': 0.4})
        sheet.merge_range(0, left_cols, 0, max_col, 'ስታድያ የምህንድስና ስራዎች ኃላ/የተ/የግ/ማህበር', header_format)
        sheet.merge_range(1, left_cols, 1, max_col, 'STADIA Engineering Works Consultant PLC', header_format)
        sheet.merge_range(2, left_cols, 2, max_col - right_cols, 'Hired Report', header_format)
        sheet.set_row(2, 50)
        sheet.merge_range(2, max_col - right_cols + 1, 2, max_col, '', date_format)

        sheet.write(max_row + 1, 0, 'No', bold)
        sheet.write(max_row + 1, 1, 'Name of Employee', bold)
        sheet.write(max_row + 1, 2, 'ID', bold)
        sheet.write(max_row + 1, 3, 'Department', bold)
        sheet.write(max_row + 1, 4, 'Project', bold)
        sheet.write(max_row + 1, 5, 'Postion', bold)
        sheet.write(max_row + 1, 6, 'Date of Employement', bold)
        sheet.write(max_row + 1, 7, 'Mobile', bold)
        sheet.write(max_row + 1, 8, 'Email', bold)
        sheet.write(max_row + 1, 9, 'Sub City', bold)
        sheet.write(max_row + 1, 10, 'Woreda', bold)
        sheet.write(max_row + 1, 11, 'Tin Number', bold)
        sheet.write(max_row + 1, 12, 'Pension Number', bold)
        sheet.write(max_row + 1, 13, 'Bank Account Number', bold)
        sheet.write(max_row + 1, 14, 'Gender', bold)
        sheet.write(max_row + 1, 15, 'Marital Status', bold)
        sheet.write(max_row + 1, 16, 'Date of Birth', bold)
        sheet.write(max_row + 1, 17, 'Nationality', bold)
        sheet.write(max_row + 1, 18, 'PIN Code', bold)

        sheet.set_column(0, 0,  5)
        sheet.set_column(1, 1,  30)
        sheet.set_column(2, 2,  20)
        sheet.set_column(3, 3,  20)
        sheet.set_column(4, 4,  20)
        sheet.set_column(5, 5,  20)
        sheet.set_column(6, 6,  20)
        sheet.set_column(7, 7,  20)
        sheet.set_column(8, 8,  20)
        sheet.set_column(9, 9,  20)
        sheet.set_column(10, 10,  20)
        sheet.set_column(11, 11,  20)
        sheet.set_column(12, 12,  20)
        sheet.set_column(13, 13,  20)
        sheet.set_column(14, 14,  20)
        sheet.set_column(15, 15,  20)
        sheet.set_column(16, 16,  20)
        sheet.set_column(17, 17,  20)
        sheet.set_column(18, 18,  20)

        row = max_row + 2
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
            if(employee.birthday):
                sheet.write(row, 16, employee.birthday.strftime('%m/%d/%Y'))
            else:
                sheet.write(row, 16, '')
            sheet.write(row, 17, employee.country_id.name)
            sheet.write(row, 18, employee.pin)
            row += 1
            c += 1
            