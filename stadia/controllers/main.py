from odoo import http

class Appraisal(http.Controller):

    @http.route('/appraisal', type="http", website=True)
    def appraisal_display_page(self, **kw):
        # Check if anser is created if not create empty answers
        return http.request.render('stadia.website_appraisal_template',{
            'data': 'abcd'
        })