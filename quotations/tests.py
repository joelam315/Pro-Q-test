from datetime import datetime, timedelta

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from companies.models import Company
from common.models import Address, Attachments, Comment, User
from quotations.models import Quotation, QuotationHistory
from teams.models import Teams


class QuotationCreateTest(object):

    def setUp(self):
        self.user = User.objects.create(
            first_name="johnQuotation", username='johnDoeQuotation', email='johnDoeQuotation@example.com', role='ADMIN')
        self.user.set_password('password')
        self.user.save()

        self.user1 = User.objects.create(
            first_name="janeQuotation",
            username='janeDoeQuotation',
            email='janeDoeQuotation@example.com',
            role="USER",
            has_sales_access=True)
        self.user1.set_password('password')
        self.user1.save()

        self.user2 = User.objects.create(
            first_name="joeQuotation",
            username='joeQuotation',
            email='joeQuotation@example.com',
            role="USER",
            has_sales_access=True)
        self.user2.set_password('password')
        self.user2.save()

        self.team_dev = Teams.objects.create(name='quotations teams')
        self.team_dev.users.add(self.user2.id)

        self.company = Company.objects.create(
            name="john quotation", email="johnDoeQuotation@example.com", phone="123456789",
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

        self.quotation = Quotation.objects.create(
            quotation_title='quotation title',
            quotation_number='quotation number',
            currency='USD',
            email='quotationTitle@email.com',
            due_date=(datetime.now() + timedelta(days=2)).strftime('%Y-%m-%d'),
            total_amount='1000',
            created_by=self.user,
            from_address=self.from_address,
            to_address=self.to_address,
        )
        self.quotation.assigned_to.add(self.user1.id)
        self.quotation.companies.add(self.company.id)

        self.quotation_history = QuotationHistory.objects.create(
            quotation_title='quotation title',
            quotation_number='quotation number',
            currency='USD',
            email='quotationTitle@email.com',
            due_date=(datetime.now() + timedelta(days=2)).strftime('%Y-%m-%d'),
            total_amount='1000',
            from_address=self.from_address,
            to_address=self.to_address,
            quotation=self.quotation
        )

        self.quotation_1 = Quotation.objects.create(
            quotation_title='quotation title',
            quotation_number='quotation_1 number',
            currency='USD',
            email='quotationTitle@email.com',
            due_date=(datetime.now() + timedelta(days=2)).strftime('%Y-%m-%d'),
            total_amount='1000',
            created_by=self.user1
        )
        self.quotation_1.assigned_to.add(self.user2.id)
        self.quotation_1.assigned_to.add(self.user1.id)
        self.quotation_1.companies.add(self.company.id)

        self.comment = Comment.objects.create(
            comment='test comment', quotation=self.quotation,
            commented_by=self.user
        )
        self.attachment = Attachments.objects.create(
            attachment='image.png', quotation=self.quotation,
            created_by=self.user
        )


class QuotationListTestCase(QuotationCreateTest, TestCase):

    def test_quotations_list(self):
        self.client.login(email='johnDoeQuotation@example.com',
                          password='password')
        response = self.client.get(reverse('quotations:quotations_list'))
        self.assertEqual(response.status_code, 200)

        self.client.login(email='janeDoeQuotation@example.com',
                          password='password')
        response = self.client.get(reverse('quotations:quotations_list'))
        self.assertEqual(response.status_code, 200)

        data = {
            'quotation_title_number': 'title',
            'created_by': self.user.id,
            'assigned_to': self.user1.id,
            'status': 'Draft',
            'total_amount': '1000',
        }
        self.client.login(email='johnDoeQuotation@example.com',
                          password='password')
        response = self.client.post(reverse('quotations:quotations_list'), data)
        self.assertEqual(response.status_code, 200)

        self.client.login(email='janeDoeQuotation@example.com',
                          password='password')
        response = self.client.post(reverse('quotations:quotations_list'), data)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(str(self.quotation), 'quotation number')
        self.assertEqual(str(self.quotation.formatted_rate()), '0 USD')
        self.assertEqual(str(self.quotation.formatted_total_quantity()), '0 Hours')

        self.assertEqual(str(self.quotation_history), 'quotation number')
        self.assertEqual(str(self.quotation_history.formatted_rate()), '0 USD')
        self.assertEqual(str(self.quotation_history.formatted_total_quantity()), '0 Hours')
        self.assertEqual(str(self.quotation_history.formatted_total_amount()), 'USD 1000')

        self.assertTrue(self.quotation_history.created_on_arrow in ['just now' or 'seconds ago'])



class QuotationAddTestCase(QuotationCreateTest, TestCase):

    def test_quotations_create(self):
        self.client.login(email='johnDoeQuotation@example.com',
                          password='password')
        response = self.client.get(reverse('quotations:quotations_create'))
        self.assertEqual(response.status_code, 200)

        data = {
            'quotation_title': 'quotation title create',
            'status': 'Draft',
            'quotation_number': 'quotation number',
            'currency': 'INR',
            'email': 'quotation@example.com',
            'due_data': (datetime.now() + timedelta(days=2)).strftime('%Y-%m-%d'),
            'total_amount': '1234',
            'teams': self.team_dev.id,
            'companies': self.company.id,
            'assigned_to': self.user1.id,
        }

        response = self.client.post(reverse('quotations:quotations_create'), data)
        self.assertEqual(response.status_code, 200)

        data = {
            'quotation_title': 'quotation title',
            'status': 'Draft',
            'quotation_number': 'INV123',
            'currency': 'INR',
            'email': 'quotation@example.com',
            'due_date': (datetime.now() + timedelta(days=2)).strftime('%Y-%m-%d'),
            'total_amount': '1234',
            'teams': self.team_dev.id,
            'companies': self.company.id,
            'assigned_to': self.user1.id,
            'quantity': 0,
        }
        response = self.client.post(reverse('quotations:quotations_create'), data)
        self.assertEqual(response.status_code, 200)

        data = {
            'quotation_title': 'quotation title',
            'status': 'Draft',
            'quotation_number': 'INV1234',
            'currency': 'INR',
            'email': 'quotation@example.com',
            'due_date': (datetime.now() + timedelta(days=2)).strftime('%Y-%m-%d'),
            'total_amount': '1234',
            'teams': self.team_dev.id,
            'companies': self.company.id,
            'assigned_to': self.user1.id,
            'quantity': 0,
            'from_company': self.company.id
        }
        response = self.client.post(reverse('quotations:quotations_create'), data)
        self.assertEqual(response.status_code, 200)

        self.client.login(email='janeDoeQuotation@example.com',
                          password='password')
        response = self.client.get(reverse('quotations:quotations_list'))
        self.assertEqual(response.status_code, 200)


class QuotationDetailTestCase(QuotationCreateTest, TestCase):

    def test_quotations_detail(self):
        self.client.login(email='johnDoeQuotation@example.com',
                          password='password')
        response = self.client.get(
            reverse('quotations:quotation_details', args=(self.quotation.id,)))
        self.assertEqual(response.status_code, 200)

        self.client.login(email='janeDoeQuotation@example.com',
                          password='password')
        response = self.client.get(
            reverse('quotations:quotation_details', args=(self.quotation.id,)))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(
            reverse('quotations:quotation_details', args=(self.quotation_1.id,)))
        self.assertEqual(response.status_code, 200)

        self.client.login(email='joeQuotation@example.com',
                          password='password')
        response = self.client.get(
            reverse('quotations:quotation_details', args=(self.quotation.id,)))
        self.assertEqual(response.status_code, 403)


class QuotationEditTestCase(QuotationCreateTest, TestCase):

    def test_quotations_edit(self):
        self.client.login(email='johnDoeQuotation@example.com',
                          password='password')
        response = self.client.get(
            reverse('quotations:quotation_edit', args=(self.quotation.id,)))
        self.assertEqual(response.status_code, 200)

        self.client.login(email='janeDoeQuotation@example.com',
                          password='password')
        response = self.client.get(
            reverse('quotations:quotation_edit', args=(self.quotation_1.id,)))
        self.assertEqual(response.status_code, 200)

        self.client.login(email='joeQuotation@example.com',
                          password='password')
        response = self.client.get(
            reverse('quotations:quotation_edit', args=(self.quotation.id,)))
        self.assertEqual(response.status_code, 403)

        data = {
            'quotation_title': 'quotation title',
            'status': 'Draft',
            'quotation_number': 'INV1234',
            'currency': 'INR',
            'email': 'quotation@example.com',
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

        self.client.login(email='johnDoeQuotation@example.com',
                          password='password')
        response = self.client.post(
            reverse('quotations:quotation_edit', args=(self.quotation.id,)), data)
        self.assertEqual(response.status_code, 200)

        data.pop('from_company')
        self.client.login(email='johnDoeQuotation@example.com',
                          password='password')
        response = self.client.post(
            reverse('quotations:quotation_edit', args=(self.quotation.id,)), data)
        self.assertEqual(response.status_code, 200)

        data.pop('quotation_number')
        self.client.login(email='johnDoeQuotation@example.com',
                          password='password')
        response = self.client.post(
            reverse('quotations:quotation_edit', args=(self.quotation.id,)), data)
        self.assertEqual(response.status_code, 200)


class QuotationSendMailTestCase(QuotationCreateTest, TestCase):

    def test_quotations_send_mail(self):

        self.client.login(email='joeQuotation@example.com',
                          password='password')
        response = self.client.get(
            reverse('quotations:quotation_send_mail', args=(self.quotation_1.id,)))
        self.assertEqual(response.status_code, 403)

        self.client.login(email='janeDoeQuotation@example.com',
                          password='password')
        response = self.client.get(
            reverse('quotations:quotation_send_mail', args=(self.quotation_1.id,)))
        self.assertEqual(response.status_code, 302)


class QuotationChangeStatusPaidTestCase(QuotationCreateTest, TestCase):

    def test_quotations_change_status_to_paid(self):

        self.client.login(email='joeQuotation@example.com',
                          password='password')
        response = self.client.get(
            reverse('quotations:quotation_change_status_paid', args=(self.quotation_1.id,)))
        self.assertEqual(response.status_code, 403)

        self.client.login(email='janeDoeQuotation@example.com',
                          password='password')
        response = self.client.get(
            reverse('quotations:quotation_change_status_paid', args=(self.quotation_1.id,)))
        self.assertEqual(response.status_code, 302)


class QuotationChangeStatusCancelledTestCase(QuotationCreateTest, TestCase):

    def test_quotations_change_status_to_cancelled(self):

        self.client.login(email='joeQuotation@example.com',
                          password='password')
        response = self.client.get(
            reverse('quotations:quotation_change_status_cancelled', args=(self.quotation_1.id,)))
        self.assertEqual(response.status_code, 403)

        self.client.login(email='janeDoeQuotation@example.com',
                          password='password')
        response = self.client.get(
            reverse('quotations:quotation_change_status_cancelled', args=(self.quotation_1.id,)))
        self.assertEqual(response.status_code, 302)


class QuotationDownloadTestCase(QuotationCreateTest, TestCase):

    def test_quotations_download(self):

        self.client.login(email='joeQuotation@example.com',
                          password='password')
        response = self.client.get(
            reverse('quotations:quotation_download', args=(self.quotation.id,)))
        self.assertEqual(response.status_code, 403)

        # self.client.login(email='johnDoeQuotation@example.com',
        #                   password='password')
        # response = self.client.get(
        #     reverse('quotations:quotation_download', args=(self.quotation_1.id,)))
        # self.assertEqual(response.status_code, 200)


class AddCommentTestCase(QuotationCreateTest, TestCase):

    def test_quotation_add_comment(self):

        self.client.login(email='johnDoeQuotation@example.com', password='password')
        data = {
            'comment': '',
            'quotation_id': self.quotation.id,
        }
        response = self.client.post(
            reverse('quotations:add_comment'), data)
        self.assertEqual(response.status_code, 200)

        data = {
            'comment': 'test comment quotation',
            'quotation_id': self.quotation.id,
        }
        response = self.client.post(
            reverse('quotations:add_comment'), data)
        self.assertEqual(response.status_code, 200)

        self.client.login(email='janeDoeQuotation@example.com', password='password')
        response = self.client.post(
            reverse('quotations:add_comment'), data)
        self.assertEqual(response.status_code, 200)


class UpdateCommentTestCase(QuotationCreateTest, TestCase):

    def test_quotation_update_comment(self):

        self.client.login(email='johnDoeQuotation@example.com', password='password')
        data = {
            'commentid': self.comment.id,
            'quotation_id': self.quotation.id,
            'comment': ''
        }
        response = self.client.post(
            reverse('quotations:edit_comment'), data)
        self.assertEqual(response.status_code, 200)

        data = {
            'comment': 'test comment',
            'commentid': self.comment.id,
            'quotation_id': self.quotation.id,
        }
        response = self.client.post(
            reverse('quotations:edit_comment'), data)
        self.assertEqual(response.status_code, 200)

        self.client.login(email='janeDoeQuotation@example.com', password='password')
        response = self.client.post(
            reverse('quotations:edit_comment'), data)
        self.assertEqual(response.status_code, 200)


class DeleteCommentTestCase(QuotationCreateTest, TestCase):

    def test_quotation_delete_comment(self):

        data = {
            'comment_id': self.comment.id,
        }
        self.client.login(email='janeDoeQuotation@example.com', password='password')
        response = self.client.post(
            reverse('quotations:remove_comment'), data)
        self.assertEqual(response.status_code, 200)

        self.client.login(email='johnDoeQuotation@example.com', password='password')
        response = self.client.post(
            reverse('quotations:remove_comment'), data)
        self.assertEqual(response.status_code, 200)


class AddAttachmentTestCase(QuotationCreateTest, TestCase):

    def test_quotation_add_attachment(self):

        data = {
            'attachment': SimpleUploadedFile('file_name.txt', bytes('file contents.', 'utf-8')),
            'quotation_id': self.quotation.id
        }
        self.client.login(email='johnDoeQuotation@example.com', password='password')
        response = self.client.post(
            reverse('quotations:add_attachment'), data)
        self.assertEqual(response.status_code, 200)

        self.client.login(email='janeDoeQuotation@example.com', password='password')
        response = self.client.post(
            reverse('quotations:add_attachment'), data)
        self.assertEqual(response.status_code, 200)

        data = {
            'attachment': '',
            'quotation_id': self.quotation.id
        }
        self.client.login(email='johnDoeQuotation@example.com', password='password')
        response = self.client.post(
            reverse('quotations:add_attachment'), data)
        self.assertEqual(response.status_code, 200)


class DeleteAttachmentTestCase(QuotationCreateTest, TestCase):

    def test_quotation_delete_attachment(self):

        data = {
            'attachment_id': self.attachment.id,
        }
        self.client.login(email='janeDoeQuotation@example.com', password='password')
        response = self.client.post(
            reverse('quotations:remove_attachment'), data)
        self.assertEqual(response.status_code, 200)

        self.client.login(email='johnDoeQuotation@example.com', password='password')
        response = self.client.post(
            reverse('quotations:remove_attachment'), data)
        self.assertEqual(response.status_code, 200)


class QuotationDeleteTestCase(QuotationCreateTest, TestCase):

    def test_quotations_delete(self):

        self.client.login(email='joeQuotation@example.com',
                          password='password')
        response = self.client.get(
            reverse('quotations:quotation_delete', args=(self.quotation_1.id,)))
        self.assertEqual(response.status_code, 403)

        self.client.login(email='janeDoeQuotation@example.com',
                          password='password')
        response = self.client.get(
            reverse('quotations:quotation_delete', args=(self.quotation_1.id,)))
        self.assertEqual(response.status_code, 302)

        self.client.login(email='johnDoeQuotation@example.com',
                          password='password')
        self.quotation.status = 'Sent'
        self.quotation.is_email_sent = False
        self.quotation.save()
        self.assertEqual(self.quotation.is_sent(), True)
        self.quotation.status = 'Sent'
        self.quotation.is_email_sent = True
        self.quotation.save()
        self.assertEqual(self.quotation.is_resent(), True)
        self.assertEqual(self.quotation.is_draft(), False)
        self.quotation.status = 'Paid'
        self.quotation.save()
        self.assertEqual(self.quotation.is_paid_or_cancelled(), True)
        response = self.client.get(
            reverse('quotations:quotation_delete', args=(self.quotation.id,)) + '?view_company={}'.format(self.company.id,))
        self.assertEqual(response.status_code, 302)
