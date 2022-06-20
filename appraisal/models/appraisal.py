from odoo import fields, api, models

class AppraisalTemplate(models.Model):
    _name = 'appraisal.template'

    name = fields.Char()
    parent_id = fields.Many2one('appraisal.template')

class Appraisal(models.Model):
    """ All employee appraisals """
    _name = 'appraisal.appraisal'

    template_ids = fields.Many2many('appraisal.template')

