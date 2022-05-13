from odoo import api, fields, models

class HrJob(models.Model):
    """ From hr.job """
    _inherit = 'hr.job'

    internal_applicant_count = fields.Integer(compute="_compute_internal_applicant_count", string="Internal Applicant Count")
    state = fields.Selection(selection_add=[
        ('internal vacancy', 'Internal Vacancy'),
        ('external vacancy', 'External Vacancy')
    ], ondelete={'internal vacancy': 'set default', 'external vacancy': 'set default'})

    def _compute_internal_applicant_count(self):
        """ Count Internal Applicants """
        read_group_result = self.env['stadia.internal.applicant'].read_group([('job_id', 'in', self.ids)], ['job_id'], ['job_id'])
        result = dict((data['job_id'][0], data['job_id_count']) for data in read_group_result)
        for job in self:
            job.internal_applicant_count = result.get(job.id, 0)

    def internal_vacancy(self):
        """ Check if  """