from odoo import fields, api, models

class HrContract(models.Model):
    _inherit = 'hr.contract'

    project_id = fields.Many2one('project.project', required=True)
    # Per day perdime
    perdime = fields.Monetary(default = 0)