from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase
from django.urls import reverse
from django.utils.encoding import force_text

from companies.models import Company
from cases.models import Case
from common.models import Address, Attachments, Comment, User
from customers.forms import CustomerAttachmentForm
from customers.models import Customer
from teams.models import Teams


class CustomerObjectsCreation(object):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(
            first_name="johnCustomer",
            username='johnDoeCustomer',
            email="johnCustomer@example.com",
            role="ADMIN")
        self.user.set_password('password')
        self.user.save()
        self.address = Address.objects.create(
            street="street",
            city="city name",
            state="state name",
            postcode=12345, country="IN")

        self.customer = Customer.objects.create(
            first_name="customer",
            email="customer@example.com",
            phone="12345",
            address=self.address,
            description="customer",
            created_by=self.user)
        self.customer.assigned_to.add(self.user)
        self.case = Case.objects.create(
            name="jane doe case",
            case_type="Problem",
            status="New",
            priority="Low",
            description="description for case",
            created_by=self.user,
            closed_on="2016-05-04")
        self.comment = Comment.objects.create(
            comment='test comment', case=self.case,
            commented_by=self.user
        )
        self.attachment = Attachments.objects.create(
            attachment='image.png', case=self.case,
            created_by=self.user
        )

        self.user_customers_mp = User.objects.create(
            first_name="janeUser@example.com",
            username='janeUserCustomer',
            email="janeUser@example.com",
            role="USER",
            has_sales_access=True)
        self.user_customers_mp.set_password('password')
        self.user_customers_mp.save()

        self.client.login(username='johnCustomer@example.com', password='password')


class CustomerObjectsCreation_Count(CustomerObjectsCreation, TestCase):

    def test_customer_object_creation(self):
        c = Customer.objects.count()
        con = Customer.objects.filter(id=self.customer.id)
        # print(self.customer.first_name)
        self.assertEqual(str(con.last()), self.customer.first_name)
        self.assertEqual(c, 1)

    def test_address_object_creation(self):
        c = Address.objects.count()
        self.assertEqual(c, 1)


