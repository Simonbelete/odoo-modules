from odoo import api, models
from datetime import datetime, time, timedelta

class AttendacneReport(models.AbstractModel):
    _name = 'report.stadia.attendance_report'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, partners):
        sheet = workbook.add_worksheet()

        total_col = 2
        employee_ids = data['form']['emp']
        start_date = datetime.strptime(data['form']['date_from'], '%Y-%m-%d').date()
        end_date = datetime.strptime(data['form']['date_to'], '%Y-%m-%d').date()

        col = 1
        # Write Headers
        is_header_written = False
        for emp_id in employee_ids:
            employee = self.env['hr.employee'].search([('id', '=', emp_id)])
            delta = timedelta(days=1)
            date_start = start_date

            sheet.write(col, 0, employee.name)

            row = 1
            while date_start <= end_date:
                current_date = date_start
                current_date_time = datetime.combine(current_date, datetime.min.time())
                current_end_date_time = datetime.combine(current_date, datetime.max.time())
                attendance = self.env['hr.attendance'].search([
                    ('employee_id', '=', emp_id),
                    ('check_in', '>=', current_date_time),
                    ('check_out', '<=', current_end_date_time)
                ])
                leaves = employee.list_leaves(current_date_time, current_end_date_time)

                # Write Header
                if(not is_header_written):
                    sheet.write(0, row, current_date.strftime('%d'))

                # Convert or add up
                total_leave_hours = 0
                for day, hours, leave in leaves:
                    total_leave_hours += hours
       
                if(attendance):
                    if(attendance.regularization):
                        sheet.write(col, row, 'S')
                    else:
                        sheet.write(col, row, 'P')
                elif(total_leave_hours > 4):
                    # Considered as full day work
                    sheet.write(col, row, 'L')
                elif(total_leave_hours == 4):
                    # Half day leave
                    # TODO: type of remark
                    sheet.write(col, row, 'LH')
                else:
                    sheet.write(col, row, 'A')

                row += 1
                date_start += delta
            col += 1

