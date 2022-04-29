from odoo import fields, models, api

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    # In Months
    appraisal_first_recuritment = fields.Integer(default = 6, config_parameter='appraisal.appraisal_first_recuritment') 
    appraisal_after_recuritment = fields.Integer(default = 12, config_parameter='appraisal.appraisal_after_recuritment')
    appraisal_every = fields.Integer(default = 12, config_parameter='appraisal.appraisal_every')