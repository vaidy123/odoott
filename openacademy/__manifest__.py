# -*- coding: utf-8 -*-
{
    'name': "OpenAcademy",

    'summary': """Session, Trainings, Attendance""",

    'description': """
""",
    'author': "Odoo, Inc",
    'website': "https://www.odoo.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Academy',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['contacts', 'web_map', 'website'],

    # always loaded
    'data': [
        'security/openacdemy_security.xml',
        'security/ir.model.access.csv',

        'views/openacademy_menu_views.xml',
        'views/openacademy_course_views.xml',
        'views/openacademy_session_views.xml',
        'views/openacademy_attendees_views.xml',
        'views/res_partner_views.xml',
        'views/templates.xml',
        
        'wizard/wizard_invite_attendee_view.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/openacademy_demo.xml',
    ],
}