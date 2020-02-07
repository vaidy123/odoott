# -*- coding: utf-8 -*-
import logging

from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class OpenAcademyController(http.Controller):
    
    @http.route([
      '/session',
      '/session/<int:session_id>',
       '/session/page/<int:page>',
    ], type='http', auth='public', website=True)
    def session(self, session_id=None, page=None, **post):
        if session_id:
            sesion_record = request.env['openacademy.session'].browse([session_id])
            return request.render('openacademy.session', {'session': sesion_record})
        else:
            session_records = request.env['openacademy.session'].search([])
            return request.render('openacademy.get_sessions', {'all_sessions': session_records})