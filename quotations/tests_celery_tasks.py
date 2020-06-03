from django.test import TestCase
from django.test.utils import override_settings

from quotations.tasks import (send_email, send_quotation_email,
                            send_quotation_email_cancel)
from quotations.tests import QuotationCreateTest


class TestSendMailOnQuotationCreationTask(QuotationCreateTest, TestCase):

    @override_settings(CELERY_EAGER_PROPAGATES_EXCEPTIONS=True,
                       CELERY_ALWAYS_EAGER=True,
                       BROKER_BACKEND='memory')
    def test_send_mail_on_quotation_creation_task(self):
        task = send_email.apply((self.quotation.id, [self.user.id, self.user1.id]))
        self.assertEqual('SUCCESS', task.state)

        task = send_quotation_email.apply((self.quotation.id,))
        self.assertEqual('SUCCESS', task.state)

        task = send_quotation_email_cancel.apply((self.quotation.id,))
        self.assertEqual('SUCCESS', task.state)
