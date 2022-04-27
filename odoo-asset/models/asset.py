from odoo import fields, models


class AssetDetail(models.Model):
    _inherit = 'account.asset.asset'
    responsible_id = fields.Many2one('hr.employee', string="Responsible Person")
    tag_number = fields.Char(string="Tag Number")
