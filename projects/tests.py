from datetime import datetime, timedelta

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from companies.models import Company
from common.models import Address, Attachments, Comment, User
from projects.models import Project, ProjectHistory
from teams.models import Teams


class ProjectCreateTest(object):

    def setUp(self):
        self.user = User.objects.create(
            first_name="johnProject", username='johnDoeProject', email='johnDoeProject@example.com', role='ADMIN')
        self.user.set_password('password')
        self.user.save()

        self.user1 = User.objects.create(
            first_name="janeProject",
            username='janeDoeProject',
            email='janeDoeProject@example.com',
            role="USER",
            has_sales_access=True)
        self.user1.set_password('password')
        self.user1.save()

        self.user2 = User.objects.create(
            first_name="joeProject",
            username='joeProject',
            email='joeProject@example.com',
            role="USER",
            has_sales_access=True)
        self.user2.set_password('password')
        self.user2.save()

        self.team_dev = Teams.objects.create(name='projects teams')
        self.team_dev.users.add(self.user2.id)

        self.company = Company.objects.create(
            name="john project", email="johnDoeProject@example.com", phone="123456789",
            billing_address_line="", billing_street="street name",
            billing_city="city name",
            billing_state="state", billing_postcode="1234",
            billing_country="US",
            website="www.example.como", created_by=self.user, status="open",
            industry="SOFTWARE", description="Testing")
        self.company.assigned_to.add(self.user1.id)

        self.from_address = Address.objects.create(
            street="from street number",
            city="from city",
            state="from state",
            postcode=12346, country="IN")

        self.to_address = Address.objects.create(
            street="to street number",
            city="to city",
            state="to state",
            postcode=12346, country="IN")

        self.project = Project.objects.create(
            project_title='project title',
            project_number='project number',
            currency='USD',
            email='projectTitle@email.com',
            due_date=(datetime.now() + timedelta(days=2)).strftime('%Y-%m-%d'),
            total_amount='1000',
            created_by=self.user,
            from_address=self.from_address,
            to_address=self.to_address,
        )
        self.project.assigned_to.add(self.user1.id)
        self.project.companies.add(self.company.id)

        self.project_history = ProjectHistory.objects.create(
            project_title='project title',
            project_number='project number',
            currency='USD',
            email='projectTitle@email.com',
            due_date=(datetime.now() + timedelta(days=2)).strftime('%Y-%m-%d'),
            total_amount='1000',
            from_address=self.from_address,
            to_address=self.to_address,
            project=self.project
        )

        self.project_1 = Project.objects.create(
            project_title='project title',
            project_number='project_1 number',
            currency='USD',
            email='projectTitle@email.com',
            due_date=(datetime.now() + timedelta(days=2)).strftime('%Y-%m-%d'),
            total_amount='1000',
            created_by=self.user1
        )
        self.project_1.assigned_to.add(self.user2.id)
        self.project_1.assigned_to.add(self.user1.id)
        self.project_1.companies.add(self.company.id)

        self.comment = Comment.objects.create(
            comment='test comment', project=self.project,
            commented_by=self.user
        )
        self.attachment = Attachments.objects.create(
            attachment='image.png', project=self.project,
            created_by=self.user
        )


class ProjectListTestCase(ProjectCreateTest, TestCase):

    def test_projects_list(self):
        self.client.login(email='johnDoeProject@example.com',
                          password='password')
        response = self.client.get(reverse('projects:projects_list'))
        self.assertEqual(response.status_code, 200)

        self.client.login(email='janeDoeProject@example.com',
                          password='password')
        response = self.client.get(reverse('projects:projects_list'))
        self.assertEqual(response.status_code, 200)

        data = {
            'project_title_number': 'title',
            'created_by': self.user.id,
            'assigned_to': self.user1.id,
            'status': 'Draft',
            'total_amount': '1000',
        }
        self.client.login(email='johnDoeProject@example.com',
                          password='password')
        response = self.client.post(reverse('projects:projects_list'), data)
        self.assertEqual(response.status_code, 200)

        self.client.login(email='janeDoeProject@example.com',
                          password='password')
        response = self.client.post(reverse('projects:projects_list'), data)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(str(self.project), 'project number')
        self.assertEqual(str(self.project.formatted_rate()), '0 USD')
        self.assertEqual(str(self.project.formatted_total_quantity()), '0 Hours')

        self.assertEqual(str(self.project_history), 'project number')
        self.assertEqual(str(self.project_history.formatted_rate()), '0 USD')
        self.assertEqual(str(self.project_history.formatted_total_quantity()), '0 Hours')
        self.assertEqual(str(self.project_history.formatted_total_amount()), 'USD 1000')

        self.assertTrue(self.project_history.created_on_arrow in ['just now' or 'seconds ago'])



