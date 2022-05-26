from odoo import fields, api, models

class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    @api.onchange('employee_id', 'date_from', 'date_to')
    def onchange_pyaslip_data(self):
        """ When the above data changes calculate attendance hours 
            and save the hours in hr.payslip.worked_days for further calculation
            on salary rule   hours
        """
        for record in self:
            attendances = self.env['hr.attendace'].search([
                ('employee_id', '=', record.employee_id),
                ('check_in', '=', record.date_from),
                ('check_out', '=', record.date_to)
            ])

            worked_hours = 0
            # Loop through attendance and add the worked_hours
            for attendance in attendances:
                worked_hours = worked_hours + attendance.worked_hours

            # Add the worked hours to the lines id with code
            self.env['hr.payslip.worked_days'].create({
                'name': 'Attendances Working Days',
                'payslip_id': record.id,
                'code': 'ATT',
                'number_of_days': worked_hours/24,
                'number_of_hours': worked_hours,
                'contract_id': record.contract_id
            })