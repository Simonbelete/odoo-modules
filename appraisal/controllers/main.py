from odoo import fields, http

class Appraisal(http.Controller):

    @http.route('/appraisal/<string:token>', type="http", website=True)
    def appraisal_display_page(self, token, **kw):
        SurveyQuestion = http.request.env['appraisal.survey.question']
        questions = SurveyQuestion.search([])
        return http.request.render('appraisal.appraisal_page_index',
        {
            'questions': questions
        })