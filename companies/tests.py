from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from companies.models import Company, Tags, Email
from cases.models import Case
from common.models import Address, Attachments, Comment, User
from contacts.models import Contact
from leads.models import Lead
from teams.models import Teams


class CompanyCreateTest(object):

    def setUp(self):
        self.user = User.objects.create(
            first_name="johnCompany", username='johnDoeCompany', email='johnCompany@example.com', role='ADMIN')
        self.user.set_password('password')
        self.user.save()

        self.user1 = User.objects.create(
            first_name="jane",
            username='janeCompany',
            email='janeCompany@example.com',
            role="USER",
            has_sales_access=True)
        self.user1.set_password('password')
        self.user1.save()

        self.company = Company.objects.create(
            name="john doe", email="johndoe@example.com", phone="123456789",
            billing_address_line="", billing_street="street name",
            billing_city="city name",
            billing_state="state", billing_postcode="1234",
            billing_country="US",
            website="www.example.como", created_by=self.user, status="open",
            industry="SOFTWARE", description="Testing")
        self.case = Case.objects.create(
            name="Jane doe", case_type="Problem",
            status="New", company=self.company,
            priority="Low", description="case description",
            created_by=self.user, closed_on="2016-05-04")
        self.comment = Comment.objects.create(
            comment='test comment', case=self.case,
            commented_by=self.user
        )
        self.attachment = Attachments.objects.create(
            attachment='image.png', case=self.case,
            created_by=self.user, company=self.company
        )
        self.client.login(email='johnCompany@example.com', password='password')
        self.lead = Lead.objects.create(title="LeadCreation",
            first_name="john lead",last_name="doe",email="johnLead@example.com",
            address_line="",street="street name",city="city name",
            state="state",postcode="5079",country="IN",
            website="www.example.com",status="assigned",source="Call",
            opportunity_amount="700",description="lead description",created_by=self.user)
        self.lead.assigned_to.add(self.user)
        self.address = Address.objects.create(
            street="street number",
            city="city",
            state="state",
            postcode=12346, country="IN")

        self.contact = Contact.objects.create(
            first_name="contact",
            email="contact@example.com",
            phone="12345",
            address=self.address,
            description="contact",
            created_by=self.user)

        self.contact_user1 = Contact.objects.create(
            first_name="contact",
            email="contactUser1@example.com",
            address=self.address,
            description="contact",
            created_by=self.user1)


class CompaniesCreateTestCase(CompanyCreateTest, TestCase):

    def test_company_create_url(self):
        response = self.client.get('/companies/create/', {
            'name': "company", 'email': "johndoe@example.com",
            'phone': "1234567891",
            'billing_address_line': "address line",
            'billing_street': "billing street",
            'billing_city': "billing city",
            'billing_state': "state",
            'billing_postcode': "1234",
            'billing_country': "IN",
            'website': "www.example.com",
            'industry': "SOFTWARE", 'description': "Testing"})
        self.assertEqual(response.status_code, 200)

    def test_company_create_html(self):
        response = self.client.get('/companies/create/', {
            'name': "company", 'email': "companyEmail@example.com", 'phone': "",
            'billing_address_line': "",
            'billing_street': "",
            'billing_city': "city",
            'billing_state': "state",
            'billing_postcode': "1234",
            'billing_country': "IN",
            'website': "www.example.com",
            'industry': "SOFTWARE", 'description': "Testing Done"})
        self.assertTemplateUsed(response, 'create_company.html')


