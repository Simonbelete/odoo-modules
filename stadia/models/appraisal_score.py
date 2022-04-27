from termios import TAB1
from odoo import models, fields

class AppraisalScore(models.Model):
    _name = 'stadia.appraisal.score'

    appraisal_id = fields.Many2one('stadia.appraisal.appraisal')
    sub_trait_id = fields.Many2one('stadia.appraisal.sub.trait', required = True)
    score = fields.Selection([
        (1, 'Severely lacking in knowledge'),
        (2, 'Noticeable deficiencies in job knowledge'),
        (3, 'Understanding job routine. Some knowledge still to be acquired'),
        (4, 'Completely understands all aspects of the job'),
        (5, 'Understands why all job functions are performed and inter-relationship with other jobs. An expert')
    ])