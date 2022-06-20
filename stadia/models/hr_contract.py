from odoo import fields, api, models

class HrContract(models.Model):
    _inherit = 'hr.contract'

    def _default_work_place_id(self):
        return self.env['stadia.workplace'].search([('name', '=', 'Head Office')], limit=1)

    def _default_ref_no(self):
        return self.env['ir.sequence'].next_by_code('ref.no.sequence')

    ref_no = fields.Char(string="Ref No", copy=False, default=_default_ref_no)
    # Per day perdime
    perdime = fields.Monetary(default = 0)
    cost_sharing = fields.Monetary(default = 0)
    work_place_id = fields.Many2one('stadia.workplace', required=True, default=_default_work_place_id)