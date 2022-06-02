from datetime import datetime
from odoo import fields, api, models

class Acquisition(models.Model):
    """ Acquisition Form for hiring or promoting employee """
    _name = 'stadia.acquisition'
    _rec_name = 'title'

    title = fields.Char(compute="_compute_name")
    acquisition_date = fields.Date(default=datetime.now(), required=True)
    requested_by = fields.Many2one('hr.employee', default=lambda self: self.env.user.employee_id.id)
    job_id = fields.Many2one('hr.job', domain="[('department_id', '=', department_id)]")
    department_id =  fields.Many2one(related="requested_by.department_id")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('approved', 'Approved'),
        ('declined', 'Declined'),
    ], default='draft', 
    help="draft - when the acquisition is created"
        "approved - approved by general manager i.e start recruiting"
        "declined - GM have not approved the acquisition")
    decline_reason = fields.Text()
    no_of_recruitment = fields.Integer(default=1)
    note = fields.Text()
    # recommendation_ids = fields.One2many('stadia.acquisition.recommendation', 'acquisition_id')
    # application_ids = fields.One2many('hr.applicant', 'acquisition_id')

    def action_approve(self):
        """ Approve acquisition, start recruiting"""
        for record in self:
            
            record.write({'state': 'approved'})

    def action_decline(self):
        """ Decline acquisition request, stop recruiting """
        for record in self:
            record.write({'state': 'declined'})

    @api.onchange('date', 'job_id')
    def _compute_name(self):
        if(not self.job_id):
            return
        for record in self:
            record.title = 'Acquisition of %s department for %s' % (record.job_id.name, record.acquisition_date.strftime('%d-%B-%Y'))