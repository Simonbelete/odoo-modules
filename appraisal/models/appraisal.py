import uuid
from odoo import fields, api, models
from datetime import date

class Appraisal(models.Model):
    """ Appraisal for each employee yearly or 6 moths. """
    _name = 'appraisal.appraisal'
    _description = 'Appraisal'
    _rec_name = 'employee_id'

    def _get_default_token(self):
        return str(uuid.uuid4())

    employee_id = fields.Many2one('hr.employee', string = 'Employee')
    # uuid for url parameter
    # instead of using id as a url parament we use generated uuid
    token = fields.Char('Token', default=lambda self: self._get_default_token(), copy=False)
    survey_id = fields.Many2one('appraisal.survey', required=True)
    state = fields.Selection(string="Status", required=True, readonly=True, copy=False, tracking=True, selection=[
        ('draft', 'To Confirm'),
        ('confirmed', 'Confirmed'),
        ('done', 'Done')
    ], default="draft",
    help="The current state of the appraisal:"
         "- To Confirm: Newly created appraisal")
    evaluation_date = fields.Date(default=date.today())

    # Reference field
    appraisal_score_ids = fields.One2many('appraisal.appraisal.score', 'appraisal_id')

    # Computed fields
    last_evaluation = fields.Date(compute="_compute_last_evaluation")
    
    # ------------------------------------------------------------
    # ACTIONS
    # ------------------------------------------------------------

    def action_start_survery(self):
        """ Open the website page with the survey form """
        self.ensure_one()
        return {
            'type': 'ir.actions.act_url',
            'name': 'Start Appraisal',
            'target': 'self',
            'url': '/appraisal/%s' % str(self.token)
        }

    def send_report(self):
        for record in self:
            mail_template = self.env.ref('appraisal.eamil_appraisla_with_report')
            mail_template.send_mail(record.id, force_send=True)

    # def action_print_report(self):
    #     data = {
    #         'ab': {
    #             'name': 'example name'
    #         }
    #     }
    #     return self.env.ref['btn_action_print_appraisal'].report_action(None, data=data)

    # ------------------------------------------------------------
    # Computed Fields
    # ------------------------------------------------------------
    def _compute_last_evaluation(self):
        for record in self:
            employee_appraisals = self.env['appraisal.appraisal'].search([
                ('employee_id', '=', record.employee_id.id)
            ])

            # Get appraisl dates as array
            employee_appraisal_dates = []
            for a in employee_appraisals:
                employee_appraisal_dates.append(a.evaluation_date)

            # Calculate the closest date from the list
            last_appraisal_date = min(employee_appraisal_dates, key=lambda sub: abs(sub - date.today()))

            record.last_evaluation = last_appraisal_date