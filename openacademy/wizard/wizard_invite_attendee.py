# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _


class WizardInviteAttendee(models.TransientModel):
    _name = 'wizard.invite.attendee'
    _description = 'Wizard Invite Attendee'
    
    session_id = fields.Many2one(comodel_name='openacademy.session', string='Session')
    attendees_ids = fields.One2many(comodel_name='wizard.attendees.line',
                        inverse_name='wizard_id', string='Attendees')


class OpenAcademyAttendees(models.TransientModel):
    _name = 'wizard.attendees.line'
    _description =  'Wizard Attendees Lines'

    name = fields.Char(string='Name', required=True)
    wizard_id = fields.Many2one(comodel_name='wizard.invite.attendee', string='Wizard')
    partner_id = fields.Many2one(comodel_name='res.partner', required=True, string='Contact')
    seat_count = fields.Integer(string='Reserved Seats', default=1)
    
    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        for record in self:
            record.name = record.partner_id.display_name if record.partner_id else record.name