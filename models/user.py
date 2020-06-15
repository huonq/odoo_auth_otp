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
    otp_key = fields.Char(string='OTP Key')
    qr_code = fields.Binary(string="QR Code", attachment=True, store=True)

    def check_otp(self, otp):
        totp = pyotp.TOTP(self.otp_key)
        return totp.verify(otp)

    @api.onchange('otp_status')
    def generate_otp_key(self):
        key = pyotp.random_base32()
        for rec in self:
            rec.otp_key = str(key)

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
