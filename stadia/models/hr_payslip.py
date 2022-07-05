import babel
from datetime import date, time, datetime
from pytz import timezone
from odoo import fields, api, models, tools, _

class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    tax_dec = fields.Float(compute="_compute_tax_dec")
    # untaken_leave_salary = fields.Float(default=0, compute="_compute_untaken_leave")
    remaining_leaves = fields.Float(related='employee_id.remaining_leaves')
    # This month taken leave
    total_taken_leaves = fields.Float(compute="_compute_total_taken_leaves")
    # Calculation values
    unpaid_value = fields.Float(compute="_compute_unpaid_value", default=0)
    absent_attendance_value = fields.Float(compute="_compute_absent_attendance_value", default=0)
    perdime_value = fields.Float(compute="_compute_perdime_value")
    # Net Worked days
    # includes LWP, absent attendance
    net_worked_days = fields.Float(compute="_compute_net_worked_days")

    def _compute_net_worked_days(self):
        for record in self:
            total = 0
            for line in record.worked_days_line_ids:
                total += line.number_of_days
            record.net_worked_days = total

    def _compute_total_taken_leaves(self):
        for record in self:
            total_days = 0
            for line in record.worked_days_line_ids:
                if(line.code == 'GLOBAL'):
                    total_days += line.number_of_days
            self.total_taken_leaves = total_days

    def _compute_unpaid_value(self):
        for record in self:
            for line in record.worked_days_line_ids:
                if(line.code == 'LWP'):
                    self.unpaid_value = abs(self.contract_id.wage/30 * line.number_of_days)
                else:
                    self.unpaid_value = 0

    def _compute_absent_attendance_value(self):
        for record in self:
            for line in record.worked_days_line_ids:
                if(line.code == 'ATT'):
                    self.absent_attendance_value = abs(self.contract_id.wage/30 * line.number_of_days)
                else:
                    self.absent_attendance_value = 0

    def _compute_perdime_value(self):
        for record in self:
            total_days = 0
            for line in record.worked_days_line_ids:
                total_days += line.number_of_days

            pd_inputs = 0
            # In Advance perdime
            for iline in record.input_line_ids:
                if(iline.code == 'PD'):
                    pd_inputs += iline.amount

            self.perdime_value = total_days * record.contract_id.perdime + pd_inputs

    def _compute_tax_dec(self):
        for total_wage in self:
            # Get Taxable income
            taxable_income = 0
            overtime = 0

            total = 0
            for line in total_wage.worked_days_line_ids:
                total += line.number_of_days

            for iline in total_wage.input_line_ids:
                if(iline.code == 'OV'):
                    overtime += iline.amount

            taxable_income = self.contract_id.wage/30 * total + overtime

            if taxable_income >= 0 and taxable_income <= 600:
                total_wage.tax_dec = 0
            elif taxable_income > 600 and taxable_income <= 1650:
                total_wage.tax_dec = taxable_income * 0.1 - 60
            elif taxable_income > 1650 and taxable_income <= 3200:
                total_wage.tax_dec = taxable_income * 0.15 - 142.5
            elif taxable_income > 3200 and taxable_income <= 5250:
                total_wage.tax_dec = taxable_income * 0.2 - 302.5
            elif taxable_income > 5250 and taxable_income <= 7800:
                total_wage.tax_dec = taxable_income * 0.25 - 565
            elif taxable_income > 7800 and taxable_income <= 10900:
                total_wage.tax_dec = taxable_income * 0.3 - 955
            elif taxable_income > 10900:
                total_wage.tax_dec = taxable_income * 0.35 - 1500

    @api.model
    def get_worked_day_lines(self, contracts, date_from, date_to):
        """
        @param contract: Browse record of contracts
        @return: returns a list of dict containing the input that should be applied for the given contract between date_from and date_to
        """
        res = []
        # fill only if the contract as a working schedule linked
        for contract in contracts.filtered(lambda contract: contract.resource_calendar_id):
            day_from = datetime.combine(fields.Date.from_string(date_from), time.min)
            day_to = datetime.combine(fields.Date.from_string(date_to), time.max)

            # compute leave days
            leaves = {}
            calendar = contract.resource_calendar_id
            tz = timezone(calendar.tz)
            day_leave_intervals = contract.employee_id.list_leaves(day_from, day_to, calendar=contract.resource_calendar_id)
            for day, hours, leave in day_leave_intervals:
                holiday = leave.holiday_id
                current_leave_struct = leaves.setdefault(holiday.holiday_status_id, {
                    'name': holiday.holiday_status_id.name or _('Global Leaves'),
                    'sequence': 5,
                    'code': holiday.holiday_status_id.code or 'GLOBAL',
                    'number_of_days': 0.0,
                    'number_of_hours': 0.0,
                    'contract_id': contract.id,
                })
                current_leave_struct['number_of_hours'] += hours
                work_hours = calendar.get_work_hours_count(
                    tz.localize(datetime.combine(day, time.min)),
                    tz.localize(datetime.combine(day, time.max)),
                    compute_leaves=False,
                )
                if work_hours:
                    current_leave_struct['number_of_days'] += hours / work_hours

                if(holiday.holiday_status_id.code == 'LWP'):
                    current_leave_struct['number_of_hours'] = -current_leave_struct['number_of_hours']
                    current_leave_struct['number_of_days'] = -current_leave_struct['number_of_days']

            # compute worked days
            work_data = contract.employee_id._get_work_days_data(day_from, day_to, calendar=contract.resource_calendar_id)
            attendances = {
                'name': _("Normal Working Days paid at 100%"),
                'sequence': 1,
                'code': 'WORK100',
                'number_of_days': work_data['days'],
                'number_of_hours': work_data['hours'],
                'contract_id': contract.id,
            }

            worked_attendances = {
                'name': 'Attendances Working Days',
                'code': 'ATT',
                'number_of_days': -work_data['days'],
                'number_of_hours': -work_data['hours'],
                'contract_id': contract.id
            }
            start_date = datetime.combine(date_from, time.min)
            end_date = datetime.combine(date_to, time.max)
            attendances_lists = self.env['hr.attendance'].search([
                ('employee_id', '=', self.employee_id.id),
                ('check_in', '>=', start_date),
                ('check_out', '<=', end_date)
            ])
            # Tab in Tab out attendace
            if attendances_lists:
                worked_hours = 0
                # formate { day: hour}
                worked_hours_per_day = {}
                for attendance in attendances_lists:
                    # Check if the check in and out date is the same
                    if(attendance.check_in.date() == attendance.check_out.date()):
                        if attendance.check_in.day in worked_hours_per_day:
                            worked_hours_per_day[attendance.check_in.day] += attendance.worked_hours
                        else:
                            worked_hours_per_day[attendance.check_in.day] = attendance.worked_hours

                # Loop through daily attendance and subtract 1 luch hour
                # per day attendance
                for i in worked_hours_per_day:
                    if(worked_hours_per_day[i] > 9):
                        worked_hours += 8
                    elif(worked_hours_per_day[i] >= 5):
                        worked_hours += worked_hours_per_day[i] - 1
                    else:
                        worked_hours += worked_hours_per_day[i] 

                worked_attendances['number_of_days'] = worked_hours/8
                worked_attendances['number_of_hours'] = worked_hours

                # Calculate not worked attendaces
                worked_attendances['number_of_days'] = -(attendances['number_of_days'] - worked_attendances['number_of_days'])
                worked_attendances['number_of_hours'] = -(attendances['number_of_hours'] - worked_attendances['number_of_hours'])

            res.append(attendances)
            res.append(worked_attendances)
            res.extend(leaves.values())
        return res


    @api.onchange('employee_id', 'date_from', 'date_to')
    def onchange_employee(self):
        self.ensure_one()
        if (not self.employee_id) or (not self.date_from) or (not self.date_to):
            return
        employee = self.employee_id
        date_from = self.date_from
        date_to = self.date_to
        contract_ids = []

        ttyme = datetime.combine(fields.Date.from_string(date_from), time.min)
        locale = self.env.context.get('lang') or 'en_US'
        self.name = _('Salary Slip of %s for %s') % (employee.name, tools.ustr(babel.dates.format_date(date=ttyme, format='MMMM-y', locale=locale)))
        self.company_id = employee.company_id

        if not self.env.context.get('contract') or not self.contract_id:
            contract_ids = self.get_contract(employee, date_from, date_to)
            if not contract_ids:
                return
            self.contract_id = self.env['hr.contract'].browse(contract_ids[0])

        if not self.contract_id.struct_id:
            return
        self.struct_id = self.contract_id.struct_id

        #computation of the salary input
        contracts = self.env['hr.contract'].browse(contract_ids)
        if contracts:
            worked_days_line_ids = self.get_worked_day_lines(contracts, date_from, date_to)
            worked_days_lines = self.worked_days_line_ids.browse([])
            for r in worked_days_line_ids:
                worked_days_lines += worked_days_lines.new(r)
            self.worked_days_line_ids = worked_days_lines

            input_line_ids = self.get_inputs(contracts, date_from, date_to)
            input_lines = self.input_line_ids.browse([])
            for r in input_line_ids:
                input_lines += input_lines.new(r)
            self.input_line_ids = input_lines
            return