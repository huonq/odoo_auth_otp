import pyotp
from odoo import models
from odoo import fields


class User(models.Model):
    _inherit = 'res.users'

    otp_status = fields.Selection([
        ('1', 'Enable'),
        ('0', 'Disable')
    ],
        string='OTP Activate', default='0')
    otp_key = fields.Char()

    def check_otp(self, otp):
        totp = pyotp.TOTP(self.otp_key)
        print("\033[92m ------------------------- \033[0m")
        print(totp.now())
        print("\033[92m ------------------------- \033[0m")
        return totp.verify(otp)
