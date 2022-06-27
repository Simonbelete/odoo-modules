from odoo import api, fields, models, _
from odoo.exceptions import UserError

class HrLeaveReportListReport(models.AbstractModel):
    _name = 'report.stadia.leave_report'
    _inherit = 'report.report_xlsx.abstract'

    @api.model
    def _get_report_values(self, docids, data=None):
        if not data.get('form'):
            raise UserError(_("Form content is missing, this report cannot be printed."))
        return {

        }

    def generate_xlsx_report(self, workbook, data, partners):
        sheet = workbook.add_worksheet()
        bold = workbook.add_format({'bold': True})
        sheet.write(0, 0, 'የተገዛበት ቀን', bold)