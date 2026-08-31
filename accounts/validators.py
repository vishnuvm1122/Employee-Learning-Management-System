import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class ASCIIUsernameValidator:
    regex = r'^[\w.@+-]+\Z'

    def __call__(self, value):
        if not re.match(self.regex, value):
            raise ValidationError(
                _("Enter a valid username. Only letters, digits and @/./+/-/_ allowed."),
                code="invalid",
            )