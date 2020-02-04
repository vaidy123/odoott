from odoo import models, fields
class OpenAcademyCourse(models.Model):
    _name = 'openacademy.course'
    _description = 'OpenAcademy Course'
    
    
    name = fields.Char(string='Course Title', required=True, index=True, help='Enter Your course title.')
    description = fields.Html(string='Description')
    banner = fields.Binary(string='Banner')
    price = fields.Float(string='Price', digits=(5,4))
    expire_date = fields.Date(string='Expire After', required=True)