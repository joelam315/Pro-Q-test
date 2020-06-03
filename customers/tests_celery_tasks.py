from datetime import datetime, timedelta

from django.test import TestCase
from django.test.utils import override_settings

from customers.tasks import send_email_to_assigned_user
from customers.tests import CustomerObjectsCreation


class TestCeleryTasks(CustomerObjectsCreation, TestCase):

    @override_settings(CELERY_EAGER_PROPAGATES_EXCEPTIONS=True,
                       CELERY_ALWAYS_EAGER=True,
                       BROKER_BACKEND='memory')
    def test_celery_tasks(self):
        task = send_email_to_assigned_user.apply(
            ([self.user.id, self.user_customers_mp.id, ], self.customer.id,),)
        self.assertEqual('SUCCESS', task.state)
