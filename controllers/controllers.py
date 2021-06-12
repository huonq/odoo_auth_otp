# -*- coding: utf-8 -*-
from odoo.addons.web.controllers.main import Home, ensure_db

from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo.http import request
from odoo import http
from odoo import _
import odoo
import base64


class Home(Home):
    @http.route('/web/login', type='http', auth="none")
    def web_login(self, redirect=None, **kw):
        ensure_db()
        request.params['login_success'] = False
        if request.httprequest.method == 'GET' and redirect and request.session.uid:
            return http.redirect_with_hash(redirect)

        if not request.uid:
            request.uid = odoo.SUPERUSER_ID

        values = request.params.copy()
        try:
            values['databases'] = http.db_list()
        except odoo.exceptions.AccessDenied:
            values['databases'] = None

        if request.httprequest.method == 'POST':
            old_uid = request.uid
            user = request.env['res.users'].sudo().search([('email', '=', request.params['login'])])
            if user:
                if user.check_otp(request.params['otp_code']):
                    try:
                        uid = request.session.authenticate(request.session.db, request.params['login'],
                                                           request.params['password'])
                        request.params['login_success'] = True
                        return http.redirect_with_hash(self._login_redirect(uid, redirect=redirect))
                    except odoo.exceptions.AccessDenied as e:
                        request.uid = old_uid
                        if e.args == odoo.exceptions.AccessDenied().args:
                            values['error'] = _("Wrong login/password")
                        else:
                            values['error'] = e.args[0]
                else:
                    request.uid = old_uid
                    values['error'] = _("Wrong otp code")
            else:
                request.uid = old_uid
                values['error'] = _("Wrong login/password")
        else:
            if 'error' in request.params and request.params.get('error') == 'access':
                values['error'] = _('Only employee can access this database. Please contact the administrator.')

        if 'login' not in values and request.session.get('auth_login'):
            values['login'] = request.session.get('auth_login')

        if not odoo.tools.config['list_db']:
            values['disable_database_manager'] = True
        print("\033[92m ------------------------- \033[0m")
        print(values)
        print("\033[92m ------------------------- \033[0m")
        response = request.render('web.login', values)
        response.headers['X-Frame-Options'] = 'DENY'
        return response


class QRgen(http.Controller):
    @http.route('/get_qr', type='http', auth="none")
    def gen_qr(self, tk):
        try:
            values = []
            user = http.request.env['res.users'].sudo().search([('view_token', '=', tk)])
            if user:
                values = request.params.copy()
                try:
                    values['databases'] = http.db_list()
                except odoo.exceptions.AccessDenied:
                    values['databases'] = None
                values['d'] = user.qr_code
                response = request.render('otp.qr_get', values)
                return response
            else:
                return "Empty"
        except:
            return "Error!"


class heh(CustomerPortal):
    def _prepare_portal_layout_values(self):
        # get customer sales rep
        sales_user = False
        partner = request.env.user.partner_id
        if partner.user_id and not partner.user_id._is_public():
            sales_user = partner.user_id

        return {
            'sales_user': sales_user,
            'page_name': 'home',
            'archive_groups': [],
        }

    @http.route('/get_otp', type='http', auth="public", website=True)
    def home(self, **kw):
        values = self._prepare_portal_layout_values()
        tk = kw.get('tk')
        user = http.request.env['res.users'].sudo().search([('view_token', '=', tk)])
        values['flag'] = False
        if user:
            values = request.params.copy()
            try:
                values['databases'] = http.db_list()
            except odoo.exceptions.AccessDenied:
                values['databases'] = None
            values['d'] = user.qr_code
            values['s'] = user.get_string()
            values['flag'] = True
            user.view_token = ""
            return request.render("odoo_auth_otp.get_qr2", values)
        else:
            return request.render("odoo_auth_otp.get_qr2", values)
