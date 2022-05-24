from odoo import api, fields, models, _


class EmployeeAsset(models.Model):
    _inherit = "hr.employee"
    assigned_asset = fields.Many2many('account.asset.asset', widget="many2many_tags")
