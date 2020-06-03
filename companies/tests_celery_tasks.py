from datetime import datetime, timedelta

from django.test import TestCase
from django.test.utils import override_settings

from companies.models import Email
from companies.tasks import (send_email, send_email_to_assigned_user,
                            send_scheduled_emails)
from companies.tests import CompanyCreateTest


class TestCeleryTasks(CompanyCreateTest, TestCase):

    @override_settings(CELERY_EAGER_PROPAGATES_EXCEPTIONS=True,
                       CELERY_ALWAYS_EAGER=True,
                       BROKER_BACKEND='memory')
    def test_celery_tasks(self):
        email_scheduled = Email.objects.create(
            message_subject='message subject', message_body='message body',
            scheduled_later=True, timezone='Asia/Kolkata',
            from_company=self.company,
            scheduled_date_time=(datetime.now() - timedelta(minutes=5)),
            from_email='from@email.com'
        )
        email_scheduled.recipients.add(self.contact.id, self.contact_user1.id)
        task = send_scheduled_emails.apply()
        self.assertEqual('SUCCESS', task.state)

        task = send_email.apply((email_scheduled.id,))
        self.assertEqual('SUCCESS', task.state)

        task = send_email_to_assigned_user.apply(
            ([self.user.id, self.user1.id, ], self.company.id,),)
        self.assertEqual('SUCCESS', task.state)