class CustomerViewsTestCase(CustomerObjectsCreation, TestCase):

    def test_customers_list_page(self):
        response = self.client.get(reverse('customers:list'))
        self.assertEqual(response.status_code, 200)
        if response.status_code == 200:
            self.assertEqual(
                response.context['customer_obj_list'][0].id, self.customer.id)
            self.assertTrue(response.context['customer_obj_list'])

    def test_customers_list_html(self):
        response = self.client.get(reverse('customers:list'))
        self.assertTemplateUsed(response, 'customers.html')

    def test_customers_create(self):
        upload_file = open('static/images/user.png', 'rb')
        response = self.client.post('/customers/create/', {
            'first_name': 'john customer',
            'last_name': 'doe',
            'email': 'johnDoeCustomer@example.com',
            'phone': '+911234567892',
            'address': self.address.id,
            'description': 'customer',
            'created_by': self.user,
            'assigned_to': str(self.user.id),
            'customer_attachment': SimpleUploadedFile(
                upload_file.name, upload_file.read())
        })
        self.assertEqual(response.status_code, 302)

    def test_customer_create(self):
        upload_file = open('static/images/user.png', 'rb')
        response = self.client.post('/customers/create/', {
            'first_name': 'janeDoe',
            'last_name': 'customer doe',
            'email': 'janeDoeCustomer@example.com',
            'phone': '+911234567892',
            'address': self.address.id,
            'description': 'customer',
            'created_by': self.user,
            'assigned_to': str(self.user.id),
            'customer_attachment': SimpleUploadedFile(
                upload_file.name, upload_file.read())
        })
        self.assertEqual(response.status_code, 302)

    def test_update_customer(self):
        upload_file = open('static/images/user.png', 'rb')
        url = '/customers/' + str(self.customer.id) + '/edit/'
        data = {
            'first_name': 'john Customer',
            'last_name': 'doe',
            'email': 'johnDoeCustomer@example.com',
            'phone': '+911234561255',
            'address': self.address.id,
            'description': 'customer',
            'created_by': self.user,
            'assigned_to': str(self.user.id),
            'customer_attachment': SimpleUploadedFile(
                upload_file.name, upload_file.read())
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)

    def test_customers_create_html(self):
        response = self.client.post('/customers/create/', {
            'name': 'customer', 'email': 'customer@example.com', 'phone': '12345',
            'address': self.address,
            'description': 'customer'})
        self.assertTemplateUsed(response, 'create_customer.html')

    def test_customers_delete(self):
        Customer.objects.filter(id=self.customer.id).delete()
        response = self.client.get(reverse("customers:list"))
        self.assertEqual(response.status_code, 200)

    def test_customers_delete_get(self):
        response = self.client.get(
            '/customers/' + str(self.customer.id) + '/delete/')
        self.assertEqual(response.status_code, 302)

    def test_customers_delete_location_checking(self):
        response = self.client.post(
            '/customers/' + str(self.customer.id) + '/delete/')
        self.assertEqual(response['location'], '/customers/')

    def test_customers_edit(self):
        response = self.client.post(
            '/customers/' + str(self.customer.id) + '/edit/', {
                'name': 'customer name',
                'email': 'customer@example.com',
                'phone': '12345',
                'pk': self.customer.id,
                'address': self.address.id})
        self.assertEqual(response.status_code, 200)

    def test_customers_edit_html(self):
        response = self.client.post(
            '/customers/' + str(self.customer.id) + '/edit/', {
                'name': 'customer Name',
                'email': 'customer@example.com',
                'phone': '12345',
                'pk': self.customer.id,
                'address': self.address.id})
        self.assertTemplateUsed(response, 'create_customer.html')

    def test_customers_view(self):
        response = self.client.get(
            '/customers/' + str(self.customer.id) + '/view/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context['customer_record'].id, self.customer.id)

    def test_customers_view_html(self):
        response = self.client.get(
            '/customers/' + str(self.customer.id) + '/view/')
        self.assertTemplateUsed(response, 'view_customer.html')

    def test_customers_edit_post(self):
        response = self.client.get(
            '/customers/' + str(self.customer.id) + '/edit/')
        self.assertEqual(response.status_code, 200)


class CustomersListTestCase(CustomerObjectsCreation, TestCase):

    def test_customers_list(self):
        self.customers = Customer.objects.all()
        response = self.client.get(reverse('customers:list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'customers.html')

    def test_customers_list_queryset(self):
        data = {'fist_name': 'jane customer',
                'city': "city name", 'phone': '12345',
                'email': "customer@example.com", 'assigned_to': str(self.user.id)}
        response = self.client.post(reverse('customers:list'), data)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'customers.html')

    def test_customers_list_user_role(self):
        self.client.login(username='janeUser@example.com', password='password')
        self.customer = Customer.objects.create(
            first_name="jane customer",
            email="janecustomer@example.com",
            created_by=self.user_customers_mp)
        response = self.client.get(reverse('customers:list'))
        self.assertEqual(response.status_code, 200)
        self.customer.delete()

        response = self.client.post(
            reverse('customers:list'), {'first_name': 'john customer', 'assigned_to': str(self.user.id)})
        self.assertEqual(response.status_code, 200)


class CommentTestCase(CustomerObjectsCreation, TestCase):

    def test_comment_add(self):
        response = self.client.post(
            '/customers/comment/add/', {'customerid': self.customer.id})
        self.assertEqual(response.status_code, 200)

    # def test_GetCustomersView(self):
    #     response = self.client.get('/get/list/')
    #     # self.assertEqual(response.status_code, 200)
        # self.assertIsNone(response.context['customers'])

    def test_comment_edit(self):
        response = self.client.post(
            '/customers/comment/edit/', {'commentid': self.comment.id})
        self.assertEqual(response.status_code, 200)
        resp = self.client.post(
            '/customers/comment/edit/',
            {'commentid': self.comment.id, 'comment': 'test comment'})
        self.assertEqual(resp.status_code, 200)

    def test_comment_delete(self):
        response = self.client.post(
            '/customers/comment/remove/', {'comment_id': self.comment.id})
        self.assertEqual(response.status_code, 200)

    def test_form_valid(self):
        response = self.client.post(
            '/customers/comment/add/', {'customerid': self.customer.id,
                                       'comment': 'test comment'})
        # print(response , "response")
        self.assertEqual(response.status_code, 200)


class AttachmentTestCase(CustomerObjectsCreation, TestCase):

    def test_attachment_add(self):
        response = self.client.post(
            '/customers/attachment/add/', {'customerid': self.customer.id})
        self.assertEqual(response.status_code, 200)

    def test_attachment_valid(self):
        upload_file = open('static/images/user.png', 'rb')
        response = self.client.post(
            '/customers/attachment/add/', {'customerid': self.customer.id,
                                          'attachment': SimpleUploadedFile(
                                              upload_file.name, upload_file.read())})
        self.assertEqual(response.status_code, 200)

    def test_attachment_delete(self):
        response = self.client.post(
            '/customers/attachment/remove/',
            {'attachment_id': self.attachment.id})
        self.assertEqual(response.status_code, 200)


class TestCustomerCreateCustomer(CustomerObjectsCreation, TestCase):

    def test_create_new_customer(self):
        upload_file = open('static/images/user.png', 'rb')
        response = self.client.post('/customers/create/', {
            'first_name': 'john doe customer',
            'last_name': 'doe',
            'email': 'johnDCustomer@example.com',
            'phone': '+911234561256',
            'address': self.address.id,
            'description': 'customer',
            'created_by': self.user,
            'assigned_to': str(self.user.id),
            'savenewform': True,
            'address_line': 'address line'
        })
        self.assertEqual(response.status_code, 302)

    def test_customer_detail_view_error(self):
        self.client.login(username='janeUser@example.com', password='password')
        self.customer = Customer.objects.create(created_by=self.user)

    def test_customer_update_view(self):
        self.client.login(username='johnCustomer@example.com', password='password')
        response = self.client.post(reverse('customers:edit_customer', args=(self.customer.id,)), {
            'first_name': 'first name',
            'last_name': 'last name',
            'phone': '232323',
            'email': 'email@email.com',
            'assigned_to': str(self.user.id)
        })
        self.assertEqual(200, response.status_code)

    def test_customer_update_view_assigned_Users(self):
        self.client.login(username='johnCustomer@example.com', password='password')
        response = self.client.post(reverse('customers:edit_customer', args=(self.customer.id,)), {
            'first_name': 'first name',
            'last_name': 'last name',
            'phone': '232323',
            'email': 'email@email.com',
            'assigned_to': str(self.user_customers_mp.id)
        })
        self.assertEqual(200, response.status_code)

        response = self.client.post(reverse('customers:edit_customer', args=(self.customer.id,)), {
            'first_name': 'first name',
            'last_name': 'last name',
            'phone': '232323',
            'email': 'email@email.com'
        })
        self.assertEqual(200, response.status_code)

    def test_customer_update_view_error(self):
        self.usermp1 = User.objects.create(
            first_name="janeDoe@example.com",
            username='janeDoe',
            email="janeDoe@example.com",
            role="USER",
            is_active=True,
            has_sales_access=True)
        self.usermp1.set_password('password')
        self.usermp1.save()
        self.customer = Customer.objects.create(
            first_name="jane doe customer",
            email="customerJaneDoe@example.com",
            created_by=self.user_customers_mp)
        self.client.login(username='janeDoe@example.com', password='password')
        response = self.client.get(
            reverse('customers:edit_customer', args=(self.customer.id,)), {})
        self.assertEqual(403, response.status_code)

        response = self.client.post(reverse('customers:remove_customer', args=(
            self.customer.id,)), {'pk': self.customer.id})
        self.assertEqual(403, response.status_code)
        self.customer.delete()

        self.customer = Customer.objects.create(created_by=self.user)
        response = self.client.post(
            '/customers/comment/add/', {'customerid': self.customer.id})
        self.assertJSONEqual(force_text(response.content), {
                             'error': "You don't have permission to comment."})

        response = self.client.post(
            '/customers/comment/edit/', {'commentid': self.comment.id})
        self.assertJSONEqual(force_text(response.content), {
                             'error': "You don't have permission to edit this comment."})

        response = self.client.post(
            '/customers/comment/remove/', {'comment_id': self.comment.id})
        self.assertJSONEqual(force_text(response.content), {
                             'error': "You don't have permission to delete this comment."})

        response = self.client.post(
            '/customers/attachment/add/', {'customerid': self.customer.id})
        self.assertJSONEqual(force_text(response.content), {
                             'error': "You don't have permission to add attachment."})

        self.attachment = Attachments.objects.create(
            attachment='image.png', case=self.case,
            created_by=self.user
        )
        response = self.client.post(
            '/customers/attachment/remove/', {'attachment_id': self.attachment.id})
        self.assertJSONEqual(force_text(response.content), {
                             'error': "You don't have permission to delete this attachment."})


class TestCustomerViews(CustomerObjectsCreation, TestCase):

    def test_create_customer(self):
        self.client.logout()
        self.client.login(username='janeUser@example.com', password='password')
        response = self.client.get(reverse('customers:list'),{})
        self.assertEqual(200, response.status_code)

        self.client.logout()
        self.client.login(username='johnCustomer@example.com', password='password')
        self.company_by_user = Company.objects.create(
            name="company edit", email="johndoe@example.com", phone="123456789",
            billing_address_line="", billing_street="street name",
            billing_city="city name",
            billing_state="state", billing_postcode="1234",
            billing_country="US",
            website="www.example.como", created_by=self.user, status="open",
            industry="SOFTWARE", description="Testing")
        self.teams_customers = Teams.objects.create(name='teams customers')
        self.teams_customers.users.add(self.user)
        data = {
            'first_name':'first name',
            'last_name':'last name',
            'phone':'+91-123-456-7854',
            'email':'example@user.com',
            'teams':[self.teams_customers.id,]
        }
        response = self.client.post(reverse('customers:add_customer') + '?view_company={}&address_form='.format(self.company_by_user.id), data)
        self.assertEqual(302, response.status_code)

        data = {
            'first_name':'first name',
            'last_name':'last name',
            'phone':'+91-123-456-7858',
            'email':'example@mail.com',
            'teams':[self.teams_customers.id,]
        }
        response = self.client.post(reverse('customers:add_customer') + '?view_company={}'.format(self.company_by_user.id), data,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(200, response.status_code)

        data = {
            'first_name':'first name',
            'last_name':'last name',
            'phone':'+91-123-456-7854',
            'email':'example@user',
            'teams':[self.teams_customers.id,]
        }
        response = self.client.post(reverse('customers:add_customer') + '?view_company={}'.format(self.company_by_user.id), data,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(200, response.status_code)
        response = self.client.get(reverse('customers:add_customer') + '?address_form=')
        self.assertEqual(200, response.status_code)

        response = self.client.post(reverse('customers:edit_customer', args=(self.customer.id,)),{
            'first_name':'customer',
            'last_name':'customer@example.com',
            'phone':'+91-123-456-7856',
            'email':'customer@example.com',
            'teams':[self.teams_customers.id,]
        })
        self.assertEqual(302, response.status_code)

        self.user_customers_mp = User.objects.create(
            first_name="joeUser@customer.com",
            username='joeUser@customer.com',
            email="joeUser@customer.com",
            role="USER",
            has_sales_access=True)
        self.user_customers_mp.set_password('password')
        self.user_customers_mp.save()

        self.client.logout()
        self.client.login(username='joeUser@customer.com', password='password')
        response = self.client.get(reverse('customers:view_customer', args=(self.customer.id,)))
        self.assertEqual(403, response.status_code)

        self.client.logout()
        self.client.login(username='janeUser@example.com', password='password')
        response = self.client.get(reverse('customers:view_customer', args=(self.customer.id,)))
        # self.assertEqual(403, response.status_code)

        self.client.logout()
        self.client.login(username='johnCustomer@example.com', password='password')
        self.teams_customers.users.add(self.user)
        data = {
            'first_name':'customer',
            'last_name':'customer',
            'phone':'+91-123-456-7852',
            'email':'customer@example.com',
            'teams':[self.teams_customers.id,]
        }
        response = self.client.post(reverse('customers:edit_customer', args=(self.customer.id,)) + '?from_company={}'.format(self.company_by_user.id), data)
        self.assertEqual(302, response.status_code)
        response = self.client.post(reverse('customers:edit_customer', args=(self.customer.id,)) + '?from_company={}&address_form='.format(self.company_by_user.id), data,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertEqual(200, response.status_code)

        data = {
            'first_name':'customer',
            'last_name':'customer',
            'phone':'+91-123-456',
            'email':'customer@example',
            'teams':[self.teams_customers.id,]
        }
        response = self.client.post(reverse('customers:edit_customer', args=(self.customer.id,)) + '?from_company={}'.format(self.company_by_user.id), data,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(200, response.status_code)

        response = self.client.post(reverse('customers:edit_customer', args=(self.customer.id,)) + '?from_company={}'.format(self.company_by_user.id), data,)
        self.assertEqual(200, response.status_code)

        self.client.logout()
        self.client.login(username='johnCustomer@example.com', password='password')
        self.customer_delete = Customer.objects.create(
            first_name="customer",
            email="customer_delete@example.com",
            phone="12345",
            address=self.address,
            description="customer",
            created_by=self.user)
        response = self.client.post(reverse('customers:remove_customer', args=(self.customer_delete.id,)), {'pk': self.customer_delete.id},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(200, response.status_code)

        self.customer_edit = Customer.objects.create(
            first_name="customer",
            email="customer_edit@example.com",
            phone="12345",
            description="customer",
            created_by=self.user_customers_mp)

        self.client.logout()
        self.client.login(username='joeUser@customer.com', password='password')
        response = self.client.get(reverse('customers:view_customer', args=(self.customer_edit.id,)), {'pk': self.customer_edit.id},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(200, response.status_code)
        response = self.client.get(reverse('customers:add_customer'))
        self.assertEqual(200, response.status_code)