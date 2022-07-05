import math
import os 
from odoo import api, models
from datetime import datetime, time, timedelta
from xlsxwriter.utility import xl_rowcol_to_cell

class PayrollRepot(models.AbstractModel):
    _name = 'report.stadia.payroll_report'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, partners):
        sheet = workbook.add_worksheet()

        dir_path = os.path.dirname(os.path.realpath(__file__))

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

        max_col = 18
        max_row = 3
        left_cols = math.floor(max_col * 0.25)
        center_cols = math.ceil(max_col * 0.5)
        right_cols = math.floor(max_col * 0.25)

        sheet.merge_range(0, 0, 0, left_cols - 1, '', header_format)
        sheet.merge_range(1, 0, 0, left_cols - 1, '', header_format)
        sheet.merge_range(2, 0, 0, left_cols - 1, '', header_format)
        sheet.insert_image(0, 0, '%s/stadia_plain_logo.png' % dir_path, {'x_scale': 0.6, 'y_scale': 0.4})
        sheet.merge_range(0, left_cols, 0, max_col, 'ስታድያ የምህንድስና ስራዎች ኃላ/የተ/የግ/ማህበር', header_format)
        sheet.merge_range(1, left_cols, 1, max_col, 'STADIA Engineering Works Consultant PLC', header_format)
        sheet.merge_range(2, left_cols, 2, max_col - right_cols, 'EMPLOYMENT, TRANSFER, TERMINATION REPORT', header_format)
        sheet.set_row(2, 50)
        sheet.merge_range(2, max_col - right_cols + 1, 2, max_col, '', date_format)

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
        sheet.write(max_row + 2, 10, 'Income Tax', bold)
        sheet.write(max_row + 2, 11, 'Pension contribution from employee 7%', bold)
        sheet.write(max_row + 2, 12, 'Absent', bold)
        sheet.write(max_row + 2, 13, 'Loan', bold)
        sheet.write(max_row + 2, 14, 'Other', bold)
        sheet.write(max_row + 2, 15, 'Total Deductions', bold)
        sheet.write(max_row + 2, 16, 'Net Pay', bold)
        sheet.write(max_row + 2, 17, 'Pension contribution from employer 11%', bold)
        sheet.write(max_row + 2, 18, 'Sign.', bold)

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
        sheet.set_column(16, 16, 10)
        sheet.set_column(16, 17, 10)
        sheet.set_column(16, 16, 5)

        row = max_row + 3
        start_row = row
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

            # positive
            pension_amount = abs(pension_amount)

            # Calc
            gross_amount = basic_amount + transport_allowance_amount + perdime_amount
            total_deducation = abs(payslip.tax_dec) + abs(payslip.tax_dec) + abs(pension_amount) + abs(other_amount) + abs(loan_amount)

            sheet.write(row, 3, work100, border)
            sheet.write(row, 4, basic_amount, border)
            sheet.write(row, 5, transport_allowance_amount, border)
            sheet.write(row, 6, perdime_amount, border)
            sheet.write(row, 7, ov_amount, border)
            sheet.write(row, 8, gross_amount, border)
            sheet.write(row, 9, taxable_income, border)
            sheet.write(row, 10, payslip.tax_dec, border)
            sheet.write(row, 11, pension_amount, border)
            sheet.write(row, 12, '', border)
            sheet.write(row, 13, loan_amount, border)
            sheet.write(row, 14, other_amount, border)
            sheet.write(row, 15, total_deducation, border)
            sheet.write(row, 16, net_amount, border)
            f = '=%s*0.11' % (xl_rowcol_to_cell(row, 4))
            sheet.write_formula(row, 17, f, border, '')
            sheet.write(row, 18, '', border)
            
            row += 1
            c += 1

        sheet.merge_range(row, 0, row, 3, 'Total', border)
        f = '=SUM(%s:%s)' % (xl_rowcol_to_cell(start_row, 4), xl_rowcol_to_cell(row - 1, 4))
        sheet.write_formula(row, 4, f, border, '')

        f = '=SUM(%s:%s)' % (xl_rowcol_to_cell(start_row, 5), xl_rowcol_to_cell(row - 1, 5))
        sheet.write_formula(row, 5, f, border, '')

        f = '=SUM(%s:%s)' % (xl_rowcol_to_cell(start_row, 6), xl_rowcol_to_cell(row - 1, 6))
        sheet.write_formula(row, 6, f, border, '')

        f = '=SUM(%s:%s)' % (xl_rowcol_to_cell(start_row, 7), xl_rowcol_to_cell(row - 1, 7))
        sheet.write_formula(row, 7, f, border, '')

        f = '=SUM(%s:%s)' % (xl_rowcol_to_cell(start_row, 8), xl_rowcol_to_cell(row - 1, 8))
        sheet.write_formula(row, 8, f, border, '')

        f = '=SUM(%s:%s)' % (xl_rowcol_to_cell(start_row, 9), xl_rowcol_to_cell(row - 1, 9))
        sheet.write_formula(row, 9, f, border, '')

        f = '=SUM(%s:%s)' % (xl_rowcol_to_cell(start_row, 10), xl_rowcol_to_cell(row - 1, 10))
        sheet.write_formula(row, 10, f, border, '')

        f = '=SUM(%s:%s)' % (xl_rowcol_to_cell(start_row, 11), xl_rowcol_to_cell(row - 1, 11))
        sheet.write_formula(row, 11, f, border, '')

        f = '=SUM(%s:%s)' % (xl_rowcol_to_cell(start_row, 12), xl_rowcol_to_cell(row - 1, 12))
        sheet.write_formula(row, 12, f, border, '')

        f = '=SUM(%s:%s)' % (xl_rowcol_to_cell(start_row, 13), xl_rowcol_to_cell(row - 1, 13))
        sheet.write_formula(row, 13, f, border, '')

        f = '=SUM(%s:%s)' % (xl_rowcol_to_cell(start_row, 14), xl_rowcol_to_cell(row - 1, 14))
        sheet.write_formula(row, 14, f, border, '')

        f = '=SUM(%s:%s)' % (xl_rowcol_to_cell(start_row, 15), xl_rowcol_to_cell(row - 1, 15))
        sheet.write_formula(row, 15, f, border, '')

        f = '=SUM(%s:%s)' % (xl_rowcol_to_cell(start_row, 16), xl_rowcol_to_cell(row - 1, 16))
        sheet.write_formula(row, 16, f, border, '')

        f = '=SUM(%s:%s)' % (xl_rowcol_to_cell(start_row, 17), xl_rowcol_to_cell(row - 1, 17))
        sheet.write_formula(row, 17, f, border, '')

        sheet.write(row, 18, '', border)


