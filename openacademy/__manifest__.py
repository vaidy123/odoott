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
    'depends': ['contacts'],

    # always loaded
    'data': [
        'views/openacademy_course_views.xml',
        'views/res_partner_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        #'demo/openacademy_course_demo.xml',
    ],
}