from odoo import models

class AppraisalReport(models.AbstractModel):
    _name = 'report.appraisal.appraisal_report'

    def _get_report_values(self, docids, data=None):
        # get the report action back as we will need its data
        report = self.env['ir.actions.report']._get_report_from_name('appraisal.appraisal_report')
        # get the records selected for this rendering of the report
        obj = self.env[report.model].browse(docids)

        AppraisalScore = self.env['appraisal.appraisal.score']
        SurveyQuestion = self.env['appraisal.survey.question']
        SurveyScore = self.env['appraisal.appraisal.score']
        # Get current appraisal
        appraisal = obj

        question_ids = appraisal.survey_id.question_ids.ids
        questions = SurveyQuestion.search([('id', 'in', question_ids)])
        answers = SurveyScore.search([('question_id', 'in', question_ids)])
        categories = []
        for question in questions:
            categories.append(question.category_id)
        categories = set(categories)

        print('ddddddddddddddddddddddddddddddddddddddddddddddd')
        print(obj.employee_id.name)

        # return a custom rendering context
        return {
            'lines': docids,
            'docs': obj,
            'appraisal_id': appraisal.id,
            'questions': questions,
            'answers': answers,
            'categories': categories
        }
