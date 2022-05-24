from odoo import api, fields, models, _

from attr import exceptions
from odoo.exceptions import ValidationError


class EmployeeContract(models.Model):
    _inherit = "hr.contract"

    def toRunning(self):
        self.state = 'open'

    def toExpired(self):
        self.state = 'close'

    def toDraft(self):
        self.state = 'draft'

    @api.constrains('employee_id.assigned_asset')
    def toCancel(self):
        if not self.employee_id.assigned_asset:
            self.state = 'cancel'
        else:
            raise ValidationError('Unable to Cancel Employee contract Before Give back Company Assets')
