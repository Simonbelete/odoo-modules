from odoo import fields, models

class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    salary = fields.Float(required=True)
    employee_id = fields.Many2one('hr.employee')