from odoo import models, fields, api

class SurveyUserInput(models.Model):
    _inherit = 'survey.user_input'
    
    @api.model
    def create(self, vals):
        ctx = self.env.context
        print('------------------------------------')
        print('------------------------------------')
        print(ctx)
        print(vals)
        if ctx.get('active_id') and ctx.get('active_model') == 'hr.appraisal':
            vals['appraisal_id'] = ctx.get('active_id')
        return super(SurveyUserInput, self).create(vals)