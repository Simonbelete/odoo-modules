from odoo import api, fields, models, _
from odoo.exceptions import UserError

class HrLeaveReportListReport(models.Model):
    _name = 'report.hr_leave_report_list_report'

    @api.model
    def _get_report_values(self, docids, data=None):
        if not data.get('form'):
            raise UserError(_("Form content is missing, this report cannot be printed."))
        return {

        }