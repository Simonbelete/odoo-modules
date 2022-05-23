from odoo import fields, models

class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    salary = fields.Float()
    employee_id = fields.Many2one('hr.employee')