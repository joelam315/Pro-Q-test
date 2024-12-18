import json
import base64
import os
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.generic import (
    CreateView, UpdateView, DetailView, TemplateView, View)
from common.models import User, Comment, Attachments,Address
from common.forms import BillingAddressForm
from common.utils import COUNTRIES
from contacts.models import Contact
from contacts.serializers import ContactSerializer,CreateContactSerializer,UpdateContactSerializer,RemoveContactSerializer
from contacts.forms import (ContactForm,
                            ContactCommentForm, ContactAttachmentForm)
from companies.models import Company
from django.core.exceptions import PermissionDenied
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.db import IntegrityError
from common.tasks import send_email_user_mentions
from contacts.tasks import send_email_to_assigned_user
from common.access_decorators_mixins import (
    sales_access_required, marketing_access_required, SalesAccessRequiredMixin, MarketingAccessRequiredMixin,AdminAccessRequiredMixin)
from teams.models import Teams

from rest_framework.authentication import SessionAuthentication, BasicAuthentication 
from rest_framework_simplejwt import authentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from phonenumber_field.phonenumber import PhoneNumber, to_python
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from sorl.thumbnail import get_thumbnail
from django.core.files.base import ContentFile


class ContactsListAPIView(APIView):
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [IsAuthenticated]
    model = Contact

    @swagger_auto_schema(
        operation_description="Return related Contact", 

        responses={
        200: ContactSerializer(),
        401: "{\"detail\":\"Authentication credentials were not provided.\"}"})
    def post(self, request):
        ret={}
        ret["result"]=True
        data = json.loads(request.body)
        #return Response(data)
        
        try:
            if request.user.role=="ADMIN" or request.user.is_superuser:
                contact=Contact.objects.all()
            else:
                contact=Contact.objects.filter(assigned_to=request.user)
        except IntegrityError as e:
            ret["result"]=False
            ret["reason"]=str(e).split("DETAIL:  ")[1]
            return Response(ret,status=403)
        results = [ob.as_json() for ob in contact]
        return Response(json.dumps(results))

class ContactsListView(AdminAccessRequiredMixin, LoginRequiredMixin, TemplateView):
    model = Contact
    context_object_name = "contact_obj_list"
    template_name = "contacts.html"

    def get_queryset(self):
        queryset = self.model.objects.all()
        if (self.request.user.role != "ADMIN" and not
                self.request.user.is_superuser):
            queryset = queryset.filter(
                Q(assigned_to__in=[self.request.user]) |
                Q(created_by=self.request.user))

        request_post = self.request.POST
        if request_post:
            if request_post.get('first_name'):
                queryset = queryset.filter(
                    first_name__icontains=request_post.get('first_name'))
            if request_post.get('city'):
                queryset = queryset.filter(
                    address__city__icontains=request_post.get('city'))
            if request_post.get('phone'):
                queryset = queryset.filter(
                    phone__icontains=request_post.get('phone'))
            if request_post.get('email'):
                queryset = queryset.filter(
                    email__icontains=request_post.get('email'))
            if request_post.getlist('assigned_to'):
                queryset = queryset.filter(
                    assigned_to__id__in=request_post.getlist('assigned_to'))
        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super(ContactsListView, self).get_context_data(**kwargs)
        context["contact_obj_list"] = self.get_queryset()
        context["per_page"] = self.request.POST.get('per_page')
        context["users"] = User.objects.filter(
            is_active=True).order_by('email')
        context["assignedto_list"] = [
            int(i) for i in self.request.POST.getlist('assigned_to', []) if i]
        search = False
        if (
            self.request.POST.get('first_name') or
            self.request.POST.get('city') or
            self.request.POST.get('phone') or
            self.request.POST.get(
                'email') or self.request.POST.get('assigned_to')
        ):
            search = True
        context["search"] = search
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


