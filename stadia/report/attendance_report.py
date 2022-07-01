from odoo import api, models
from datetime import datetime, time, timedelta

class AttendacneReport(models.AbstractModel):
    _name = 'report.stadia.attendance_report'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, partners):
        sheet = workbook.add_worksheet()

        bold = workbook.add_format({'bold': True})
        yellow = workbook.add_format({'bg_color': '#FCD5B5'})
        center = workbook.add_format()
        center.set_align('center')
        center.set_align('vcenter')
        border = workbook.add_format()
        border.set_border(style=1)
        table_header_format = workbook.add_format()
        table_header_format.set_align('center')
        table_header_format.set_align('vcenter')
        table_header_format.set_bold()
        table_header_format.set_font_size(13)
        table_header_format.set_border(style=1)

        employee_ids = data['form']['emp']
        start_date = datetime.strptime(data['form']['date_from'], '%Y-%m-%d').date()
        end_date = datetime.strptime(data['form']['date_to'], '%Y-%m-%d').date()

        total_row = len(employee_ids) + 3
        total_col = (end_date - start_date).days

        # Logo Header
        header_row = 5
        header_format = workbook.add_format()
        header_format.set_font_size(15)
        header_format.set_bold()
        half_row = abs(int((total_row - 13)/2))
        
        sheet.merge_range(0, half_row, 0, half_row + 15, 'Stadia Engineering Works Consultant Plc', header_format)

        # Tables header
        table_start_row = header_row + 1
        sheet.merge_range(table_start_row, 0, table_start_row + 3, 0, 'S.No', table_header_format)
        sheet.merge_range(table_start_row, 1, table_start_row + 3, 1, 'Name', table_header_format)
        sheet.merge_range(table_start_row + 1, total_col + 3, table_start_row + 1, total_col + 8, 'Total', table_header_format)
        sheet.write(table_start_row + 2, total_col + 3, 'P', center)
        sheet.write(table_start_row + 2, total_col + 4, 'S', center)
        sheet.write(table_start_row + 2, total_col + 5, 'T', center)
        sheet.write(table_start_row + 2, total_col + 6, 'L', center)
        sheet.write(table_start_row + 2, total_col + 7, 'A', center)
        sheet.write(table_start_row + 2, total_col + 8, 'Total', center)

        # Sizes
        sheet.set_column(0, 0, 5)
        sheet.set_column(1, 1, 20)
        sheet.set_column(total_col + 3, total_col + 3, 5)
        sheet.set_column(total_col + 4, total_col + 4, 5)
        sheet.set_column(total_col + 5, total_col + 5, 5)
        sheet.set_column(total_col + 6, total_col + 6, 5)
        sheet.set_column(total_col + 7, total_col + 7, 5)
        sheet.set_column(total_col + 8, total_col + 8, 5)

        data_start_row = table_start_row + 4
        col = data_start_row
        # Write Headers
        is_header_written = False
        for emp_id in employee_ids:
            employee = self.env['hr.employee'].search([('id', '=', emp_id)])
            delta = timedelta(days=1)
            date_start = start_date

            sheet.write(col, 0, col - table_start_row + 1)
            sheet.write(col, 1, employee.name)

            row = 2
            while date_start <= end_date:
                color = workbook.add_format()
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
                    sheet.merge_range(table_start_row, row, table_start_row + 3, row, current_date.strftime('%d'), table_header_format)
                    sheet.set_column(table_start_row, row, 3)
                    total_col += 1

                # Convert or add up
                total_leave_hours = 0
                for day, hours, leave in leaves:
                    total_leave_hours += hours

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
