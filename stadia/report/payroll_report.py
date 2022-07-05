import math
from odoo import api, models
from datetime import datetime, time, timedelta
from xlsxwriter.utility import xl_rowcol_to_cell

class AttendacneReport(models.AbstractModel):
    _name = 'report.stadia.payroll_report'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, partners):
        sheet = workbook.add_worksheet()

        bold = workbook.add_format({'bold': True})
        bold.set_border(style=1)
        border = workbook.add_format()
        border.set_border(style=1)
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

        max_col = 9
        max_row = 3
        left_cols = math.floor(max_col * 0.25)
        center_cols = math.ceil(max_col * 0.5)
        right_cols = math.floor(max_col * 0.25)

        sheet.merge_range(0, 0, 0, left_cols - 1, '', header_format)
        sheet.merge_range(1, 0, 0, left_cols - 1, '', header_format)
        sheet.merge_range(2, 0, 0, left_cols - 1, '', header_format)
        sheet.merge_range(0, left_cols, 0, max_col, 'ስታድያ የምህንድስና ስራዎች ኃላ/የተ/የግ/ማህበር', header_format)
        sheet.merge_range(1, left_cols, 1, max_col, 'STADIA Engineering Works Consultant PLC', header_format)
        sheet.merge_range(2, left_cols, 2, max_col - right_cols, 'EMPLOYMENT, TRANSFER, TERMINATION REPORT', header_format)
        sheet.set_row(2, 50)
        sheet.merge_range(2, max_col - right_cols + 1, 2, max_col, 'Date:- %s - %s' % ('', ''), date_format)

        payslip_ids = data['context']['active_ids']

        sheet.write(max_row + 2, 0, 'No', bold)
        sheet.write(max_row + 2, 1, 'Name of Employee', bold)
        sheet.write(max_row + 2, 2, 'Postion', bold)
        sheet.write(max_row + 2, 3, 'No. Of  working days', bold)
        sheet.write(max_row + 2, 4, 'Basic salary', bold)
        sheet.write(max_row + 2, 5, 'Transport  Allowance', bold)
        sheet.write(max_row + 2, 6, 'Additional Per Diem', bold)
        sheet.write(max_row + 2, 7, 'Over time', bold)
        sheet.write(max_row + 2, 8, 'Gross salary', bold)
        sheet.write(max_row + 2, 9, 'Taxable Income', bold)
        sheet.write(max_row + 2, 10, 'Pension contribution from employee 7%', bold)
        sheet.write(max_row + 2, 11, 'Absent', bold)
        sheet.write(max_row + 2, 12, 'Other', bold)
        sheet.write(max_row + 2, 13, 'Total Deductions', bold)
        sheet.write(max_row + 2, 14, 'Net Pay', bold)
        sheet.write(max_row + 2, 15, 'Pension contribution from employer 11%', bold)
        sheet.write(max_row + 2, 16, 'Sign.', bold)

        # Sizes
        sheet.set_row(max_row + 2, max_row + 2, 50)
        sheet.set_column(0, 0, 5)
        sheet.set_column(1, 1, 20)
        sheet.set_column(2, 2, 20)
        sheet.set_column(3, 3, 5)
        sheet.set_column(4, 4, 10)
        sheet.set_column(5, 5, 10)
        sheet.set_column(6, 6, 10)
        sheet.set_column(7, 7, 10)
        sheet.set_column(8, 8, 10)
        sheet.set_column(9, 9, 10)
        sheet.set_column(10, 10, 10)
        sheet.set_column(11, 11, 10)
        sheet.set_column(12, 12, 10)
        sheet.set_column(13, 13, 10)
        sheet.set_column(14, 14, 10)
        sheet.set_column(15, 15, 10)
        sheet.set_column(16, 16, 5)

        row = max_row + 2
        c = 1
        for payslip_id in payslip_ids:
            payslip = self.env['hr.payslip'].search([('id', '=', payslip_id)])

            sheet.write(row, 0, c, border)
            sheet.write(row, 1, payslip.employee_id.name, border)
            sheet.write(row, 2, payslip.contract_id.job_id.name, border)
            sheet.write(row, 3, payslip.contract_id.job_id.name, border)

            work100 = 0
            ov_amount = 0

            for line in payslip.worked_days_line_ids:
                work100 += line.number_of_days
                

            for line in payslip.input_line_ids:
                if(line.code == 'OV'):
                    ov_amount = line.number_of_days

            sheet.write(row, 4, work100, border)
            sheet.write(row, 5, payslip.contract_id.wage, border)
            sheet.write(row, 5, payslip.contract_id.transport_allowance, border)
            sheet.write(row, 5, payslip.contract_id.perdime, border)
            sheet.write(row, 6, ov_amount, border)
            
            row += 1
            c += 1