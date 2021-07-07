from django.utils.translation import ugettext_lazy as _


class EmailAlreadyExistsError(Exception):
    message = _("An account with this email already exists.")


class PhoneAlreadyExistsError(Exception):
    message = _("An account with this phone number already exists.")
