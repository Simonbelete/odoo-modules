from odoo import models, fields, api
from datetime import date
from dateutil.relativedelta import relativedelta

class HrEmployee(models.Model):
    """ From hr.hr_employee """
    # _name = 'appraisal.hr.employee'
    _inherit = 'hr.employee'

    appraisal_ids = fields.One2many('appraisal.appraisal', 'employee_id')
    # last_appraisal_date = fields.Date(compute="_compute_last_appraisal_date", store=True)
    hired_date = fields.Date(default=date.today(), required=True)
    appraisal_status = fields.Selection([
        ('new', 'New'),
        ('to start', 'To Start'),
        ('started', 'Started'),
        ('done', 'Canacled')
    ], default='new')
    # last_appraisal_date = fields.Date()
    
    # def _compute_last_appraisal_date(self):

    # @api.depends('last_appraisal_date')
    # def _compute_appraisal_status(self):
    #     for record in self:
    #         if(not record.appraisal_ids):
    #             record.appraisal_status = 'new'
    #         else:
    #             last_appraisal = None
    #             last_appraisal_date = None
    #             last_appraisal_date_index = -1
    #             appraisal_dates = []
    #             for appraisal in record.appraisal_ids:
    #                 appraisal_dates.append(appraisal.evaluation_date)

    #             last_appraisal_date = min(appraisal_dates, key=lambda sub: abs(sub - date.today()))
    #             last_appraisal_date_index = appraisal_dates.index(last_appraisal_date)
    #             last_appraisal = record.appraisal_ids[last_appraisal_date_index]
    #             # Calculate apprisal dates
    #             if(last_appraisal):
    #                 if((last_appraisal.evaluation_date + relativedelta(1)) > date.today()):
    #                     record.appraisal_status = 'to start'
    #                 else:
    #                     record.appraisal_status = 'started'
    #             else:
    #                 record.appraisal_status = 'done'

    def diff_month(self, d1, d2):
        return abs((d1.year - d2.year) * 12 + d1.month - d2.month)

    def diff_days(self, d1, d2):
        return abs((d2 - d1).days)

    def send_email(self, emp_id):
        mail_template = self.env.ref('appraisal.eamil_appraisla_notify')
        mail_template.send_mail(emp_id, force_send=True)

    def notify_and_upate_appraisal_status(self):
        settings_appraisal_first_recuritment = int(self.env['ir.config_parameter'].sudo().get_param('appraisal.appraisal_first_recuritment'))
        settings_appraisal_every = int(self.env['ir.config_parameter'].sudo().get_param('appraisal.appraisal_every'))
        employees = self.env['hr.employee'].search([('work_email', '=', 'emptwo@localhost.com')])
        for employee in employees:
            # Check if appraisal using hired_date
            no_days = self.diff_days(employee.hired_date, date.today())
            no_months = self.diff_month(employee.hired_date, date.today())
            if(no_months == settings_appraisal_first_recuritment):
                # Temp Employee
                self.send_email(employee.id)
                employee.write({'appraisal_status': 'to start'})
            elif(no_months > settings_appraisal_first_recuritment and (no_months % settings_appraisal_every == 0)):
                self.send_email(employee.id)
                employee.write({'appraisal_status': 'to start'})