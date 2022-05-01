from odoo import fields, http

class Appraisal(http.Controller):

    @http.route('/appraisal/test/<string:appraisal_id>', type="http", website=True)
    def appraisal_test(self, appraisal_id, **kwargs):
        SurveyQuestion = http.request.env['appraisal.survey.question']
        questions = SurveyQuestion.search([]) #search([('survey_ids', 'in', appraisal_id )])
        return http.request.render('appraisal.appraisal_survery_page', {
            'teachers': ["Diana Padilla", "Jody Caroll", "Lester Vaughn"],
            'questions': questions
        })

    @http.route('/appraisal/test/start', type="json", website=True)
    def appraisal_test_start(self, **kwargs):
        return {'a':'b'}