from odoo import models,fields

class Partner (models.Model):
    _name='res.partner'
    _inherit='res.partner'
    
    instructor = fields.Boolean(string='Instructor')
    