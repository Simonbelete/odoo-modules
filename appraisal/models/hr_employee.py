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

    def notify_and_upate_appraisal_status(self):
        appraisals = self.env['hr.employee'].search([])
        print('11111111111111111111111111111111111111111111111111')
        print(appraisals)