class CompaniesListTestCase(CompanyCreateTest, TestCase):

    def test_companies_list(self):
        self.companies = Company.objects.all()
        response = self.client.get(reverse('companies:list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'companies.html')

    def test_companies_list_queryset(self):
        self.company = Company.objects.all()
        data = {'name': 'name', 'city': 'city',
                'billing_address_line': "billing_address_line",
                'billing_street': "billing_street",
                'billing_city': "billing_city",
                'billing_state': "billing_state",
                'billing_postcode': "billing_postcode",
                'billing_country': "billing_country"}
        response = self.client.post(reverse('companies:list'), data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'companies.html')


class CompaniesCountTestCase(CompanyCreateTest, TestCase):

    def test_companies_list_count(self):
        count = Company.objects.all().count()
        self.assertEqual(count, 1)


class CompaniesViewTestCase(CompanyCreateTest, TestCase):

    def test_companies_view(self):
        self.companies = Company.objects.all()
        response = self.client.get(
            '/companies/' + str(self.company.id) + '/view/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'view_company.html')


class CompaniesRemoveTestCase(CompanyCreateTest, TestCase):

    def test_companies_remove(self):
        response = self.client.get(
            '/companies/' + str(self.company.id) + '/delete/')
        self.assertEqual(response['location'], '/companies/')

    # def test_companies_remove_status(self):
    #     Company.objects.filter(id=self.company.id).delete()
    #     response = self.client.get('/companies/list/')
    #     self.assertEqual(response.status_code, 200)


class CompaniesUpdateUrlTestCase(CompanyCreateTest, TestCase):

    def test_companies_update(self):
        response = self.client.get(
            '/companies/' + str(self.company.id) + '/edit/', {
                'name': "janedoe",
                'email': "janeDoe@example.com", 'phone': "1234567891",
                'billing_address_line': "",
                'billing_street': "street",
                'billing_city': "city",
                'billing_state': "state",
                'billing_postcode': "1234",
                'billing_country': "IN",
                'website': "www.example.com",
                'industry': "SOFTWARE",
                'description': "Test description"})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_company.html')

    def test_companies_update_post(self):
        response = self.client.post(
            '/companies/' + str(self.company.id) + '/edit/',
            {
                'name': "janeDoe", 'email': "janeDoe@example.com",
                'phone': "1234567891",
                'billing_address_line': "",
                'billing_street': "Stree",
                'billing_city': "city",
                'billing_state': "state",
                'billing_postcode': "1234",
                'billing_country': "IN",
                'website': "www.example.com",
                'industry': "SOFTWARE", 'description': "Testing Description"})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_company.html')

    def test_companies_update_status(self):
        response = self.client.get(
            '/companies/' + str(self.company.id) + '/edit/')
        self.assertEqual(response.status_code, 200)

    def test_companies_update_html(self):
        response = self.client.get(
            '/companies/' + str(self.company.id) + '/edit/')
        self.assertTemplateUsed(response, 'create_company.html')


class CompanyCreateEmptyFormTestCase(CompanyCreateTest, TestCase):

    def test_company_creation_invalid_data(self):
        data = {'name': "", 'email': "", 'phone': "",
                'website': "", 'industry': "",
                'description': "",
                'billing_address_line': "",
                'billing_street': "",
                'billing_city': "city",
                'billing_state': "state",
                'billing_postcode': "1234567897",
                'billing_country': "IN"}
        response = self.client.post('/companies/create/', data)
        self.assertEqual(response.status_code, 200)


class CompanyModelTest(CompanyCreateTest, TestCase):

    def test_string_representation(self):
        company = Company(name="Company name", )
        self.assertEqual(str(company), company.name)

    def setUp(self):
        self.user = User.objects.create(
            username='username', email='email@email.com')


class CommentTestCase(CompanyCreateTest, TestCase):

    def test_comment_add(self):
        response = self.client.post(
            '/companies/comment/add/', {'companyid': self.company.id})
        self.assertEqual(response.status_code, 200)

    def test_comment_create(self):
        response = self.client.post(
            '/companies/comment/add/', {'companyid': self.company.id,
                                       'comment': self.comment.id})
        self.assertEqual(response.status_code, 200)

    def test_comment_creation(self):
        self.client.login(email='mp@micropyramid.com', password='mp')
        response = self.client.post(
            '/companies/comment/add/', {'companyid': self.company.id,
                                       'comment': 'comment'})
        self.assertEqual(response.status_code, 200)

    def test_comment_edit(self):
        self.client.login(email='mp@micropyramid.com', password='mp')
        response = self.client.post(
            '/companies/comment/edit/', {'commentid': self.comment.id,
                                        'comment': 'comment'})
        self.assertEqual(response.status_code, 200)

    def test_comment_update(self):
        response = self.client.post(
            '/companies/comment/edit/', {'commentid': self.comment.id,
                                        'comment': 'comment'})
        self.assertEqual(response.status_code, 200)

    # def test_comment_valid(self):
    #     url = "/companies/comment/add/"
    #     data = {"comment": "hai", "commented_by": self.user,
    #             "company": self.company}
    #     response = self.client.post(url, data)
    #     print(url,response)
    #     self.assertEqual(response.status_code, 200)

    def test_comment_delete(self):
        response = self.client.post(
            '/companies/comment/remove/', {'comment_id': self.comment.id})
        self.assertEqual(response.status_code, 200)

    def test_comment_deletion(self):
        self.client.login(email='mp@micropyramid.com', password='mp')
        response = self.client.post(
            '/companies/comment/remove/', {'comment_id': self.comment.id})
        self.assertEqual(response.status_code, 200)


class AttachmentTestCase(CompanyCreateTest, TestCase):

    def test_attachment_add(self):
        self.client.login(email='janeCompany@example.com', password='password')
        response = self.client.post(
            '/companies/attachment/add/', {'companyid': self.company.id})
        self.assertEqual(response.status_code, 200)

    def test_attachment_valid(self):
        upload_file = open('static/images/user.png', 'rb')
        response = self.client.post(
            '/companies/attachment/add/', {'companyid': self.company.id,
                                          'attachment': SimpleUploadedFile(
                                              upload_file.name, upload_file.read())})
        self.assertEqual(response.status_code, 200)

    def test_attachment_delete(self):
        response = self.client.post(
            '/companies/attachment/remove/',
            {'attachment_id': self.attachment.id})
        self.assertEqual(response.status_code, 200)

    def test_attachment_deletion(self):
        self.client.login(email='janeCompany@example.com', password='password')
        response = self.client.post(
            '/companies/attachment/remove/',
            {'attachment_id': self.attachment.id})
        self.assertEqual(response.status_code, 200)


class TagCreateTest(object):

    def setUp(self):
        self.tag = Tags.objects.create(
            name="tag", slug="tag1")


class TagModelTest(TagCreateTest, TestCase):

    def test_string_representation(self):
        tag = Tags(name="tag", slug="tag1")
        self.assertEqual(str(self.tag.name), tag.name)


class TestCreateLeadPostView(CompanyCreateTest, TestCase):

    def test_create_lead_post_status(self):
        upload_file = open('static/images/user.png', 'rb')
        response = self.client.post(reverse(
            'companies:new_company'), {"name": "janeLead",
            "email": "janeLead@example.com",
            "phone": "+911234567891",
            "billing_address_line": "address line",
            "billing_street": "street name",
            "billing_city": "city name",
            "billing_state": "usa",
            "billing_postcode": "1234",
            "billing_country": "IN",
            "website": "www.example.com",
            "created_by": self.user,
            "status": "open",
            "industry": "SOFTWARE",
            "description": "Test description",
            "lead": str(self.lead.id),
            'contacts': str(self.contact.id),
            'tags': 'tag1',
            'company_attachment': SimpleUploadedFile(
            upload_file.name, upload_file.read())
            },
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)

    def test_update_lead_post_status(self):
        upload_file = open('static/images/user.png', 'rb')
        response = self.client.post(reverse(
            'companies:edit_company', kwargs={'pk': self.company.id}),
            {"name": "janedoeLead",
             "email": "janelead@example.com",
             "phone": "91123456789",
             "billing_address_line": "",
             "billing_street": "stree",
             "billing_city": "city",
             "billing_state": "state name",
             "billing_postcode": "123456",
             "billing_country": "IN",
             "website": "www.example.com",
             "created_by": self.user,
             "status": "open",
             "industry": "SOFTWARE",
             "description": "Testing Description",
             "lead": str(self.lead.id),
             'contacts': str(self.contact.id),
             'tags': 'tag1',
             'company_attachment': SimpleUploadedFile(
                 upload_file.name, upload_file.read())
             })
        self.assertEqual(response.status_code, 200)

class test_company_forms(CompanyCreateTest, TestCase):

    def test_company_form(self):
        self.client.login(email='janeCompany@example.com', password='password')
        response = self.client.get(reverse('companies:new_company'))
        self.assertEqual(200, response.status_code)

        response = self.client.get(reverse('companies:create_mail') + '?company_id={}'.format(self.company.id))
        self.assertEqual(200, response.status_code)

        data = {
            'company_id': self.company.id,
            'message_body': 'message body {{email}}',
            'message_subject':'message subject',
            'recipients':[self.contact.id, self.contact_user1.id],
            'scheduled_date_time': timezone.now(),
        }

        response = self.client.post(reverse('companies:create_mail'), data)
        self.assertEqual(200, response.status_code)

        data = {
            'company_id': self.company.id,
            'message_body': 'message body {{email}',
            'message_subject':'message subject',
            'recipients':[self.contact.id, self.contact_user1.id],
            'scheduled_date_time': '',
            'scheduled_later': 'true',
        }

        response = self.client.post(reverse('companies:create_mail'), data)
        self.assertEqual(200, response.status_code)

        data = {
            'company_id': self.company.id,
            'message_body': 'message body {{email}}}',
            'message_subject':'message subject',
            'recipients':[self.contact.id, self.contact_user1.id],
            'scheduled_date_time': timezone.now().strftime('%Y-%m-%d %H:%M'),
        }

        response = self.client.post(reverse('companies:create_mail'), data)
        self.assertEqual(200, response.status_code)

        data = {
            'company_id': self.company.id,
            'message_body': 'message body {{email}}',
            'message_subject':'message subject',
            'recipients':[self.contact.id, self.contact_user1.id],
            'scheduled_date_time': timezone.now().strftime('%Y-%m-%d %H:%M'),
            'scheduled_later':'true',
        }
        response = self.client.post(reverse('companies:create_mail'), data)
        self.assertEqual(200, response.status_code)

        data = {
            'company_id': self.company.id,
            'message_body': 'message body {{email}}',
            'message_subject':'message subject',
            'recipients':[self.contact.id, self.contact_user1.id],
            'from_email': 'jane@doe.com',
            'timezone':'UTC',
        }
        response = self.client.post(reverse('companies:create_mail'), data)
        self.assertEqual(200, response.status_code)

        data = {
            'company_id': 0,
            'message_body': 'message body {{email}}',
            'message_subject':'message subject',
            'recipients':[self.contact.id, self.contact_user1.id],
            'from_email': 'jane@doe.com',
            'timezone':'UTC',
        }
        response = self.client.post(reverse('companies:create_mail'), data)
        self.assertEqual(200, response.status_code)

        data = {
            'company_id': self.company.id,
            'message_body': 'message body {{email}}',
            'message_subject':'message subject',
            'recipients':[self.contact.id, self.contact_user1.id],
            'from_email': 'jane@doe.com',
            'timezone':'UTC',
            'scheduled_later': 'true',
            'scheduled_date_time': timezone.now().strftime('%Y-%m-%d %H:%M'),
        }
        response = self.client.post(reverse('companies:create_mail'), data)
        self.assertEqual(200, response.status_code)


class test_company_models(CompanyCreateTest, TestCase):

    def test_company_model(self):
        self.company.billing_address_line = 'billing address line'
        self.company.save()
        self.assertEqual('billing address line, street name, city name, state, 1234, United States',
            self.company.get_complete_address())
        self.company.billing_street = 'billing street'
        self.company.save()
        self.assertEqual('billing address line, billing street, city name, state, 1234, United States',
            self.company.get_complete_address())
        self.company.billing_city = None
        self.company.billing_address_line = None
        self.company.billing_street = None
        self.company.save()
        self.assertEqual('state, 1234, United States',
            self.company.get_complete_address())
        self.company.billing_state = None
        self.company.save()
        self.assertEqual('1234, United States',
            self.company.get_complete_address())
        self.company.billing_postcode = None
        self.company.save()
        self.assertEqual('United States',self.company.get_complete_address())
        self.company.billing_country = None
        self.company.save()
        self.assertEqual('', self.company.get_complete_address())
        self.company.billing_city = 'city'
        self.company.save()
        self.assertEqual('city', self.company.get_complete_address())
        self.assertEqual('' ,self.company.contact_values)

class test_company_views_list(CompanyCreateTest, TestCase):

    def test_company_views(self):
        self.client.login(email='janeCompany@example.com', password='password')
        response = self.client.get(reverse('companies:list'))
        self.assertEqual(200, response.status_code)
        response = self.client.get(reverse('companies:list')+'?tag=1')
        self.assertEqual(200, response.status_code)
        response = self.client.post(reverse('companies:list'), {'industry': 'industry',
            'tag': [1, ], 'tab_status': 'true'})
        self.assertEqual(200, response.status_code)
        self.tag_name = Tags.objects.create(name='tag name')
        self.team_company = Teams.objects.create(name='dev team')
        self.team_company.users.add(self.user1.id)
        self.client.logout()
        self.client.login(email='johnCompany@example.com', password='password')
        response = self.client.post(reverse('companies:new_company'), {
            'name': "company", 'email': "johndoe@example.com",
            'phone': "+91-123-456-7894",
            'billing_address_line': "address line",
            'billing_street': "billing street",
            'billing_city': "billing city",
            'billing_state': "state",
            'billing_postcode': "1234",
            'billing_country': "IN",
            'website': "www.example.com",
            'industry': "SOFTWARE", 'description': "Testing",
            'contacts':[self.contact_user1.id,],
            'tags': self.tag_name.name,
            'assigned_to' : [self.user.id, ],
            'teams': [self.team_company.id,]},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        response = self.client.post(reverse('companies:new_company'), {
            'name': "company", 'email': "johndoe@example.com",
            'phone': "+91-123-456-7894",
            'billing_address_line': "address line",
            'billing_street': "billing street",
            'billing_city': "billing city",
            'billing_state': "state",
            'billing_postcode': "1234",
            'billing_country': "IN",
            'website': "www.example.com",
            'industry': "SOFTWARE", 'description': "Testing",
            'contacts':[self.contact_user1.id,],
            'tags': self.tag_name.name,
            'assigned_to' : [self.user.id, ],
            'teams': [self.team_company.id,]})
        self.assertEqual(response.status_code, 302)

        response = self.client.post(reverse('companies:new_company'), {
            'name': "company", 'email': "johndoe@example.com",
            'phone': "+91-123-456-7894",
            'billing_address_line': "address line",
            'billing_street': "billing street",
            'billing_city': "billing city",
            'billing_state': "state",
            'billing_postcode': "1234",
            'billing_country': "IN",
            'website': "www.example.com",
            'industry': "SOFTWARE", 'description': "Testing",
            'contacts':[self.contact_user1.id,],
            'tags': self.tag_name.name,
            'assigned_to' : [self.user.id, ],
            'teams': [self.team_company.id,],
            'savenewform': 'true'})
        self.assertEqual(response.status_code, 302)

        response = self.client.post(reverse('companies:new_company'), {
            'name': "company", 'email': "johndoe@example.com",
            'phone': "+91-123-456-789",
            'billing_address_line': "address line",
            'billing_street': "billing street",
            'billing_city': "billing city",
            'billing_state': "state",
            'billing_postcode': "1234",
            'billing_country': "IN",
            'website': "www.example.com",
            'industry': "SOFTWARE", 'description': "Testing",
            'tags': self.tag_name.name,
            'assigned_to' : [0, ],
            'teams': [0,],},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)

        self.client.logout()
        self.client.login(email='janeCompany@example.com', password='password')
        response = self.client.get(reverse('companies:view_company', args=(self.company.id,)))
        self.assertEqual(403, response.status_code)

        self.client.logout()
        self.client.login(email='johnCompany@example.com', password='password')
        response = self.client.post(reverse('companies:new_company'), {
            'name': "company", 'email': "johndoe@example.com",
            'phone': "+91-123-456-789",
            'billing_address_line': "address line",
            'billing_street': "billing street",
            'billing_city': "billing city",
            'billing_state': "state",
            'billing_postcode': "1234",
            'billing_country': "IN",
            'website': "www.example.com",
            'industry': "SOFTWARE", 'description': "Testing",
            'contacts':[self.contact_user1.id,],
            'tags': self.tag_name.name,
            'assigned_to' : [self.user.id, ],
            'teams': [self.team_company.id,]},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(200, response.status_code)

        self.company_edit = Company.objects.create(
            name="company edit", email="johndoe@example.com", phone="123456789",
            billing_address_line="", billing_street="street name",
            billing_city="city name",
            billing_state="state", billing_postcode="1234",
            billing_country="US",
            website="www.example.como", created_by=self.user, status="open",
            industry="SOFTWARE", description="Testing")
        self.company_by_user = Company.objects.create(
            name="company edit", email="johndoe@example.com", phone="123456789",
            billing_address_line="", billing_street="street name",
            billing_city="city name",
            billing_state="state", billing_postcode="1234",
            billing_country="US",
            website="www.example.como", created_by=self.user, status="open",
            industry="SOFTWARE", description="Testing")
        upload_file = open('static/images/user.png', 'rb')
        response = self.client.post(reverse('companies:edit_company', args=(self.company_edit.id,)), {
            'name': "company", 'email': "johndoe@example.com",
            'phone': "+91-123-456-7894",
            'billing_address_line': "address line",
            'billing_street': "billing street",
            'billing_city': "billing city",
            'billing_state': "state",
            'billing_postcode': "1234",
            'billing_country': "IN",
            'website': "www.example.com",
            'industry': "SOFTWARE", 'description': "Testing",
            'contacts':[self.contact_user1.id,],
            'tags': self.tag_name.name + ', another tag edit',
            'assigned_to' : [self.user.id, ],
            'teams': [self.team_company.id,],
            'savenewform': 'true',
            'company_attachment': SimpleUploadedFile(
                 upload_file.name, upload_file.read())})
        self.assertEqual(response.status_code, 302)
        response = self.client.post(reverse('companies:edit_company', args=(self.company_edit.id,)), {
            'name': "company", 'email': "johndoe@example.com",
            'phone': "+91-123-456-7894",
            'billing_address_line': "address line",
            'billing_street': "billing street",
            'billing_city': "billing city",
            'billing_state': "state",
            'billing_postcode': "1234",
            'billing_country': "IN",
            'website': "www.example.com",
            'industry': "SOFTWARE", 'description': "Testing",
            'contacts':[self.contact_user1.id,],
            'tags': self.tag_name.name + ', another tag edit',
            'teams': [self.team_company.id,],
            'savenewform': 'true',},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse('companies:edit_company', args=(self.company_edit.id,)), {
            'name': "company", 'email': "johndoe@example.com",
            'phone': "+91-123-456   ",
            'billing_address_line': "address line",
            'billing_street': "billing street",
            'billing_city': "billing city",
            'billing_state': "state",
            'billing_postcode': "1234",
            'billing_country': "IN",
            'website': "www.example.com",
            'industry': "SOFTWARE", 'description': "Testing",
            'contacts':[self.contact_user1.id,],
            'tags': self.tag_name.name + ', another tag edit',
            'teams': [self.team_company.id,],
            'savenewform': 'true',},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)

        self.client.logout()
        self.client.login(email='janeCompany@example.com', password='password')
        response = self.client.get(reverse('companies:edit_company', args=(self.company_by_user.id,)), {})
        self.assertEqual(403, response.status_code)
        self.company_by_user1 = Company.objects.create(
            name="company edit", email="johndoe@example.com", phone="123456789",
            billing_address_line="", billing_street="street name",
            billing_city="city name",
            billing_state="state", billing_postcode="1234",
            billing_country="US",
            website="www.example.como", created_by=self.user1, status="open",
            industry="SOFTWARE", description="Testing")
        response = self.client.get(reverse('companies:edit_company', args=(self.company_by_user1.id,)), {})
        self.assertEqual(200, response.status_code)
        response = self.client.get(reverse('companies:remove_company', args=(self.company_by_user.id,)), {})
        self.assertEqual(403, response.status_code)

        response = self.client.post(reverse('companies:add_comment'), {'companyid':self.company_by_user.id})
        self.assertEqual(200, response.status_code)

        response = self.client.post(reverse('companies:edit_comment'), {'commentid':self.comment.id})
        self.assertEqual(200, response.status_code)

        self.client.logout()
        self.client.login(email='johnCompany@example.com', password='password')

        response = self.client.post(reverse('companies:edit_comment'), {'commentid':self.comment.id, 'comment':''})
        self.assertEqual(200, response.status_code)

        self.client.logout()
        self.client.login(email='janeCompany@example.com', password='password')
        response = self.client.post(reverse('companies:remove_comment'), {'comment_id':self.comment.id, 'comment':''})
        self.assertEqual(200, response.status_code)

        self.client.logout()
        self.client.login(email='johnCompany@example.com', password='password')

        response = self.client.post(reverse('companies:add_attachment'), {'companyid':self.company.id, 'comment':''})
        self.assertEqual(200, response.status_code)

        email_str = Email.objects.create(message_subject='message subject', message_body='message body')
        self.assertEqual(str(email_str), 'message subject')

        response = self.client.post(reverse('companies:get_contacts_for_company'), {
            'company_id':self.company.id
        })
        self.assertEqual(200, response.status_code)

        self.company.contacts.add(self.contact.id, self.contact_user1.id)

        response = self.client.post(reverse('companies:get_contacts_for_company'), {
            'company_id':self.company.id
        })
        self.assertEqual(200, response.status_code)

        response = self.client.get(reverse('companies:get_contacts_for_company'), {
            'company_id':self.company.id
        })
        self.assertEqual(200, response.status_code)

        response = self.client.post(reverse('companies:get_email_data_for_company'), {
            'email_company_id':email_str.id
        })
        self.assertEqual(200, response.status_code)

        response = self.client.get(reverse('companies:get_email_data_for_company'), {
            'email_company_id':email_str.id
        })
        self.assertEqual(200, response.status_code)


class TestCompanyUserMentions(CompanyCreateTest, TestCase):

    def test_company_views(self):
        self.user_created_by = User.objects.create(
            first_name="jane",
            username='janeCompanyCreatedBy',
            email='janeCompanyCreatedBy@example.com',
            role="USER",
            has_sales_access=True)
        self.user_created_by.set_password('password')
        self.user_created_by.save()

        self.user_assigned_to = User.objects.create(
            first_name="jane",
            username='janeCompanyUserAssigned',
            email='janeCompanyUserAssigned@example.com',
            role="USER",
            has_sales_access=True)
        self.user_assigned_to.set_password('password')
        self.user_assigned_to.save()

        self.company = Company.objects.create(
            name="john doe acc created by", email="johndoe@example.com", phone="123456789",
            billing_address_line="", billing_street="street name",
            billing_city="city name",
            billing_state="state", billing_postcode="1234",
            billing_country="US",
            website="www.example.como", created_by=self.user_created_by, status="open",
            industry="SOFTWARE", description="Testing")

        self.company.assigned_to.add(self.user_assigned_to.id)
        self.client.logout()
        self.client.login(email='janeCompanyCreatedBy@example.com', password='password')
        response = self.client.get(reverse('companies:view_company', args=(self.company.id,)))
        self.assertEqual(200, response.status_code)

        self.client.logout()
        self.client.login(email='janeCompanyUserAssigned@example.com', password='password')
        response = self.client.get(reverse('companies:view_company', args=(self.company.id,)))
        self.assertEqual(200, response.status_code)
