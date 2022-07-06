import os
import math
from odoo import api, models
from datetime import datetime, time, timedelta
from xlsxwriter.utility import xl_rowcol_to_cell

class AttendacneReport(models.AbstractModel):
    _name = 'report.stadia.attendance_report'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, partners):
        sheet = workbook.add_worksheet()

        bold = workbook.add_format({'bold': True})
        yellow = workbook.add_format({'bg_color': '#FCD5B5'})
        yellow.set_border(style=1)
        center = workbook.add_format()
        center.set_align('center')
        center.set_align('vcenter')
        center.set_border(style=1)
        border = workbook.add_format()
        border.set_border(style=1)
        table_header_format = workbook.add_format()
        table_header_format.set_align('center')
        table_header_format.set_align('vcenter')
        table_header_format.set_bold()
        table_header_format.set_font_size(13)
        table_header_format.set_border(style=1)
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

        employee_ids = data['form']['emp']
        start_date = datetime.strptime(data['form']['date_from'], '%Y-%m-%d').date()
        end_date = datetime.strptime(data['form']['date_to'], '%Y-%m-%d').date()

        total_row = len(employee_ids) + 3
        total_col = (end_date - start_date).days

        dir_path = os.path.dirname(os.path.realpath(__file__))
        
        # Header
        max_col = total_col + 8
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
        sheet.merge_range(2, left_cols, 2, max_col - right_cols, 'Attendance Sheet', header_format)
        sheet.set_row(2, 50)
        sheet.merge_range(2, max_col - right_cols + 1, 2, max_col, 'Date:- %s - %s' % (start_date.strftime('%m/%d/%Y'), end_date.strftime('%m/%d/%Y')), date_format)
        # sheet.write(2, max_col - right_cols + 1, 'Date:- %s - %s' % (start_date.strftime('%m/%d/%Y'), end_date.strftime('%m/%d/%Y')), date_format)

        # Logo Header
        # header_row = 5
        # half_row = abs(int((total_row - 13)/2))
        
        # sheet.merge_range(0, half_row, 0, half_row + 15, 'Stadia Engineering Works Consultant Plc', header_format)

        # Tables header
        table_start_row = max_row + 1
        sheet.merge_range(table_start_row, 0, table_start_row + 2, 0, 'S.No', table_header_format)
        sheet.merge_range(table_start_row, 1, table_start_row + 2, 1, 'Name', table_header_format)
        sheet.merge_range(table_start_row , total_col + 3, table_start_row, total_col + 8, 'Total', table_header_format)
        sheet.write(table_start_row + 1, total_col + 3, 'P', center)
        sheet.write(table_start_row + 1, total_col + 4, 'S', center)
        sheet.write(table_start_row + 1, total_col + 5, 'T', center)
        sheet.write(table_start_row + 1, total_col + 6, 'L', center)
        sheet.write(table_start_row + 1, total_col + 7, 'A', center)
        sheet.write(table_start_row + 1, total_col + 8, 'Total', center)

        # Sizes
        sheet.set_column(0, 0, 5)
        sheet.set_column(1, 1, 20)
        sheet.set_column(total_col + 3, total_col + 3, 5)
        sheet.set_column(total_col + 4, total_col + 4, 5)
        sheet.set_column(total_col + 5, total_col + 5, 5)
        sheet.set_column(total_col + 6, total_col + 6, 5)
        sheet.set_column(total_col + 7, total_col + 7, 5)
        sheet.set_column(total_col + 8, total_col + 8, 5)

        data_start_row = table_start_row + 3
        col = data_start_row
        # Write Headers
        is_header_written = False
        for emp_id in employee_ids:
            employee = self.env['hr.employee'].search([('id', '=', emp_id)])
            delta = timedelta(days=1)
            date_start = start_date

            sheet.write(col, 0, col - data_start_row + 1, border)
            sheet.write(col, 1, employee.name, border)
            f = '=COUNTIF(%s:%s,%s)' % (xl_rowcol_to_cell(col, 2), xl_rowcol_to_cell(col, total_col + 2) , xl_rowcol_to_cell(table_start_row + 1, total_col + 3))
            sheet.write_formula(col, total_col + 3, f, border, '')
            f = '=COUNTIF(%s:%s,%s)' % (xl_rowcol_to_cell(col, 2), xl_rowcol_to_cell(col, total_col + 2) , xl_rowcol_to_cell(table_start_row + 1, total_col + 4))
            sheet.write_formula(col, total_col + 4, f, border, '')
            f = '=COUNTIF(%s:%s,%s)' % (xl_rowcol_to_cell(col, 2), xl_rowcol_to_cell(col, total_col + 2) , xl_rowcol_to_cell(table_start_row + 1, total_col + 5))
            sheet.write_formula(col, total_col + 5, f, border, '')
            f = '=COUNTIF(%s:%s,%s)' % (xl_rowcol_to_cell(col, 2), xl_rowcol_to_cell(col, total_col + 2) , xl_rowcol_to_cell(table_start_row + 1, total_col + 6))
            sheet.write_formula(col, total_col + 6, f, border, '')
            f = '=COUNTIF(%s:%s,%s)' % (xl_rowcol_to_cell(col, 2), xl_rowcol_to_cell(col, total_col + 2), xl_rowcol_to_cell(table_start_row + 1, total_col + 7))
            sheet.write_formula(col, total_col + 7, f, border, '')
            f = '=COUNTA(%s:%s)' % (xl_rowcol_to_cell(col, 2), xl_rowcol_to_cell(col, total_col + 2))
            sheet.write_formula(col, total_col + 8, f, border, '')
            
            row = 2
            while date_start <= end_date:
                color = workbook.add_format()
                color.set_border(style=1)
                current_date = date_start
                current_date_time = datetime.combine(current_date, datetime.min.time())
                current_end_date_time = datetime.combine(current_date, datetime.max.time())
                attendance = self.env['hr.attendance'].search([
                    ('employee_id', '=', emp_id),
                    ('check_in', '>=', current_date_time),
                    ('check_out', '<=', current_end_date_time)
                ])
                leaves = employee.list_leaves(current_date_time, current_end_date_time)

                # Weekend Sunday color
                weekend = set([6]) # Sunday
                if(current_date.weekday() in weekend):
                    color = yellow
                # Center Color
                color.set_align('center')
       
                # Write Header
                if(not is_header_written):
                    sheet.merge_range(table_start_row, row, table_start_row + 2, row, current_date.strftime('%d'), table_header_format)
                    sheet.set_column(table_start_row, row, 3)

                # Convert or add up
                total_leave_hours = 0
                for day, hours, leave in leaves:
                    total_leave_hours += hours

                if(current_date.weekday() in weekend):
                    sheet.write(col, row, 'P', color)
                else:
                    if(attendance):
                        if(attendance.regularization):
                            sheet.write(col, row, 'S', color)
                        else:
                            sheet.write(col, row, 'P', color)
                    elif(total_leave_hours > 4):
                        # Considered as full day work
                        sheet.write(col, row, 'L', color)
                    elif(total_leave_hours == 4):
                        # Half day leave
                        # TODO: type of remark
                        sheet.write(col, row, 'LH', color)
                    else:
                        sheet.write(col, row, 'A', color)

                row += 1
                date_start += delta

            is_header_written = True
            col += 1

        workbook.close()