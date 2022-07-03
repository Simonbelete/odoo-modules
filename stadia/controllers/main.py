from odoo import http

class Appraisal(http.Controller):

    @http.route('/appraisal/<string:token>', type="http", website=True)
    def appraisal_display_page(self, token, **kw):
        appraisal = http.request.env['stadia.appraisal'].search([('token', '=', token)])
        return http.request.render('stadia.website_appraisal_template',{
            'appraisal': appraisal
        })