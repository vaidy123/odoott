# -*- coding: utf-8 -*-
import logging
from datetime import timedelta


from odoo import models, fields, api, exceptions, _

_logger = logging.getLogger(__name__)
    
class OpenAcademySession(models.Model):
    _name = 'openacademy.session'
    _description =  'OpenAcademy Sessions'
    _order = 'id, start_date'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    sequence = fields.Integer(string='Sequence')
    name = fields.Char(string='Name', required=True, 
                        index=True, help='Enter your course title on this field.',
                          readonly=True, states={'draft': [('readonly', False)]})
    active = fields.Boolean(string='Active', default=True)
    course_id = fields.Many2one(comodel_name='openacademy.course', required=True,
                         readonly=True, states={'draft': [('readonly', False)]})
    insructor_id = fields.Many2one(comodel_name='res.partner', required=True,
                        string='Instructor', ondelete='restrict', copy=False,
                        domain=[('instructor', '=', True)],
                        readonly=True, states={'draft': [('readonly', False)], 'approve': [('readonly', False)], 'confirm': [('readonly', False)]})
    location_id = fields.Many2one(comodel_name='res.partner', ondelete='restrict',
                        readonly=True, states={'draft': [('readonly', False)], 'approve': [('readonly', False)]})
    code = fields.Char(string='Code', size=32,
                          readonly=True, states={'draft': [('readonly', False)]})
    start_date = fields.Datetime(string='Start Date', required=True,
                                readonly=True, states={'draft': [('readonly', False)]})
    end_date = fields.Datetime(string='End Date', required=True,
                                  readonly=True, states={'draft': [('readonly', False)]})
    avail_seat_per = fields.Float(string='Avaliable Seats (%)', store=False,
                        compute='_compute_booked_seats')
    max_seats = fields.Integer(string='Maximum Seats',
                              readonly=True, states={'draft': [('readonly', False)], 'approve': [('readonly', False)], 'confirm': [('readonly', False)]})
    min_seats = fields.Integer(string='Minimum Required Seats',
                              readonly=True, states={'draft': [('readonly', False)], 'approve': [('readonly', False)], 'confirm': [('readonly', False)]})
    booked_seats = fields.Integer(string='Reserved Seats', store=False,
                        compute='_compute_booked_seats')
    syllabus_notes = fields.Html(string='Syllabus')
    count_attendee = fields.Integer(string='# Attendees', store=False, compute='_compute_syllabus_notes')
    attendees_ids = fields.One2many(comodel_name='openacademy.attendees',
                        inverse_name='session_id', string='Attendees',
                        readonly=True, states={'approve': [('readonly', False)], 'confirm': [('readonly', False)]})
    state = fields.Selection(selection=[
                            ('draft', 'New'),
                            ('approve', 'Approved'),
                            ('confirm', 'Confirmed'),
                            ('cancel', 'Cancelled'),
                            ('done', 'Done'),
                        ], string='State', default='draft')
    _sql_constraints = [
        ('openacademy_Session_unique_code', 'UNIQUE (code)', 'Code must be unique !'),
    ]
    
    @api.onchange('start_date')
    def onchange_start_date(self):
        for record in self:
            if record.start_date:
                record.end_date = record.start_date + timedelta(days=1)
    
    @api.depends('attendees_ids')
    def _compute_syllabus_notes(self):
        for session in self:
            session.count_attendee = len(session.attendees_ids)
    
    @api.depends('max_seats', 'attendees_ids.seat_count', 'attendees_ids.state')
    def _compute_booked_seats(self):
        for record in self:
            """
            booked_seats = 0.0
            for att in record.attendees_ids:
                if att.state not in ('cancel', 'no'):
                    booked_seats += att.seat_count
            """
            booked_seats = sum(record.attendees_ids.filtered(lambda ati: ati.state not in ('cancel', 'no')).mapped('seat_count'))
            record.booked_seats = booked_seats
            if record.max_seats > 0:
                record.avail_seat_per = (float(record.max_seats - booked_seats)/float(record.max_seats))*100.0
            
    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
        for session in self:
            if session.start_date > session.end_date:
                raise exceptions.ValidationError(_('Start date "%s" can not be after end date %s"')%(session.start_date, session.end_date))

    @api.model_create_multi          
    def create(self, vals_list):
        _logger.info('*'*50)
        _logger.info(vals_list)
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

    def action_approve(self):
        for session in self:
            session.state = 'approve'

    def action_confirm(self):
        for session in self:
            session.state = 'confirm'

    def action_reset(self):
        for session in self:
            session.state = 'draft'
            
    def action_cancel(self):
        for session in self:
            session.state = 'cancel'

    def action_done(self):
        for session in self:
            session.state = 'done'
            
    def action_open_attendee(self):
        self.ensure_one()
        #action_id = self.env.ref('openacademy.action_openacademy_attendees_views')
        #action_vals = action_id.read()[0]
        #action_vals.update({'domain': [('session_id', '=', self.id)]})
        action_vals = {
            'name': 'Attendees',
            'type': 'ir.actions.act_window',
            'res_model': 'openacademy.attendees',
            'views': [[self.env.ref('openacademy.view_openacademy_attendees_tree').id, "tree"], [self.env.ref('openacademy.view_openacademy_attendees_form').id, "form"]],
            'domain': [('session_id', '=', self.id)],
            'target': 'current'
        }
        _logger.info(action_vals)
        return action_vals