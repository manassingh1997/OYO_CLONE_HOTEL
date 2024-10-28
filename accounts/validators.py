import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class CustomPasswordValidator:
    def validate(self,password,user=None):
        if len(password)<8:
            raise ValidationError(
                _("Password must be at least 8 characters long."),
                code = 'password_too_short',
            )
        if not re.search(r'[A-Z]',password):
            raise ValidationError(
                _("Password must contain atleat one uppercase letter"),
                code = 'no_uppercase',
            )
        if not re.search(r'[a-z]',password):
            raise ValidationError(
                _("Password must contain atleast one lowercase letter"),
                code = 'no_lowercase',
            )
        if not re.search(r'\d',password):
            raise ValidationError(
                _("Password must contain atleast one number"),
                code = "no_number",
            )
        if not re.search(r'[!@#$%^&*()_:{}|<>]',password):
            raise ValidationError(
                _("Password must contain atleat one speacial character"),
                code ='no_special_char',
            )
        
    def get_help_text(self):
        return _(
            "Your password must contain at least 8 characters, including"
            "an uppercase letter, a lowercase letter, a number and a special character."
        )