class CreateContactAPIView(APIView):
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [IsAuthenticated]
    model = Contact

    @swagger_auto_schema(
        operation_description="Create a Contact via API call", 
        request_body=CreateContactSerializer,

        responses={
        200: "{\"result\":true}",
        400: "{\"result\":false,\"reason\":\"Missing first_name\"}"+
            "\n{\"result\":false,\"reason\":\"Missing last_name\"}"+
            "\n{\"result\":false,\"reason\":\"Missing phone\"}"+
            "\n{\"result\":false,\"reason\":\"Phone number format invalid\"}",
        401: "{\"detail\":\"Authentication credentials were not provided.\"}",
        403: "{\"result\":false,\"reason\":\"{Key ([feild])=([field_value]) already exists.\"}"})
    def post(self, request):
        ret={}
        ret["result"]=True
        data = json.loads(request.body)
        img = None
        #return Response(data)
        if data.get("first_name")==None:
            ret["result"]=False
            ret["reason"]="Missing first_name"
            return Response(ret,status=400)
        if  data.get("last_name")==None:
            ret["result"]=False
            ret["reason"]="Missing last_name"
            return Response(ret,status=400)
        if  data.get("phone")==None:
            ret["result"]==False
            ret["reason"]="Missing phone"
            return Response(ret,status=400)
        if not PhoneNumber.is_valid(to_python(data.get("phone"))):
            ret["result"]=False
            ret["reason"]="Phone number format invalid"
            return Response(ret,status=400);
        try:
            if data.get("icon")!=None:
                format, imgstr = data.get("icon").split(';base64,') 
                ext = format.split('/')[-1] 

                img = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        except Exception as e:
            ret["result"]=False
            ret["reason"]="Icon wrong format"
            return Response(ret,status=403)
        try:
            contact=Contact.objects.create(
                first_name=data.get("first_name"),
                last_name=data.get("last_name"),
                email=data.get("email"),
                phone=data.get("phone"),
                profile_pic=img,
                description=data.get("description"),
                created_by=request.user)
            contact.assigned_to.add(request.user)
        except IntegrityError as e:
            try:
                contact=Contact.objects.get(email=data.get("email"))
                contact.assigned_to.add(request.user)
                contact.save()
                company, created=Company.objects.get_or_create(name=data.get("company"),created_by=request.user)
                company.assigned_to.add(request.user)
                return Response(ret)
            except Contact.DoesNotExist:
                pass
            ret["result"]=False
            ret["reason"]=str(e).split("DETAIL:  ")[1]
            return Response(ret,status=403)
        if data.get("address")!=None:
            try:
                address=Address.objects.create(
                    address_line=data.get("address").get("address_line"),
                    lat=data.get("address").get("lat"),
                    lng=data.get("address").get("lng"))
                contact.address=address
                contact.save()
            except Exception as e:
                ret["result"]=False
                ret["reason"]="Problem Occured in creating address"
                return Response(ret, status=403)
        if data.get("company")!=None:
            company, created=Company.objects.get_or_create(name=data.get("company"),created_by=request.user)
            company.contacts.add(contact)
            company.assigned_to.add(request.user)
            company.save()
        return Response(ret)