class ProjectAddTestCase(ProjectCreateTest, TestCase):

    def test_projects_create(self):
        self.client.login(email='johnDoeProject@example.com',
                          password='password')
        response = self.client.get(reverse('projects:projects_create'))
        self.assertEqual(response.status_code, 200)

        data = {
            'project_title': 'project title create',
            'status': 'Draft',
            'project_number': 'project number',
            'currency': 'INR',
            'email': 'project@example.com',
            'due_data': (datetime.now() + timedelta(days=2)).strftime('%Y-%m-%d'),
            'total_amount': '1234',
            'teams': self.team_dev.id,
            'companies': self.company.id,
            'assigned_to': self.user1.id,
        }

        response = self.client.post(reverse('projects:projects_create'), data)
        self.assertEqual(response.status_code, 200)

        data = {
            'project_title': 'project title',
            'status': 'Draft',
            'project_number': 'INV123',
            'currency': 'INR',
            'email': 'project@example.com',
            'due_date': (datetime.now() + timedelta(days=2)).strftime('%Y-%m-%d'),
            'total_amount': '1234',
            'teams': self.team_dev.id,
            'companies': self.company.id,
            'assigned_to': self.user1.id,
            'quantity': 0,
        }
        response = self.client.post(reverse('projects:projects_create'), data)
        self.assertEqual(response.status_code, 200)

        data = {
            'project_title': 'project title',
            'status': 'Draft',
            'project_number': 'INV1234',
            'currency': 'INR',
            'email': 'project@example.com',
            'due_date': (datetime.now() + timedelta(days=2)).strftime('%Y-%m-%d'),
            'total_amount': '1234',
            'teams': self.team_dev.id,
            'companies': self.company.id,
            'assigned_to': self.user1.id,
            'quantity': 0,
            'from_company': self.company.id
        }
        response = self.client.post(reverse('projects:projects_create'), data)
        self.assertEqual(response.status_code, 200)

        self.client.login(email='janeDoeProject@example.com',
                          password='password')
        response = self.client.get(reverse('projects:projects_list'))
        self.assertEqual(response.status_code, 200)


class ProjectDetailTestCase(ProjectCreateTest, TestCase):

    def test_projects_detail(self):
        self.client.login(email='johnDoeProject@example.com',
                          password='password')
        response = self.client.get(
            reverse('projects:project_details', args=(self.project.id,)))
        self.assertEqual(response.status_code, 200)

        self.client.login(email='janeDoeProject@example.com',
                          password='password')
        response = self.client.get(
            reverse('projects:project_details', args=(self.project.id,)))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(
            reverse('projects:project_details', args=(self.project_1.id,)))
        self.assertEqual(response.status_code, 200)

        self.client.login(email='joeProject@example.com',
                          password='password')
        response = self.client.get(
            reverse('projects:project_details', args=(self.project.id,)))
        self.assertEqual(response.status_code, 403)


