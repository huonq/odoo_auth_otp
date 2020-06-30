import pyotp
import qrcode
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
    view_token = fields.Char()

    def check_otp(self, otp):
        totp = pyotp.TOTP(self.otp_key)
        return totp.verify(otp)

    @api.onchange('otp_key')
    def generate_qr_code(self):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        data = pyotp.totp.TOTP(self.otp_key).provisioning_uri(self.email, issuer_name="Secure App")
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image()
        temp = BytesIO()
        img.save(temp, format="PNG")
        qr_image = base64.b64encode(temp.getvalue())
        self.qr_code = qr_image

    def regen_code(self):
        key = pyotp.random_base32()
        for rec in self:
            rec.otp_key = str(key)

    def send_code(self):
        print("\033[92m ------------------------- \033[0m")
        print("tteetete!!!!!!!!!!!!!!!")
        print("\033[92m ------------------------- \033[0m")
        template_obj = self.env['mail.template'].sudo().search([('name', '=', 'Order tracking mail template')],
                                                               limit=1)
        body = template_obj.body_html
        body = body.replace('__customer', self.name)
        body = body.replace('__company', 'IMUSNANO')
        body = body.replace('__link', "demodemo")
        if template_obj:
            mail_values = {
                'subject': template_obj.subject,
                'subject': "Detail of order ",
                'body_html': body,
                'email_to': self.email,
                'email_cc': '',
                'email_from': 'nqhuong_erp@demo.vn',
            }
            create_and_send_email = self.env['mail.mail'].sudo().create(mail_values).send()