class PayrollRepotRun(models.AbstractModel):
    _name = 'report.stadia.payroll_report_run'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, partners):
        sheet = workbook.add_worksheet()

        dir_path = os.path.dirname(os.path.realpath(__file__))

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

        max_col = 18
        max_row = 3
        left_cols = math.floor(max_col * 0.25)
        center_cols = math.ceil(max_col * 0.5)
        right_cols = math.floor(max_col * 0.25)

        payslip_id = data['context']['active_id']
        batch_payslip = self.env['hr.payslip.run'].search([('id', '=', payslip_id)])

        sheet.merge_range(0, 0, 0, left_cols - 1, '', header_format)
        sheet.merge_range(1, 0, 0, left_cols - 1, '', header_format)
        sheet.merge_range(2, 0, 0, left_cols - 1, '', header_format)
        sheet.insert_image(0, 0, '%s/stadia_plain_logo.png' % dir_path, {'x_scale': 0.6, 'y_scale': 0.4})
        sheet.merge_range(0, left_cols, 0, max_col, 'ስታድያ የምህንድስና ስራዎች ኃላ/የተ/የግ/ማህበር', header_format)
        sheet.merge_range(1, left_cols, 1, max_col, 'STADIA Engineering Works Consultant PLC', header_format)
        sheet.merge_range(2, left_cols, 2, max_col - right_cols, 'EMPLOYMENT, TRANSFER, TERMINATION REPORT', header_format)
        sheet.set_row(2, 50)
        sheet.merge_range(2, max_col - right_cols + 1, 2, max_col, 'Date:- %s - %s' % (batch_payslip.date_start.strftime('%m/%d/%Y'), batch_payslip.date_end.strftime('%m/%d/%Y')), date_format)

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
        sheet.write(max_row + 2, 10, 'Income Tax', bold)
        sheet.write(max_row + 2, 11, 'Pension contribution from employee 7%', bold)
        sheet.write(max_row + 2, 12, 'Absent', bold)
        sheet.write(max_row + 2, 13, 'Loan', bold)
        sheet.write(max_row + 2, 14, 'Other', bold)
        sheet.write(max_row + 2, 15, 'Total Deductions', bold)
        sheet.write(max_row + 2, 16, 'Net Pay', bold)
        sheet.write(max_row + 2, 17, 'Pension contribution from employer 11%', bold)
        sheet.write(max_row + 2, 18, 'Sign.', bold)

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
        sheet.set_column(16, 16, 10)
        sheet.set_column(16, 17, 10)
        sheet.set_column(16, 16, 5)

        row = max_row + 3
        start_row = row
        c = 1
        for payslip in batch_payslip.slip_ids:

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

            # positive
            pension_amount = abs(pension_amount)

            # Calc
            gross_amount = basic_amount + transport_allowance_amount + perdime_amount
            total_deducation = abs(payslip.tax_dec) + abs(payslip.tax_dec) + abs(pension_amount) + abs(other_amount) + abs(loan_amount)

            sheet.write(row, 3, work100, border)
            sheet.write(row, 4, basic_amount, border)
            sheet.write(row, 5, transport_allowance_amount, border)
            sheet.write(row, 6, perdime_amount, border)
            sheet.write(row, 7, ov_amount, border)
            sheet.write(row, 8, gross_amount, border)
            sheet.write(row, 9, taxable_income, border)
            sheet.write(row, 10, payslip.tax_dec, border)
            sheet.write(row, 11, pension_amount, border)
            sheet.write(row, 12, '', border)
            sheet.write(row, 13, loan_amount, border)
            sheet.write(row, 14, other_amount, border)
            sheet.write(row, 15, total_deducation, border)
            sheet.write(row, 16, net_amount, border)
            f = '=%s*0.11' % (xl_rowcol_to_cell(row, 4))
            sheet.write_formula(row, 17, f, border, '')
            sheet.write(row, 18, '', border)
            
            row += 1
            c += 1

        sheet.merge_range(row, 0, row, 3, 'Total', border)
        f = '=SUM(%s:%s)' % (xl_rowcol_to_cell(start_row, 4), xl_rowcol_to_cell(row - 1, 4))
        sheet.write_formula(row, 4, f, border, '')

        f = '=SUM(%s:%s)' % (xl_rowcol_to_cell(start_row, 5), xl_rowcol_to_cell(row - 1, 5))
        sheet.write_formula(row, 5, f, border, '')

        f = '=SUM(%s:%s)' % (xl_rowcol_to_cell(start_row, 6), xl_rowcol_to_cell(row - 1, 6))
        sheet.write_formula(row, 6, f, border, '')

        f = '=SUM(%s:%s)' % (xl_rowcol_to_cell(start_row, 7), xl_rowcol_to_cell(row - 1, 7))
        sheet.write_formula(row, 7, f, border, '')

        f = '=SUM(%s:%s)' % (xl_rowcol_to_cell(start_row, 8), xl_rowcol_to_cell(row - 1, 8))
        sheet.write_formula(row, 8, f, border, '')

        f = '=SUM(%s:%s)' % (xl_rowcol_to_cell(start_row, 9), xl_rowcol_to_cell(row - 1, 9))
        sheet.write_formula(row, 9, f, border, '')

        f = '=SUM(%s:%s)' % (xl_rowcol_to_cell(start_row, 10), xl_rowcol_to_cell(row - 1, 10))
        sheet.write_formula(row, 10, f, border, '')

        f = '=SUM(%s:%s)' % (xl_rowcol_to_cell(start_row, 11), xl_rowcol_to_cell(row - 1, 11))
        sheet.write_formula(row, 11, f, border, '')

        f = '=SUM(%s:%s)' % (xl_rowcol_to_cell(start_row, 12), xl_rowcol_to_cell(row - 1, 12))
        sheet.write_formula(row, 12, f, border, '')

        f = '=SUM(%s:%s)' % (xl_rowcol_to_cell(start_row, 13), xl_rowcol_to_cell(row - 1, 13))
        sheet.write_formula(row, 13, f, border, '')

        f = '=SUM(%s:%s)' % (xl_rowcol_to_cell(start_row, 14), xl_rowcol_to_cell(row - 1, 14))
        sheet.write_formula(row, 14, f, border, '')

        f = '=SUM(%s:%s)' % (xl_rowcol_to_cell(start_row, 15), xl_rowcol_to_cell(row - 1, 15))
        sheet.write_formula(row, 15, f, border, '')

        f = '=SUM(%s:%s)' % (xl_rowcol_to_cell(start_row, 16), xl_rowcol_to_cell(row - 1, 16))
        sheet.write_formula(row, 16, f, border, '')

        f = '=SUM(%s:%s)' % (xl_rowcol_to_cell(start_row, 17), xl_rowcol_to_cell(row - 1, 17))
        sheet.write_formula(row, 17, f, border, '')

        sheet.write(row, 18, '', border)