# -*- coding: utf-8 -*-
# from odoo import http


# class Otp(http.Controller):
#     @http.route('/otp/otp/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/otp/otp/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('otp.listing', {
#             'root': '/otp/otp',
#             'objects': http.request.env['otp.otp'].search([]),
#         })

#     @http.route('/otp/otp/objects/<model("otp.otp"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('otp.object', {
#             'object': obj
#         })
