from odoo import fields, api, models

class HrContract(models.Model):
    _inherit = 'hr.contract'

    # In days
    perdime = fields.Monetary(default = 0)