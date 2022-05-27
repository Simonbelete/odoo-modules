from odoo import fields, api, models

class HrContract(models.Model):
    _inherit = 'hr.contract'

    # In days
    perdime = fields.Float(default = 0)