class ProjectEditTestCase(ProjectCreateTest, TestCase):

    def test_projects_edit(self):
        self.client.login(email='johnDoeProject@example.com',
                          password='password')
        response = self.client.get(
            reverse('projects:project_edit', args=(self.project.id,)))
        self.assertEqual(response.status_code, 200)

        self.client.login(email='janeDoeProject@example.com',
                          password='password')
        response = self.client.get(
            reverse('projects:project_edit', args=(self.project_1.id,)))
        self.assertEqual(response.status_code, 200)

        self.client.login(email='joeProject@example.com',
                          password='password')
        response = self.client.get(
            reverse('projects:project_edit', args=(self.project.id,)))
        self.assertEqual(response.status_code, 403)

        data = {
            'project_title': 'project title',
            'status': 'Draft',
            'project_number': 'INV1234',
            'currency': 'INR',
            'email': 'project@example.com',
            'due_date': (datetime.now() + timedelta(days=2)).strftime('%Y-%m-%d'),
            'total_amount': '1234',
            'teams': self.team_dev.id,
            'companies': self.company.id,
            'assigned_to': self.user1.id,
            'quantity': 0,
            'from_company': self.company.id,
            'from-address_line': '',
            'from-street': '',
            'from-city': '',
            'from-state': '',
            'from-postcode': '',
            'from-country': '',
            'to-address_line': '',
            'to-street': '',
            'to-city': '',
            'to-state': '',
            'to-postcode': '',
            'to-country': '',
        }

        self.client.login(email='johnDoeProject@example.com',
                          password='password')
        response = self.client.post(
            reverse('projects:project_edit', args=(self.project.id,)), data)
        self.assertEqual(response.status_code, 200)

        data.pop('from_company')
        self.client.login(email='johnDoeProject@example.com',
                          password='password')
        response = self.client.post(
            reverse('projects:project_edit', args=(self.project.id,)), data)
        self.assertEqual(response.status_code, 200)

        data.pop('project_number')
        self.client.login(email='johnDoeProject@example.com',
                          password='password')
        response = self.client.post(
            reverse('projects:project_edit', args=(self.project.id,)), data)
        self.assertEqual(response.status_code, 200)


class ProjectSendMailTestCase(ProjectCreateTest, TestCase):

    def test_projects_send_mail(self):

        self.client.login(email='joeProject@example.com',
                          password='password')
        response = self.client.get(
            reverse('projects:project_send_mail', args=(self.project_1.id,)))
        self.assertEqual(response.status_code, 403)

        self.client.login(email='janeDoeProject@example.com',
                          password='password')
        response = self.client.get(
            reverse('projects:project_send_mail', args=(self.project_1.id,)))
        self.assertEqual(response.status_code, 302)


class ProjectChangeStatusPaidTestCase(ProjectCreateTest, TestCase):

    def test_projects_change_status_to_paid(self):

        self.client.login(email='joeProject@example.com',
                          password='password')
        response = self.client.get(
            reverse('projects:project_change_status_paid', args=(self.project_1.id,)))
        self.assertEqual(response.status_code, 403)

        self.client.login(email='janeDoeProject@example.com',
                          password='password')
        response = self.client.get(
            reverse('projects:project_change_status_paid', args=(self.project_1.id,)))
        self.assertEqual(response.status_code, 302)


class ProjectChangeStatusCancelledTestCase(ProjectCreateTest, TestCase):

    def test_projects_change_status_to_cancelled(self):

        self.client.login(email='joeProject@example.com',
                          password='password')
        response = self.client.get(
            reverse('projects:project_change_status_cancelled', args=(self.project_1.id,)))
        self.assertEqual(response.status_code, 403)

        self.client.login(email='janeDoeProject@example.com',
                          password='password')
        response = self.client.get(
            reverse('projects:project_change_status_cancelled', args=(self.project_1.id,)))
        self.assertEqual(response.status_code, 302)


class ProjectDownloadTestCase(ProjectCreateTest, TestCase):

    def test_projects_download(self):

        self.client.login(email='joeProject@example.com',
                          password='password')
        response = self.client.get(
            reverse('projects:project_download', args=(self.project.id,)))
        self.assertEqual(response.status_code, 403)

        # self.client.login(email='johnDoeProject@example.com',
        #                   password='password')
        # response = self.client.get(
        #     reverse('projects:project_download', args=(self.project_1.id,)))
        # self.assertEqual(response.status_code, 200)


class AddCommentTestCase(ProjectCreateTest, TestCase):

    def test_project_add_comment(self):

        self.client.login(email='johnDoeProject@example.com', password='password')
        data = {
            'comment': '',
            'project_id': self.project.id,
        }
        response = self.client.post(
            reverse('projects:add_comment'), data)
        self.assertEqual(response.status_code, 200)

        data = {
            'comment': 'test comment project',
            'project_id': self.project.id,
        }
        response = self.client.post(
            reverse('projects:add_comment'), data)
        self.assertEqual(response.status_code, 200)

        self.client.login(email='janeDoeProject@example.com', password='password')
        response = self.client.post(
            reverse('projects:add_comment'), data)
        self.assertEqual(response.status_code, 200)


