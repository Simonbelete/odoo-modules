import json
from odoo import fields, http

class Appraisal(http.Controller):

    def _query(self):
        return """
            SELECT appraisal_appraisal.survey_id
                FROM appraisal_appraisal
                
        """.strip()

        #  INNER JOIN appraisal_survey
        #         INNER JOIN appraisal_survey_question
        #         INNER JOIN appraisal_appraisal_score
        #         WHERE appraisal_appraisal.survey_id = appraisal_survey.id
        #             AND appraisal_survey_question.id in appraisal_survey
        #             AND appraisal_appraisal_score.id = appraisal_survey_question.id

    @http.route('/appraisal/<string:token>', type="http", website=True)
    def appraisal_display_page(self, token, **kw):
        Appraisal = http.request.env['appraisal.appraisal']
        SurveyQuestion = http.request.env['appraisal.survey.question']
        SurveyScore = http.request.env['appraisal.appraisal.score']
        # Get current appraisal
        # appraisal = Appraisal.search([('token', '=', token)])
        # Get appraisals survey questions
        # questions = SurveyQuestion.search([('survey_ids', 'in', (appraisal.id))])
        # answers = SurveyScore.search([('appraisal_id.token', '=', token)])
        questions = http.request.cr.execute(self._query())
        data = http.request.cr.fetchall()
        print("0000000000000000000000000000000000000000000000")
        print(json.dumps(data, indent=4, sort_keys=True, default=str))
        return http.request.render('appraisal.appraisal_page_index',
        {
            'questions': data,
            # 'answers': answers
        })