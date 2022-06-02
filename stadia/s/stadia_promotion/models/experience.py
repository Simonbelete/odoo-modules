from odoo import fields, api, models

class Experience(models.Model):
    """ Employee experience when promotion is approved"""
    _name = 'stadia.promotion.experience'

    start_date = fields.Date()
    end_date = fields.Date()
    # No of experience day, month, year
    #promotion_id = fields.One2one('stadia.promotion.promotion')