class CreateContactView(AdminAccessRequiredMixin, LoginRequiredMixin, CreateView):
    model = Contact
    form_class = ContactForm
    template_name = "create_contact.html"

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.role == 'ADMIN' or self.request.user.is_superuser:
            self.users = User.objects.filter(is_active=True).order_by('email')
        else:
            self.users = User.objects.filter(role='ADMIN').order_by('email')
        return super(CreateContactView, self).dispatch(
            request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(CreateContactView, self).get_form_kwargs()
        if self.request.user.role == 'ADMIN' or self.request.user.is_superuser:
            self.users = User.objects.filter(is_active=True).order_by('email')
            kwargs.update({"assigned_to": self.users})
        return kwargs

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        address_form = BillingAddressForm(request.POST)
        if form.is_valid() and address_form.is_valid():
            self.assigned_to=contact_obj.assigned_to
            self.teams=contact_obj.teams
            address_obj = address_form.save()
            contact_obj = form.save(commit=False)
            contact_obj.address = address_obj
            contact_obj.created_by = self.request.user
            contact_obj.save()
            if self.request.GET.get('view_company', None):
                if Company.objects.filter(
                        id=int(self.request.GET.get('view_company'))).exists():
                    Company.objects.get(id=int(self.request.GET.get(
                        'view_company'))).contacts.add(contact_obj)
            return self.form_valid(form)

        return self.form_invalid(form)

    def form_valid(self, form):
        contact_obj = form.save(commit=False)
        contact_obj.assigned_to.add(self.request.user)
        if self.request.user.role == 'ADMIN' or self.request.user.is_superuser:
            if self.request.POST.getlist('assigned_to', []):
                contact_obj.assigned_to.add(
                    *self.request.POST.getlist('assigned_to'))
        else:
            contact_obj.assigned_to.set(self.assigned_to.all())
            # for assigned_to_user in assigned_to_list:
            #     user = get_object_or_404(User, pk=assigned_to_user)
            #     mail_subject = 'Assigned to contact.'
            #     message = render_to_string(
            #         'assigned_to/contact_assigned.html', {
            #             'user': user,
            #             'domain': current_site.domain,
            #             'protocol': self.request.scheme,
            #             'contact': contact_obj
            #         })
            #     email = EmailMessage(mail_subject, message, to=[user.email])
            #     email.content_subtype = "html"
            #     email.send()
        if self.request.user.role == 'ADMIN' or self.request.user.is_superuser:
            if self.request.POST.getlist('teams', []):
                user_ids = Teams.objects.filter(id__in=self.request.POST.getlist('teams')).values_list('users', flat=True)
                assinged_to_users_ids = contact_obj.assigned_to.all().values_list('id', flat=True)
                for user_id in user_ids:
                    if user_id not in assinged_to_users_ids:
                        contact_obj.assigned_to.add(user_id)

            if self.request.POST.getlist('teams', []):
                contact_obj.teams.add(*self.request.POST.getlist('teams'))
        else:
            contact_obj.teams.set(self.teams.all())

        contact_obj.save()

        assigned_to_list = list(contact_obj.assigned_to.all().values_list('id', flat=True))
        current_site = get_current_site(self.request)
        recipients = assigned_to_list
        send_email_to_assigned_user.delay(recipients, contact_obj.id, domain=current_site.domain,
            protocol=self.request.scheme)

        if self.request.FILES.get('contact_attachment'):
            attachment = Attachments()
            attachment.created_by = self.request.user
            attachment.file_name = self.request.FILES.get(
                'contact_attachment').name
            attachment.contact = contact_obj
            attachment.attachment = self.request.FILES.get(
                'contact_attachment')
            attachment.save()

        if self.request.is_ajax():
            return JsonResponse({'error': False})
        if self.request.POST.get("savenewform"):
            return redirect("contacts:add_contact")

        return redirect('contacts:list')

    def form_invalid(self, form):
        address_form = BillingAddressForm(self.request.POST)
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'contact_errors': form.errors,
                                 'address_errors': address_form.errors})
        return self.render_to_response(
            self.get_context_data(form=form, address_form=address_form))

    def get_context_data(self, **kwargs):
        context = super(CreateContactView, self).get_context_data(**kwargs)
        context["contact_form"] = context["form"]
        context["users"] = self.users
        context["countries"] = COUNTRIES
        context["assignedto_list"] = [
            int(i) for i in self.request.POST.getlist('assigned_to', []) if i]
        if "address_form" in kwargs:
            context["address_form"] = kwargs["address_form"]
        else:
            if self.request.POST:
                context["address_form"] = BillingAddressForm(self.request.POST)
            else:
                context["address_form"] = BillingAddressForm()
        context["teams"] = Teams.objects.all()
        return context


