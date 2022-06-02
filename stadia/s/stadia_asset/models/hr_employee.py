from odoo import fields, api, models

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    asset_ids = fields.One2many('account.asset.asset', 'employee_id')