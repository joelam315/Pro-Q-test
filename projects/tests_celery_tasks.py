from django.test import TestCase
from django.test.utils import override_settings

from projects.tasks import (send_email, send_project_email,
                            send_project_email_cancel)
from projects.tests import ProjectCreateTest


class TestSendMailOnProjectCreationTask(ProjectCreateTest, TestCase):

    @override_settings(CELERY_EAGER_PROPAGATES_EXCEPTIONS=True,
                       CELERY_ALWAYS_EAGER=True,
                       BROKER_BACKEND='memory')
    def test_send_mail_on_project_creation_task(self):
        task = send_email.apply((self.project.id, [self.user.id, self.user1.id]))
        self.assertEqual('SUCCESS', task.state)

        task = send_project_email.apply((self.project.id,))
        self.assertEqual('SUCCESS', task.state)

        task = send_project_email_cancel.apply((self.project.id,))
        self.assertEqual('SUCCESS', task.state)
