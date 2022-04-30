import uuid
from odoo import fields, api, models

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
    survey_id = fields.Many2one('appraisal.survey')
    state = fields.Selection(string="Status", required=True, readonly=True, copy=False, tracking=True, selection=[
        ('draft', 'To Confirm'),
        ('confirmed', 'Confirmed'),
        ('done', 'Done')
    ], default="draft",
    help="The current state of the appraisal:"
         "- To Confirm: Newly created appraisal")

    # ------------------------------------------------------------
    # ACTIONS
    # ------------------------------------------------------------

    def action_start_survery(self):
        """ Open the website page with the survey form """