class UpdateCommentTestCase(ProjectCreateTest, TestCase):

    def test_project_update_comment(self):

        self.client.login(email='johnDoeProject@example.com', password='password')
        data = {
            'commentid': self.comment.id,
            'project_id': self.project.id,
            'comment': ''
        }
        response = self.client.post(
            reverse('projects:edit_comment'), data)
        self.assertEqual(response.status_code, 200)

        data = {
            'comment': 'test comment',
            'commentid': self.comment.id,
            'project_id': self.project.id,
        }
        response = self.client.post(
            reverse('projects:edit_comment'), data)
        self.assertEqual(response.status_code, 200)

        self.client.login(email='janeDoeProject@example.com', password='password')
        response = self.client.post(
            reverse('projects:edit_comment'), data)
        self.assertEqual(response.status_code, 200)


class DeleteCommentTestCase(ProjectCreateTest, TestCase):

    def test_project_delete_comment(self):

        data = {
            'comment_id': self.comment.id,
        }
        self.client.login(email='janeDoeProject@example.com', password='password')
        response = self.client.post(
            reverse('projects:remove_comment'), data)
        self.assertEqual(response.status_code, 200)

        self.client.login(email='johnDoeProject@example.com', password='password')
        response = self.client.post(
            reverse('projects:remove_comment'), data)
        self.assertEqual(response.status_code, 200)


class AddAttachmentTestCase(ProjectCreateTest, TestCase):

    def test_project_add_attachment(self):

        data = {
            'attachment': SimpleUploadedFile('file_name.txt', bytes('file contents.', 'utf-8')),
            'project_id': self.project.id
        }
        self.client.login(email='johnDoeProject@example.com', password='password')
        response = self.client.post(
            reverse('projects:add_attachment'), data)
        self.assertEqual(response.status_code, 200)

        self.client.login(email='janeDoeProject@example.com', password='password')
        response = self.client.post(
            reverse('projects:add_attachment'), data)
        self.assertEqual(response.status_code, 200)

        data = {
            'attachment': '',
            'project_id': self.project.id
        }
        self.client.login(email='johnDoeProject@example.com', password='password')
        response = self.client.post(
            reverse('projects:add_attachment'), data)
        self.assertEqual(response.status_code, 200)


class DeleteAttachmentTestCase(ProjectCreateTest, TestCase):

    def test_project_delete_attachment(self):

        data = {
            'attachment_id': self.attachment.id,
        }
        self.client.login(email='janeDoeProject@example.com', password='password')
        response = self.client.post(
            reverse('projects:remove_attachment'), data)
        self.assertEqual(response.status_code, 200)

        self.client.login(email='johnDoeProject@example.com', password='password')
        response = self.client.post(
            reverse('projects:remove_attachment'), data)
        self.assertEqual(response.status_code, 200)


class ProjectDeleteTestCase(ProjectCreateTest, TestCase):

    def test_projects_delete(self):

        self.client.login(email='joeProject@example.com',
                          password='password')
        response = self.client.get(
            reverse('projects:project_delete', args=(self.project_1.id,)))
        self.assertEqual(response.status_code, 403)

        self.client.login(email='janeDoeProject@example.com',
                          password='password')
        response = self.client.get(
            reverse('projects:project_delete', args=(self.project_1.id,)))
        self.assertEqual(response.status_code, 302)

        self.client.login(email='johnDoeProject@example.com',
                          password='password')
        self.project.status = 'Sent'
        self.project.is_email_sent = False
        self.project.save()
        self.assertEqual(self.project.is_sent(), True)
        self.project.status = 'Sent'
        self.project.is_email_sent = True
        self.project.save()
        self.assertEqual(self.project.is_resent(), True)
        self.assertEqual(self.project.is_draft(), False)
        self.project.status = 'Paid'
        self.project.save()
        self.assertEqual(self.project.is_paid_or_cancelled(), True)
        response = self.client.get(
            reverse('projects:project_delete', args=(self.project.id,)) + '?view_company={}'.format(self.company.id,))
        self.assertEqual(response.status_code, 302)
