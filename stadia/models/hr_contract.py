from odoo import fields, api, models

class HrContract(models.Model):
    _inherit = 'hr.contract'

    # Per day perdime
    perdime = fields.Monetary(default = 0)
    cost_sharing = fields.Monetary(default = 0)