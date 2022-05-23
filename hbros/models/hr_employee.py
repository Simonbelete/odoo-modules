from odoo import fields, api, models

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    mr_production = fields.Many2one('mrp.production', 'user_id')
    