class ContactDetailView(AdminAccessRequiredMixin, LoginRequiredMixin, DetailView):
    model = Contact
    context_object_name = "contact_record"
    template_name = "view_contact.html"

    def get_queryset(self):
        queryset = super(ContactDetailView, self).get_queryset()
        return queryset.select_related("address")

    def get_context_data(self, **kwargs):
        context = super(ContactDetailView, self).get_context_data(**kwargs)
        user_assgn_list = [
            assigned_to.id for assigned_to in context['object'].assigned_to.all()]
        user_assigned_companies = set(self.request.user.company_assigned_users.values_list('id', flat=True))
        contact_companies = set(context['object'].company_contacts.values_list('id', flat=True))
        if user_assigned_companies.intersection(contact_companies):
            user_assgn_list.append(self.request.user.id)
        if self.request.user == context['object'].created_by:
            user_assgn_list.append(self.request.user.id)
        if (self.request.user.role != "ADMIN" and not
                self.request.user.is_superuser):
            if self.request.user.id not in user_assgn_list:
                raise PermissionDenied
        assigned_data = []
        for each in context['contact_record'].assigned_to.all():
            assigned_dict = {}
            assigned_dict['id'] = each.id
            assigned_dict['name'] = each.email
            assigned_data.append(assigned_dict)

        if self.request.user.is_superuser or self.request.user.role == 'ADMIN':
            users_mention = list(User.objects.filter(is_active=True).values('username'))
        elif self.request.user != context['object'].created_by:
            users_mention = [{'username': context['object'].created_by.username}]
        else:
            users_mention = list(context['object'].assigned_to.all().values('username'))

        context.update({"comments":
                        context["contact_record"].contact_comments.all(),
                        'attachments':
                        context["contact_record"].contact_attachment.all(),
                        "assigned_data": json.dumps(assigned_data),
                        "tasks" : context['object'].contacts_tasks.all(),
                        'users_mention':  users_mention,
                        })
        return context


class UpdateContactAPIView(APIView):
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [IsAuthenticated]
    model = Contact

    @swagger_auto_schema(
        operation_description="Update a Contact via API call", 
        request_body=UpdateContactSerializer,

        responses={
        200: "{\"result\":true}",
        400: "{\"result\":false,\"reason\":\"Phone number format invalid\"}",
        401: "{\"detail\":\"Authentication credentials were not provided.\"}"+
            "\n{\"detail\":\"Not Authorized\"}",
        403: "{\"result\":false,\"reason\":\"{Key ([feild])=([field_value]) already exists.\"}"})
    def post(self, request):
        ret={}
        ret["result"]=True
        data = json.loads(request.body)



        if not PhoneNumber.is_valid(to_python(data.get("phone"))):
            ret["result"]=False
            ret["reason"]="Phone number format invalid"
            return Response(ret,status=400);

        try:
            contact=Contact.objects.get(id=data.get("id"))
        except IntegrityError as e:
            ret["result"]=False
            ret["reason"]=str(e).split("DETAIL:  ")[1]
            return Response(ret,status=403)

        if request.user.role=="ADMIN" or request.user.is_superuser:
            pass
        elif not request.user in contact.assigned_to.all():
            ret["result"]=False
            ret["reason"]="Not Authorized"
            return Response(ret,status=401)
        #return Response(data)
        if data.get("first_name")!=None:
            contact.first_name=data.get("first_name")

        if  data.get("last_name")!=None:
            contact.last_name=data.get("last_name")

        if  data.get("phone")!=None:
            contact.phone=data.get("phone")

        
        if data.get("address")!=None:
            try:
                address=contact.address
                if data.get("address").get("address_line")!=None:
                    address.address_line=data.get("address").get("address_line")
                if data.get("address").get("lat")!=None:
                    address.lat=data.get("address").get("lat")
                if data.get("address").get("lng")!=None:
                    address.lng=data.get("address").get("lng")
                address.save()
            except Exception as e:
                ret["result"]=False
                ret["reason"]="Problem Occured in creating address"
                return Response(ret, status=403)
            
        try:
            contact.save()
        except IntegrityError as e:
            ret["result"]=False
            ret["reason"]=str(e).split("DETAIL:  ")[1]
            return Response(ret,status=403)
        if data.get("company")!=None:
            company, created=Company.objects.get_or_create(name=data.get("company"),created_by=request.user)
            company.contacts.add(contact)
            company.save()
        return Response(ret)

