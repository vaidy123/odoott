# -*- coding: utf-8 -*-
import logging
from odoo import models, fields, api, exceptions, _

_logger = logging.getLogger(__name__)
    
class OpenAcademyAttendees(models.Model):
    _name = 'openacademy.attendees'
    _description =  'OpenAcademy Attendees'
    
    sequence = fields.Integer(string='Sequence')
    name = fields.Char(string='Name', required=True, 
                        index=True, help='Enter your course title on this field.')
    session_id = fields.Many2one(comodel_name='openacademy.session', required=True)
    partner_id = fields.Many2one(comodel_name='res.partner', required=True,
                        string='Contact', ondelete='restrict', copy=False)
    seat_count = fields.Integer(string='Reserved Seats', default=1)
    state = fields.Selection(selection=[
                            ('invite', 'Invited'),
                            ('going', 'Going'),
                            ('maybe', 'Maybe'),
                            ('no', 'Declined'),
                            ('cancel', 'Cancelled'),
                        ], string='Status', default='invite')

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        for record in self:
            record.name = record.partner_id.display_name if record.partner_id else record.name