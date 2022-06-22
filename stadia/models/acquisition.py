from datetime import datetime
from odoo import fields, api, models

class Acquisition(models.Model):
    """ Acquisition Form for hiring or promoting employee """
    _name = 'stadia.acquisition'
    _rec_name = 'title'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'acquisition_date desc'

    title = fields.Char(compute="_compute_name")
    acquisition_date = fields.Date(default=datetime.now(), required=True)
    requested_by = fields.Many2one('hr.employee', default=lambda self: self.env.user.employee_id.id)
    job_id = fields.Many2one('hr.job', domain="[('department_id', '=', department_id)]")
    department_id =  fields.Many2one(related="requested_by.department_id")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('requested', 'Requested'),
        ('approved', 'Approved'),
        ('declined', 'Declined'),
        ('done', 'Done')
    ], default='draft', 
    help="draft - when the acquisition is created"
        "approved - approved by general manager i.e start recruiting"
        "declined - GM have not approved the acquisition")
    no_of_recruitment = fields.Integer(default=1)
    note = fields.Text()
    internal_applicant_ids = fields.One2many('stadia.promotion', 'acquisition_id')
    external_applicant_ids = fields.One2many('hr.applicant', 'acquisition_id')

    # Job Specifications
    education_id = fields.Many2one('stadia.education')
    experience_total_year = fields.Integer()
    experience_related_job_id = fields.Many2one('hr.job')
    training_related_job_id = fields.Many2one('hr.job')
    training_skills = fields.Char()
    # Duties and Responsibilities
    job_description = fields.Html()
    place_department_id = fields.Many2one('hr.department')
    work_place_id = fields.Many2one('stadia.workplace')
    

    def action_request(self):
        """ Request to GM """
        self.schedule_activity()
        for record in self:
            record.write({'state': 'requested'})

    def action_approve(self):
        """ Approve acquisition, start recruiting"""
        for record in self:
            record.write({'state': 'approved'})
        self.schedule_activity_done()

    def action_decline(self):
        """ Decline acquisition request, stop recruiting """
        for record in self:
            record.write({'state': 'declined'})

    def action_done(self):
        """ Move all (internal/external) applicants to refused state """
        # for ea in self.external_applicant_ids:
        #     ea.write({'active': False})

        # for ia in self.internal_applicant_ids:
        #     ia.write({'active': False})

        self.write({'state': 'done'})

    @api.model
    def create(self, values):
        acquisition = super(Acquisition, self).create(values)
        # self.activity_schedule('stadia.mail_act_acquisition_approval',user_id=self.zz.user_id, summary='Acquisition Approval', note=f'Please Approve {self.title}')
        return acquisition

    @api.onchange('date', 'job_id')
    def _compute_name(self):
        for record in self:
            if(not record.job_id or not record.acquisition_date):
                record.title = ''
            else: 
                record.title = 'Acquisition of %s department for %s' % (record.job_id.name, record.acquisition_date.strftime('%d-%B-%Y'))

    def schedule_activity(self):
        users = self.env.ref('stadia.group_acquisition_admin').users
        for user in users:
            if(user.active == True):
                self.activity_schedule('stadia.mail_act_acquisition_approval', user_id=user.id, summary='Acquisition Approval', note=f'Please Approve {self.title}')

    def schedule_activity_done(self):
        activity = self.env['mail.activity'].search([
            ('res_id', '=', self.id), 
            ('user_id', '=', self.env.user.id), 
            ('activity_type_id', '=', self.env.ref('stadia.mail_act_acquisition_approval').id)
            ])
        activity.action_feedback(feedback='Approved')
        other_activity = self.env['mail.activity'].search([
            ('res_id', '=', self.id), 
            ('activity_type_id', '=', self.env.ref('stadia.mail_act_acquisition_approval').id)
            ])
        other_activity.unlink()
