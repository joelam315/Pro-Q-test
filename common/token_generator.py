from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six
from django.utils import timezone


class TokenGenerator(PasswordResetTokenGenerator):
    """ this class is used to generate a unique token to identify the user """

    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.is_active)
        )


account_activation_token = TokenGenerator()
