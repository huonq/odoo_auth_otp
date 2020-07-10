import pyotp
import qrcode
import random
import string
import base64
from odoo import models
from odoo import fields
from odoo import api
from io import BytesIO


class User(models.Model):
    _inherit = 'res.users'

    otp_status = fields.Selection([
        ('1', 'Enable'),
        ('0', 'Disable')
    ],
        string='OTP Activate', default='0')
    otp_key = fields.Char(string='OTP Key', store=True)
    qr_code = fields.Binary(string="QR Code", attachment=True, store=True)
    view_token = fields.Char(default="")

    def check_otp(self, otp):
        key = self.otp_key
        totp = pyotp.TOTP(key)
        return totp.verify(otp)

    def get_string(self):
        return pyotp.totp.TOTP(self.otp_key).provisioning_uri(self.email, issuer_name=self.name)

    def regen_code(self):
        key = pyotp.random_base32()
        for rec in self:
            rec.otp_key = str(key)
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        data = pyotp.totp.TOTP(self.otp_key).provisioning_uri(self.email, issuer_name=self.name)
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image()
        temp = BytesIO()
        img.save(temp, format="PNG")
        qr_image = base64.b64encode(temp.getvalue())
        self.qr_code = qr_image

    def send_code(self):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        template_obj = self.env['mail.template'].sudo().search([('name', '=', 'Mail OTP')], limit=1)
        self.gen_token_view()
        body = template_obj.body_html
        body = body.replace('__customer', self.name)
        body = body.replace('__company', 'TTCN Demo')
        body = body.replace('__link', base_url + "/get_otp?tk=" + self.view_token)
        if template_obj:
            mail_values = {
                'subject': template_obj.subject,
                'subject': "OTP key for " + self.email,
                'body_html': body,
                'email_to': self.email,
                'email_cc': '',
                'email_from': 'nqhuong_erp@demo.vn',
            }
            create_and_send_email = self.env['mail.mail'].sudo().create(mail_values).send()

    def gen_token_view(self):
        letters = string.ascii_lowercase
        result_str = ''.join(random.choice(letters) for i in range(32))
        for r in self:
            r.view_token = result_str
