import math
from odoo import api, models
from datetime import datetime, time, timedelta
from xlsxwriter.utility import xl_rowcol_to_cell

class AttendacneReport(models.AbstractModel):
    _name = 'report.stadia.payroll_report'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, partners):
        sheet = workbook.add_worksheet()

        bold = workbook.add_format({'bold': True, 'text_wrap': True})
        bold.set_border(style=2)
        bold.set_rotation(90)
        bold.set_align('center')
        bold.set_align('vcenter')
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
        sheet.write(max_row + 2, 12, 'Loan', bold)
        sheet.write(max_row + 2, 13, 'Other', bold)
        sheet.write(max_row + 2, 14, 'Total Deductions', bold)
        sheet.write(max_row + 2, 15, 'Net Pay', bold)
        sheet.write(max_row + 2, 16, 'Pension contribution from employer 11%', bold)
        sheet.write(max_row + 2, 17, 'Sign.', bold)

        # Sizes
        sheet.set_row(max_row + 2, 120)
        sheet.set_column(0, 0, 5)
        sheet.set_column(1, 1, 25)
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

        row = max_row + 3
        c = 1
        for payslip_id in payslip_ids:
            payslip = self.env['hr.payslip'].search([('id', '=', payslip_id)])

            sheet.write(row, 0, c, border)
            sheet.write(row, 1, payslip.employee_id.name, border)
            sheet.write(row, 2, payslip.contract_id.job_id.name, border)

            work100 = 0
            ov_amount = 0
            basic_amount = 0
            gross_amount = 0
            transport_allowance_amount = 0
            perdime_amount = 0
            pension_amount = 0
            other_amount = 0
            total_deducation = 0
            net_amount = 0
            taxable_income = 0
            loan_amount = 0

            for line in payslip.worked_days_line_ids:
                work100 += line.number_of_days
                
            for line in payslip.input_line_ids:
                if(line.code == 'OV'):
                    ov_amount = line.number_of_days

            for line in payslip.line_ids:
                if(line.code == 'BASIC'):
                    basic_amount = line.amount
                if(line.code == 'TRA'):
                    transport_allowance_amount = line.amount
                if(line.code == 'PD'):
                    perdime_amount = line.amount
                if(line.code == 'PE'):
                    pension_amount = line.amount
                if(line.code == 'OT'):
                    other_amount = line.amount
                if(line.code == 'NET'):
                    net_amount = line.amount
                if(line.code == 'TI'):
                    taxable_income = line.amount
                if(line.code == 'LO'):
                    loan_amount = line.amount
            # Calc
            gross_amount = basic_amount + transport_allowance_amount + perdime_amount
            total_deducation = payslip.tax_dec + pension_amount + other_amount + loan_amount

            sheet.write(row, 3, work100, border)
            sheet.write(row, 4, basic_amount, border)
            sheet.write(row, 5, transport_allowance_amount, border)
            sheet.write(row, 6, perdime_amount, border)
            sheet.write(row, 7, ov_amount, border)
            sheet.write(row, 8, gross_amount, border)
            sheet.write(row, 9, taxable_income, border)
            sheet.write(row, 10, payslip.tax_dec, border)
            sheet.write(row, 11, '', border)
            sheet.write(row, 12, loan_amount, border)
            sheet.write(row, 13, other_amount, border)
            sheet.write(row, 14, total_deducation, border)
            sheet.write(row, 15, net_amount, border)
            f = '=%s*0.11' % (xl_rowcol_to_cell(row, 4))
            sheet.write_formula(row, 16, f, border, '')
            sheet.write(row, 15, '', border)
            
            row += 1
            c += 1