from odoo import fields, api, models

class Acquisition(models.Model):
    """ Acquisition Form for hiring or promoting employee """
    _name = 'stadia.acquisition.acquisition'
    _res_name = 'job_id'

    requested_by = fields.Many2one('hr.employee') # default=lambda self: self.env.user)
    job_id = fields.Many2one('hr.job')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('approved', 'Approved'),
        ('declined', 'Declined'),
        ('done', 'Done'),
    ], default='draft', 
    help="draft - when the acquisition is created"
        "approved - approved by general manager i.e start recruiting"
        "declined - GM have not approved the acquisition")
    decline_reason = fields.Char()
    no_of_recruitment = fields.Integer(default=1)

    ## Below fields are for recommendation cv/employee
    #recommended_employee_id = fields.Many2one('hr.employee')
    #recommended_employee_salary = fields.Float()
    #recommended_employee_allowance = fields.Float()
    #recommended_effective_date = fields.Date()

    def action_approve(self):
        """ Approve acquisition and create/start recruiting in hr.recruitment """
        for record in self:
            record.write({'state': 'approved'})

    def action_decline(self):
        """ Decline acquisition request """
        for record in self:
            record.write({'state': 'declined'})