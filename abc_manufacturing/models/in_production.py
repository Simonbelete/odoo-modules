from odoo import models, fields

class InProduction(models.Model):
    _name = 'production.model'
    _inherit = 'mrp.production'

    def action_cost_analysis(self):
        print('--------------------------dddddd')
        print('clicked')
        return True