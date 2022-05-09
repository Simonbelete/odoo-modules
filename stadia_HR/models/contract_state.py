from odoo import fields, models, _, api


class ContractStat(models.Model):
    _inherit = "hr.contract"
    asset_taken = fields.Boolean(string="Asset Check")
    loan_taken = fields.Boolean(string="Loan Check")

    def expire(self):
        if self.asset_taken and self.loan_taken:
            self.state = 'close'

    def draft(self):
        self.state = 'open'

    def close(self):
        self.state = 'cancel'
    # state_name = fields.Char(related="stage_id.name", string="Sname")
