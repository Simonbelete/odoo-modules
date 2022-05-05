from odoo import models

class AppraisalReport(models.AbstractModel):
    _name = 'report.appraisal.appraisal_report'

    def _get_report_values(self, docids, data=None):
        # get the report action back as we will need its data
        report = self.env['ir.actions.report']._get_report_from_name('appraisal.appraisal_report')
        # get the records selected for this rendering of the report
        obj = self.env[report.model].browse(docids)
        # return a custom rendering context
        return {
            'lines': docids,
            'data': 'data',
            'da': {'name': 'eg name'}
        }
