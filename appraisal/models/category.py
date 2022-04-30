from odoo import models, fields

class Category(models.Model):
    """ Top level Category of assement """
    _name = "appraisal.category"

    name = fields.Char(required = True)
    definition = fields.Text()