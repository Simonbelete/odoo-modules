from odoo import api, fields, models

class HrJob(models.Model):
    """ From hr.job """
    _inherit = 'hr.job'

    state = fields.Selection(selection_add=[
        ('internal vacancy', 'Internal Vacancy'),
        ('external vacancy', 'External Vacancy')
    ], ondelete={'internal vacancy': 'set default', 'external vacancy': 'set default'})

    def internal_vacancy(self):
        """ Check if  """