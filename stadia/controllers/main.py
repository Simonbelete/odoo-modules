from odoo import http

class Appraisal(http.Controller):

    @http.route('/appraisal', type="http", website=True)
    def appraisal_display_page(self, **kw):
        return http.request.render('stadia.website_appraisal_template',{
            'data': 'abcd'
        })