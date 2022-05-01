import json
from odoo import fields, http

class Appraisal(http.Controller):

    def _query(self, question_ids):
        return """
            SELECT appraisal_survey_question.id AS question_id,
                    appraisal_survey_question.title AS title,
                    appraisal_survey_question.description AS description,
                    appraisal_survey_question.sequence AS question_sequence,
                    appraisal_appraisal_score.id AS score_id
                FROM appraisal_survey_question
                LEFT JOIN appraisal_appraisal_score
                    ON appraisal_survey_question.id = appraisal_appraisal_score.question_id
                WHERE appraisal_survey_question.id IN (%s)
                ORDER BY appraisal_survey_question.category_id ASC,
                    appraisal_survey_question.sequence ASC
        """ % (','.join(map(str, question_ids)))


        # SELECT appraisal_appraisal.survey_id,
        #             appraisal_survey.title,
        #             appraisal_survey_question.title
        #         FROM appraisal_appraisal
        #         INNER JOIN appraisal_survey
        #             ON appraisal_appraisal.survey_id = appraisal_survey.id
        #         INNER JOIN appraisal_survey_question
        #             ON  appraisal_survey.question_ids = appraisal_survey_question.id

        #  INNER JOIN appraisal_survey
        #         INNER JOIN appraisal_survey_question
        #         INNER JOIN appraisal_appraisal_score
        #         WHERE appraisal_appraisal.survey_id = appraisal_survey.id
        #             AND appraisal_survey_question.id in appraisal_survey
        #             AND appraisal_appraisal_score.id = appraisal_survey_question.id

    @http.route('/appraisal/<string:token>', type="http", website=True)
    def appraisal_display_page(self, token, **kw):
        Appraisal = http.request.env['appraisal.appraisal']
        AppraisalScore = http.request.env['appraisal.appraisal.score']
        SurveyQuestion = http.request.env['appraisal.survey.question']
        SurveyScore = http.request.env['appraisal.appraisal.score']
        # Get current appraisal
        appraisal = Appraisal.search([('token', '=', token)])
        # Get appraisals survey questions
        # question_ids = appraisal.survey_id.question_ids.ids
        # http.request.cr.execute(self._query(question_ids))
        # question_with_answers = http.request.cr.dictfetchall()
        # print("0000000000000000000000000000000000000000000000")
        # print(json.dumps(question_with_answers, indent=4, sort_keys=True, default=str))

        question_ids = appraisal.survey_id.question_ids.ids
        questions = SurveyQuestion.search([('id', 'in', question_ids)])
        answers = SurveyScore.search([('question_id', 'in', question_ids)])
        categories = []
        for question in questions:
            categories.append(question.category_id)
        categories = set(categories)

        print("0000000000000000000000000000000000000000000000")
        print(json.dumps(answers, indent=4, sort_keys=True, default=str))

        return http.request.render('appraisal.appraisal_page_index',
        {
            'appraisal_id': appraisal.id,
            'appraisal_token': token,
            'questions': questions,
            'answers': answers,
            'categories': categories
        })

    @http.route('/appraisal/submit', type='http', website=True)
    def appraisal_submit(self, **kw):
        # Format of post data
        # { 'question_id': 'score'}
        SurveyScore = http.request.env['appraisal.appraisal.score']
        SurveyQuestion = http.request.env['appraisal.survey.question']
        data = kw
        # clean data 
        # get only question_id dict
        del data['appraisal_id']
        del data['appraisal_token']

        for question_id in data:
            # Check if score exists if so update, if not create
            survey = SurveyScore.search_count([
                ('appraisal_id', '=', kw.get('appraisal_id')),
                ('question_id', '=', question_id)
            ])
            score_dict = {
                'appraisal_id': kw.get('appraisal_id'),
                'question_id': question_id,
                'score': data[question_id]
            }

            if survey == 0:
                SurveyScore.create(score_dict)
            elif survey > 1:
                SurveyScore.write(score_dict)
        print(kw)
