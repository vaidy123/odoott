# -*- coding: utf-8 -*-
import logging
from odoo import models, fields, api, exceptions, _

_logger = logging.getLogger(__name__)
    
class OpenAcademySession(models.Model):
    _name = 'openacademy.session'
    _description =  'OpenAcademy Sessions'
    _order = 'id, start_date'
    
    sequence = fields.Integer(string='Sequence')
    name = fields.Char(string='Name', required=True, 
                        index=True, help='Enter your course title on this field.')
    active = fields.Boolean(string='Active', default=True)
    course_id = fields.Many2one(comodel_name='openacademy.course', required=True)
    insructor_id = fields.Many2one(comodel_name='res.partner', required=True,
                        string='Instructor', ondelete='restrict', copy=False)
    location_id = fields.Many2one(comodel_name='res.partner', ondelete='restrict')
    code = fields.Char(string='Code', size=32)
    start_date = fields.Datetime(string='Start Date', required=True)
    end_date = fields.Datetime(string='End Date', required=True)
    avail_seat_per = fields.Float(string='Avaliable Seats (%)', store=True,
                        compute='_compute_booked_seats')
    max_seats = fields.Integer(string='Maximum Seats')
    min_seats = fields.Integer(string='Minimum Required Seats')
    booked_seats = fields.Integer(string='Reserved Seats', )
    syllabus_notes = fields.Html(string='Syllabus')
    state = fields.Selection(selection=[
                            ('draft', 'New'),
                            ('approve', 'Approved'),
                            ('confirm', 'Confirmed'),
                            ('cancel', 'Cancelled'),
                            ('done', 'Done'),
                        ])
    _sql_constraints = [
        ('openacademy_Session_unique_code', 'UNIQUE (code)', 'Code must be unique !'),
    ]
    
    @api.depends('max_seats', 'booked_seats')
    def _compute_booked_seats(self):
        for record in self:
            if record.max_seats > 0:
                record.avail_seat_per = (float(record.max_seats - record.booked_seats)/float(record.max_seats))*100.0
            
    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
        for session in self:
            if session.start_date > session.end_date:
                raise exceptions.ValidationError(_('Start date "%s" can not be after end date %s"')%(session.start_date, session.end_date))

    @api.model_create_multi          
    def create(self, vals_list):
        _logger.warning('*'*50)
        _logger.warning(vals_list)
        """
        for record in vals_list:
            if record.get('start_date') and record.get('end_date') and \
                record.get('start_date') > record.get('end_date'):
                    raise exceptions.ValidationError(_('1) Start date can not be after end date')
        """
        res = super(OpenAcademySession, self).create(vals_list)
        return res
    
    def unlink(self):
        _logger.info(self.env.context)
        if not self.env.context.get('bypass_unlink'):
            raise exceptions.AccessDenied('You can not delete this record.')
        return super(OpenAcademySession, self).unlink()