from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six


class AccountVerificationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.password) + six.text_type(timestamp) +
            six.text_type(user.profile.email_confirmed)
        )


account_verification_token = AccountVerificationTokenGenerator()