class UpdateContactView(AdminAccessRequiredMixin, LoginRequiredMixin, UpdateView):
    model = Contact
    form_class = ContactForm
    template_name = "create_contact.html"

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.role == 'ADMIN' or self.request.user.is_superuser:
            self.users = User.objects.filter(is_active=True).order_by('email')
        else:
            self.users = User.objects.filter(role='ADMIN').order_by('email')
        return super(UpdateContactView, self).dispatch(
            request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(UpdateContactView, self).get_form_kwargs()
        if self.request.user.role == 'ADMIN' or self.request.user.is_superuser:
            self.users = User.objects.filter(is_active=True).order_by('email')
            kwargs.update({"assigned_to": self.users})
        return kwargs

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        address_obj = self.object.address
        form = self.get_form()
        address_form = BillingAddressForm(request.POST, instance=address_obj)
        if form.is_valid() and address_form.is_valid():
            self.assigned_to=self.object.assigned_to
            self.teams=self.object.teams
            addres_obj = address_form.save()
            contact_obj = form.save(commit=False)
            contact_obj.address = addres_obj
            contact_obj.save()
            return self.form_valid(form)
        return self.form_invalid(form)

    def form_valid(self, form):
        assigned_to_ids = self.get_object().assigned_to.all().values_list(
            'id', flat=True)

        contact_obj = form.save(commit=False)
        previous_assigned_to_users = list(contact_obj.assigned_to.all().values_list('id', flat=True))
        all_members_list = []

        if self.request.user.role == 'ADMIN' or self.request.user.is_superuser: 
            if self.request.POST.getlist('assigned_to', []):
                current_site = get_current_site(self.request)
                assigned_form_users = form.cleaned_data.get(
                    'assigned_to').values_list('id', flat=True)
                all_members_list = list(
                    set(list(assigned_form_users)) - set(list(assigned_to_ids)))
                # if all_members_list:
                #     for assigned_to_user in all_members_list:
                #         user = get_object_or_404(User, pk=assigned_to_user)
                #         mail_subject = 'Assigned to contact.'
                #         message = render_to_string(
                #             'assigned_to/contact_assigned.html', {
                #                 'user': user,
                #                 'domain': current_site.domain,
                #                 'protocol': self.request.scheme,
                #                 'contact': contact_obj
                #             })
                #         email = EmailMessage(
                #             mail_subject, message, to=[user.email])
                #         email.content_subtype = "html"
                #         email.send()

                contact_obj.assigned_to.clear()
                contact_obj.assigned_to.add(
                    *self.request.POST.getlist('assigned_to'))
            else:
                contact_obj.assigned_to.clear()
        else:
            contact_obj.assigned_to.set(self.assigned_to.all())

        if self.request.user.role == 'ADMIN' or self.request.user.is_superuser:
            if self.request.POST.getlist('teams', []):
                user_ids = Teams.objects.filter(id__in=self.request.POST.getlist('teams')).values_list('users', flat=True)
                assinged_to_users_ids = contact_obj.assigned_to.all().values_list('id', flat=True)
                for user_id in user_ids:
                    if user_id not in assinged_to_users_ids:
                        contact_obj.assigned_to.add(user_id)

            if self.request.POST.getlist('teams', []):
                contact_obj.teams.clear()
                contact_obj.teams.add(*self.request.POST.getlist('teams'))
            else:
                contact_obj.teams.clear()
        else:
            contact_obj.teams.set(self.teams.all())

        current_site = get_current_site(self.request)
        assigned_to_list = list(contact_obj.assigned_to.all().values_list('id', flat=True))
        recipients = list(set(assigned_to_list) - set(previous_assigned_to_users))
        send_email_to_assigned_user.delay(recipients, contact_obj.id, domain=current_site.domain,
            protocol=self.request.scheme)

        if self.request.FILES.get('contact_attachment'):
            attachment = Attachments()
            attachment.created_by = self.request.user
            attachment.file_name = self.request.FILES.get(
                'contact_attachment').name
            attachment.contact = contact_obj
            attachment.attachment = self.request.FILES.get(
                'contact_attachment')
            attachment.save()
        if self.request.POST.get('from_company'):
            from_company = self.request.POST.get('from_company')
            return redirect("companies:view_company", pk=from_company)
        if self.request.is_ajax():
            return JsonResponse({'error': False})
        return redirect("contacts:list")

    def form_invalid(self, form):
        address_obj = self.object.address
        address_form = BillingAddressForm(
            self.request.POST, instance=address_obj)
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'contact_errors': form.errors,
                                 'address_errors': address_form.errors})
        return self.render_to_response(
            self.get_context_data(form=form, address_form=address_form))

    def get_context_data(self, **kwargs):
        context = super(UpdateContactView, self).get_context_data(**kwargs)
        context["contact_obj"] = self.object
        user_assgn_list = [
            assigned_to.id for assigned_to in context["contact_obj"].assigned_to.all()]
        if self.request.user == context['contact_obj'].created_by:
            user_assgn_list.append(self.request.user.id)
        if (self.request.user.role != "ADMIN" and not
                self.request.user.is_superuser):
            if self.request.user.id not in user_assgn_list:
                raise PermissionDenied
        contact_profile_name = str(context["contact_obj"].profile_pic).split("/")
        contact_profile_name = contact_profile_name[-1]
        context["contact_profile_name"] = contact_profile_name
        context["address_obj"] = self.object.address
        context["contact_form"] = context["form"]
        context["users"] = self.users
        context["countries"] = COUNTRIES
        context["teams"] = Teams.objects.all()
        context["assignedto_list"] = [
            int(i) for i in self.request.POST.getlist('assigned_to', []) if i]
        if "address_form" in kwargs:
            context["address_form"] = kwargs["address_form"]
        else:
            if self.request.POST:
                context["address_form"] = BillingAddressForm(
                    self.request.POST, instance=context["address_obj"])
            else:
                context["address_form"] = BillingAddressForm(
                    instance=context["address_obj"])
        return context

