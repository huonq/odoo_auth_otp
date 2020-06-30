# -*- coding: utf-8 -*-
{
    'name': "OTP Authencation",

    'summary': """
        Provide OTP authencation!""",

    'description': """
        Provide OTP authencation solution with soft otp on mobile phone.
    """,

    'author': "nqhuong",
    'website': "https://coderchan.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','mail'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'data/mail_template.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