class RemoveContactAPIView(APIView):
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [IsAuthenticated]
    model = Contact

    @swagger_auto_schema(
        operation_description="Return related Contact", 
        request_body=ContactSerializer,

        responses={
        200: ContactSerializer(),
        400: "{\"result\":false,\"reason\":\"Missing id\"}",
        401: "{\"detail\":\"Authentication credentials were not provided.\"}",
        404: "{\"detail\":\"Not found.\"}"
        })
    def post(self, request):
        ret={}
        ret["result"]=True
        data = json.loads(request.body)
        #return Response(data)
        
        try:
            if request.user.role=="ADMIN" or request.user.is_superuser:
                contact=get_object_or_404(Contact, id=data.get("id"))
            else:
                contact=get_object_or_404(Contact, id=data.get("id"),assigned_to=request.user)
        except IntegrityError as e:
            ret["result"]=False
            ret["reason"]=str(e).split("DETAIL:  ")[1]
            return Response(ret,status=403)

        contact.assigned_to.remove(request.user)
        return Response(ret)

class RemoveContactView(AdminAccessRequiredMixin, LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        contact_id = kwargs.get("pk")
        self.object = get_object_or_404(Contact, id=contact_id)
        if (self.request.user.role != "ADMIN" and not
            self.request.user.is_superuser and
                self.request.user != self.object.created_by):
            contact.assigned_to.remove(self.request.user)
            contact.save()
            return redirect("contacts:list")
        else:
            if self.object.address_id:
                self.object.address.delete()
            self.object.delete()
            if self.request.is_ajax():
                return JsonResponse({'error': False})
            return redirect("contacts:list")


class AddCommentView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = ContactCommentForm
    http_method_names = ["post"]

    def post(self, request, *args, **kwargs):
        self.object = None
        self.contact = get_object_or_404(
            Contact, id=request.POST.get('contactid'))
        if (
            request.user in self.contact.assigned_to.all() or
            request.user == self.contact.created_by or
            request.user.is_superuser or
            request.user.role == 'ADMIN'
        ):
            form = self.get_form()
            if form.is_valid():
                return self.form_valid(form)

            return self.form_invalid(form)

        data = {'error': "You don't have permission to comment."}
        return JsonResponse(data)

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.commented_by = self.request.user
        comment.contact = self.contact
        comment.save()
        comment_id = comment.id
        current_site = get_current_site(self.request)
        send_email_user_mentions.delay(comment_id, 'contacts', domain=current_site.domain,
            protocol=self.request.scheme)
        return JsonResponse({
            "comment_id": comment.id, "comment": comment.comment,
            "commented_on": comment.commented_on,
            "commented_on_arrow": comment.commented_on_arrow,
            "commented_by": comment.commented_by.email
        })

    def form_invalid(self, form):
        return JsonResponse({"error": form['comment'].errors})


class UpdateCommentView(LoginRequiredMixin, View):
    http_method_names = ["post"]

    def post(self, request, *args, **kwargs):
        self.comment_obj = get_object_or_404(
            Comment, id=request.POST.get("commentid"))
        if request.user == self.comment_obj.commented_by:
            form = ContactCommentForm(request.POST, instance=self.comment_obj)
            if form.is_valid():
                return self.form_valid(form)

            return self.form_invalid(form)

        data = {'error': "You don't have permission to edit this comment."}
        return JsonResponse(data)

    def form_valid(self, form):
        self.comment_obj.comment = form.cleaned_data.get("comment")
        self.comment_obj.save(update_fields=["comment"])
        comment_id = self.comment_obj.id
        current_site = get_current_site(self.request)
        send_email_user_mentions.delay(comment_id, 'contacts', domain=current_site.domain,
            protocol=self.request.scheme)
        return JsonResponse({
            "commentid": self.comment_obj.id,
            "comment": self.comment_obj.comment,
        })

    def form_invalid(self, form):
        return JsonResponse({"error": form['comment'].errors})


class DeleteCommentView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        self.object = get_object_or_404(
            Comment, id=request.POST.get("comment_id"))
        if request.user == self.object.commented_by:
            self.object.delete()
            data = {"cid": request.POST.get("comment_id")}
            return JsonResponse(data)

        data = {'error': "You don't have permission to delete this comment."}
        return JsonResponse(data)


class GetContactsView(LoginRequiredMixin, TemplateView):
    model = Contact
    context_object_name = "contacts"
    template_name = "contacts_list.html"

    def get_context_data(self, **kwargs):
        context = super(GetContactsView, self).get_context_data(**kwargs)
        context["contacts"] = self.get_queryset()
        return context


class AddAttachmentsView(LoginRequiredMixin, CreateView):
    model = Attachments
    form_class = ContactAttachmentForm
    http_method_names = ["post"]

    def post(self, request, *args, **kwargs):
        self.object = None
        self.contact = get_object_or_404(
            Contact, id=request.POST.get('contactid'))
        if (
                request.user in self.contact.assigned_to.all() or
                request.user == self.contact.created_by or
                request.user.is_superuser or
                request.user.role == 'ADMIN'
        ):
            form = self.get_form()
            if form.is_valid():
                return self.form_valid(form)

            return self.form_invalid(form)

        data = {'error': "You don't have permission to add attachment."}
        return JsonResponse(data)

    def form_valid(self, form):
        attachment = form.save(commit=False)
        attachment.created_by = self.request.user
        attachment.file_name = attachment.attachment.name
        attachment.contact = self.contact
        attachment.save()
        return JsonResponse({
            "attachment_id": attachment.id,
            "attachment": attachment.file_name,
            "attachment_url": attachment.attachment.url,
            "created_on": attachment.created_on,
            "created_on_arrow": attachment.created_on_arrow,
            "download_url": reverse('common:download_attachment',
                                    kwargs={'pk': attachment.id}),
            "attachment_display": attachment.get_file_type_display(),
            "created_by": attachment.created_by.email,
            "file_type": attachment.file_type()
        })

    def form_invalid(self, form):
        return JsonResponse({"error": form['attachment'].errors})


class DeleteAttachmentsView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        self.object = get_object_or_404(
            Attachments, id=request.POST.get("attachment_id"))
        if (
            request.user == self.object.created_by or
            request.user.is_superuser or
            request.user.role == 'ADMIN'
        ):
            self.object.delete()
            data = {"aid": request.POST.get("attachment_id")}
            return JsonResponse(data)

        data = {'error':
                "You don't have permission to delete this attachment."}
        return JsonResponse(data)

class DeleteContactProfilePicView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        self.object = get_object_or_404(
            Contact, id=request.POST.get("contact_id"))
        if (
            request.user == self.object.created_by or
            request.user.is_superuser or
            request.user.role == 'ADMIN'
        ):
            os.remove(self.object.profile_pic.path)
            self.object.profile_pic=None
            self.object.save()
            data = {"cid": request.POST.get("contact_id")}
            return JsonResponse(data)

        data = {'error':
                "You don't have permission to delete this attachment."}
        return JsonResponse(data)
