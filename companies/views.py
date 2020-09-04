import pytz
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, FormView,
                                  TemplateView, UpdateView, View)

from companies.forms import (CompanyAttachmentForm, CompanyCommentForm,
                            CompanyForm, EmailForm)
from companies.models import Company, Email, Tags
from companies.tasks import send_email, send_email_to_assigned_user
from cases.models import Case
from common.access_decorators_mixins import (MarketingAccessRequiredMixin,
                                             SalesAccessRequiredMixin,
                                             marketing_access_required,
                                             sales_access_required,
                                             AdminAccessRequiredMixin)
from common.models import Attachments, Comment, User
from common.tasks import send_email_user_mentions
from common.utils import (CASE_TYPE, COUNTRIES, CURRENCY_CODES, INDCHOICES,
                          PRIORITY_CHOICE, STATUS_CHOICE)
from contacts.models import Contact
from leads.models import Lead
from opportunity.models import SOURCES, STAGES, Opportunity
from teams.models import Teams


class CompaniesListView(AdminAccessRequiredMixin, LoginRequiredMixin, TemplateView):
    model = Company
    context_object_name = "companies_list"
    template_name = "companies.html"

    def get_queryset(self):
        queryset = self.model.objects.all()
        if self.request.user.role != "ADMIN" and not self.request.user.is_superuser:
            queryset = queryset.filter(
                Q(created_by=self.request.user) | Q(assigned_to=self.request.user)).distinct()

        if self.request.GET.get('tag', None):
            queryset = queryset.filter(tags__in = self.request.GET.getlist('tag'))

        request_post = self.request.POST
        if request_post:
            if request_post.get('name'):
                queryset = queryset.filter(
                    name__icontains=request_post.get('name'))
            if request_post.get('city'):
                queryset = queryset.filter(
                    billing_city__contains=request_post.get('city'))
            if request_post.get('industry'):
                queryset = queryset.filter(
                    industry__icontains=request_post.get('industry'))
            if request_post.get('tag'):
                queryset = queryset.filter(tags__in=request_post.getlist('tag'))

        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super(CompaniesListView, self).get_context_data(**kwargs)
        open_companies = self.get_queryset().filter(status='open')
        close_companies = self.get_queryset().filter(status='close')
        context["companies_list"] = self.get_queryset()
        context["users"] = User.objects.filter(
            is_active=True).order_by('email')
        context['open_companies'] = open_companies
        context['close_companies'] = close_companies
        context["industries"] = INDCHOICES
        context["per_page"] = self.request.POST.get('per_page')
        tag_ids = list(set(Company.objects.values_list('tags', flat=True)))
        context["tags"] = Tags.objects.filter(id__in=tag_ids)
        if self.request.POST.get('tag', None):
            context["request_tags"] = self.request.POST.getlist('tag')
        elif self.request.GET.get('tag', None):
            context["request_tags"] = self.request.GET.getlist('tag')
        else:
            context["request_tags"] = None

        search = False
        if (
            self.request.POST.get('name') or self.request.POST.get('city') or
            self.request.POST.get('industry') or self.request.POST.get('tag')
        ):
            search = True

        context["search"] = search

        tab_status = 'Open'
        if self.request.POST.get('tab_status'):
            tab_status = self.request.POST.get('tab_status')
        context['tab_status'] = tab_status
        TIMEZONE_CHOICES = [(tz, tz) for tz in pytz.common_timezones]
        context["timezones"] = TIMEZONE_CHOICES
        context["settings_timezone"] = settings.TIME_ZONE

        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


class CreateCompanyView(AdminAccessRequiredMixin, LoginRequiredMixin, CreateView):
    model = Company
    form_class = CompanyForm
    template_name = "create_company.html"

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.role == 'ADMIN' or self.request.user.is_superuser:
            self.users = User.objects.filter(is_active=True).order_by('email')
        elif request.user.google.all():
            self.users = []
        else:
            self.users = User.objects.filter(role='ADMIN').order_by('email')
        return super(
            CreateCompanyView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(CreateCompanyView, self).get_form_kwargs()
        kwargs.update({"company": True})
        kwargs.update({"request_user": self.request.user})
        # if self.request.user.role != "ADMIN" and not self.request.user.is_superuser:
        #     kwargs.update({"request_user": self.request.user})
        return kwargs

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)

        return self.form_invalid(form)

    def form_valid(self, form):
        # Save Company
        company_object = form.save(commit=False)
        company_object.created_by = self.request.user
        company_object.save()

        if self.request.POST.get('tags', ''):
            tags = self.request.POST.get("tags")
            splitted_tags = tags.split(",")
            for t in splitted_tags:
                tag = Tags.objects.filter(name=t.lower())
                if tag:
                    tag = tag[0]
                else:
                    tag = Tags.objects.create(name=t.lower())
                company_object.tags.add(tag)
        '''if self.request.POST.getlist('contacts', []):
            company_object.contacts.add(*self.request.POST.getlist('contacts'))
        if self.request.POST.getlist('assigned_to', []):
            company_object.assigned_to.add(*self.request.POST.getlist('assigned_to'))'''
        if self.request.FILES.get('company_attachment'):
            attachment = Attachments()
            attachment.created_by = self.request.user
            attachment.file_name = self.request.FILES.get(
                'company_attachment').name
            attachment.company = company_object
            attachment.attachment = self.request.FILES.get(
                'company_attachment')
            attachment.save()
        if self.request.POST.getlist('teams', []):
            user_ids = Teams.objects.filter(id__in=self.request.POST.getlist('teams')).values_list('users', flat=True)
            assinged_to_users_ids = company_object.assigned_to.all().values_list('id', flat=True)
            for user_id in user_ids:
                if user_id not in assinged_to_users_ids:
                    company_object.assigned_to.add(user_id)
        if self.request.POST.getlist('teams', []):
            company_object.teams.add(*self.request.POST.getlist('teams'))

        #assigned_to_list = list(company_object.assigned_to.all().values_list('id', flat=True))
        current_site = get_current_site(self.request)
        #recipients = assigned_to_list
        #send_email_to_assigned_user.delay(recipients, company_object.id, domain=current_site.domain,
        #    protocol=self.request.scheme)

        if self.request.POST.get("savenewform"):
            return redirect("companies:new_company")

        if self.request.is_ajax():
            data = {'success_url': reverse_lazy(
                'companies:list'), 'error': False}
            return JsonResponse(data)

        return redirect("companies:list")

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        return self.render_to_response(
            self.get_context_data(form=form)
        )

    def get_context_data(self, **kwargs):
        context = super(CreateCompanyView, self).get_context_data(**kwargs)
        context["company_form"] = context["form"]
        context["users"] = self.users
        context["industries"] = INDCHOICES
        context["countries"] = COUNTRIES
        # context["contact_count"] = Contact.objects.count()
        if self.request.user.role == 'ADMIN' or self.request.user.is_superuser:
            context["leads"] = Lead.objects.exclude(
                status__in=['converted', 'closed'])
            #context["contacts"] = Contact.objects.all()
        else:
           ''' context["leads"] = Lead.objects.filter(
                Q(assigned_to__in=[self.request.user]) | Q(created_by=self.request.user)).exclude(
                status__in=['converted', 'closed'])'''
        context["lead_count"] = context["leads"].count()
        '''if self.request.user.role != "ADMIN" and not self.request.user.is_superuser:
            context["lead_count"] = Lead.objects.filter(
                Q(assigned_to__in=[self.request.user]) | Q(created_by=self.request.user)).exclude(status='closed').count()
            context["contacts"] = Contact.objects.filter(
                Q(assigned_to__in=[self.request.user]) | Q(created_by=self.request.user))
        context["contact_count"] = context["contacts"].count()
        context["teams"] = Teams.objects.all()'''
        return context


class CompanyDetailView(AdminAccessRequiredMixin, LoginRequiredMixin, DetailView):
    model = Company
    context_object_name = "company_record"
    template_name = "view_company.html"

    def get_context_data(self, **kwargs):
        context = super(CompanyDetailView, self).get_context_data(**kwargs)
        company_record = context["company_record"]
        if self.request.user.role != "ADMIN" and not self.request.user.is_superuser:
            if not ((self.request.user == company_record.created_by) or
                (self.request.user in company_record.assigned_to.all())):
                raise PermissionDenied

        comment_permission = True if (
            self.request.user == company_record.created_by or
            self.request.user.is_superuser or self.request.user.role == 'ADMIN'
        ) else False

        if self.request.user.is_superuser or self.request.user.role == 'ADMIN':
            users_mention = list(User.objects.filter(is_active=True).values('username'))
        elif self.request.user != company_record.created_by:
            if company_record.created_by:
                users_mention = [{'username': company_record.created_by.username}]
            else:
                users_mention = []
        else:
            users_mention = []

        context.update({
            "comments": company_record.companies_comments.all(),
            "attachments": company_record.company_attachment.all(),
            #"opportunity_list": Opportunity.objects.filter(
            #    company=company_record),
            #"contacts": company_record.contacts.all(),
            "users": User.objects.filter(is_active=True).order_by('email'),
            #"cases": Case.objects.filter(company=company_record),
            "stages": STAGES,
            "sources": SOURCES,
            "countries": COUNTRIES,
            "currencies": CURRENCY_CODES,
            "case_types": CASE_TYPE,
            "case_priority": PRIORITY_CHOICE,
            "case_status": STATUS_CHOICE,
            'comment_permission': comment_permission,
            #'tasks':company_record.companies_tasks.all(),
            #'quotations':company_record.companies_quotations.all(),
            #'emails':company_record.sent_email.all(),
            'users_mention': users_mention,
        })
        return context


class CompanyUpdateView(AdminAccessRequiredMixin, LoginRequiredMixin, UpdateView):
    model = Company
    form_class = CompanyForm
    template_name = "create_company.html"

    def dispatch(self, request, *args, **kwargs):
        self.users = User.objects.filter(is_active=True).order_by('email')
        # if self.request.user.role == 'ADMIN' or self.request.user.is_superuser:
        # elif request.user.google.all():
        #     self.users = []
        # else:
        #     self.users = User.objects.filter(role='ADMIN').order_by('email')
        return super(CompanyUpdateView, self).dispatch(
            request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(CompanyUpdateView, self).get_form_kwargs()
        kwargs.update({"company": True})
        kwargs.update({"request_user": self.request.user})
        # if self.request.user.role != "ADMIN" and not self.request.user.is_superuser:
        #     kwargs.update({"request_user": self.request.user})
        return kwargs

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)

        return self.form_invalid(form)

    def form_valid(self, form):
        # Save Company
        company_object = form.save(commit=False)
        company_object.save()
        #previous_assigned_to_users = list(company_object.assigned_to.all().values_list('id', flat=True))
        company_object.tags.clear()
        if self.request.POST.get('tags', ''):
            tags = self.request.POST.get("tags")
            splitted_tags = tags.split(",")
            for t in splitted_tags:
                tag = Tags.objects.filter(name=t.lower())
                if tag:
                    tag = tag[0]
                else:
                    tag = Tags.objects.create(name=t.lower())
                company_object.tags.add(tag)
        if self.request.POST.getlist('contacts', []):
            company_object.contacts.clear()
            company_object.contacts.add(*self.request.POST.getlist('contacts'))
        if self.request.POST.getlist('assigned_to', []):
            company_object.assigned_to.clear()
            company_object.assigned_to.add(*self.request.POST.getlist('assigned_to'))
        else:
            company_object.assigned_to.clear()
        if self.request.FILES.get('company_attachment'):
            attachment = Attachments()
            attachment.created_by = self.request.user
            attachment.file_name = self.request.FILES.get(
                'company_attachment').name
            attachment.company = company_object
            attachment.attachment = self.request.FILES.get(
                'company_attachment')
            attachment.save()

        if self.request.POST.getlist('teams', []):
            company_object.teams.clear()
            company_object.teams.add(*self.request.POST.getlist('teams'))
        else:
            company_object.teams.clear()


        if self.request.POST.getlist('teams', []):
            user_ids = Teams.objects.filter(id__in=self.request.POST.getlist('teams')).values_list('users', flat=True)
            assinged_to_users_ids = company_object.assigned_to.all().values_list('id', flat=True)
            for user_id in user_ids:
                if user_id not in assinged_to_users_ids:
                    company_object.assigned_to.add(user_id)

        assigned_to_list = list(company_object.assigned_to.all().values_list('id', flat=True))
        current_site = get_current_site(self.request)
        #recipients = list(set(assigned_to_list) - set(previous_assigned_to_users))
        #send_email_to_assigned_user.delay(recipients, company_object.id, domain=current_site.domain,
        #    protocol=self.request.scheme)

        if self.request.is_ajax():
            data = {'success_url': reverse_lazy(
                'companies:list'), 'error': False}
            return JsonResponse(data)
        return redirect("companies:list")

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        return self.render_to_response(
            self.get_context_data(form=form)
        )

    def get_context_data(self, **kwargs):
        context = super(CompanyUpdateView, self).get_context_data(**kwargs)
        context["company_obj"] = self.object
        if self.request.user.role != "ADMIN" and not self.request.user.is_superuser:
            if ((self.request.user != context['company_obj'].created_by ) and
                (self.request.user not in context['company_obj'].assigned_to.all())):
                raise PermissionDenied
        context["company_form"] = context["form"]
        if self.request.user.role != "ADMIN" and not self.request.user.is_superuser:
            self.users = self.users.filter(Q(role='ADMIN') | Q(id__in=[self.request.user.id,]))
        context["users"] = self.users
        context["industries"] = INDCHOICES
        context["countries"] = COUNTRIES
        context["contact_count"] = Contact.objects.count()
        if self.request.user.role == 'ADMIN':
            context["leads"] = Lead.objects.exclude(
                status__in=['converted', 'closed'])
        else:
            context["leads"] = Lead.objects.filter(
                Q(assigned_to__in=[self.request.user]) | Q(created_by=self.request.user)).exclude(
                status__in=['converted', 'closed'])
        context["lead_count"] = context["leads"].count()
        if self.request.user.role != "ADMIN" and not self.request.user.is_superuser:
            context["lead_count"] = Lead.objects.filter(
                Q(assigned_to__in=[self.request.user]) | Q(created_by=self.request.user)).exclude(status='closed').count()
        context["teams"] = Teams.objects.all()
        return context


class CompanyDeleteView(AdminAccessRequiredMixin, LoginRequiredMixin, DeleteView):
    model = Company
    template_name = 'view_company.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.request.user.role != "ADMIN" and not self.request.user.is_superuser:
            if self.request.user != self.object.created_by:
                raise PermissionDenied
        self.object.delete()
        return redirect("companies:list")


class AddCommentView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CompanyCommentForm
    http_method_names = ["post"]

    def post(self, request, *args, **kwargs):
        self.object = None
        self.company = get_object_or_404(
            Company, id=request.POST.get('companyid'))
        if (
            request.user == self.company.created_by or request.user.is_superuser or
            request.user.role == 'ADMIN' or request.user in self.company.assigned_to.all()
        ):
            form = self.get_form()
            if form.is_valid():
                return self.form_valid(form)
            return self.form_invalid(form)

        data = {
            'error': "You don't have permission to comment for this company."}
        return JsonResponse(data)

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.commented_by = self.request.user
        comment.company = self.company
        comment.save()
        comment_id = comment.id
        current_site = get_current_site(self.request)
        send_email_user_mentions.delay(comment_id, 'companies', domain=current_site.domain,
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
            form = CompanyCommentForm(request.POST, instance=self.comment_obj)
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
        send_email_user_mentions.delay(comment_id, 'companies', domain=current_site.domain,
            protocol=self.request.scheme)
        return JsonResponse({
            "comment_id": self.comment_obj.id,
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


class AddAttachmentView(LoginRequiredMixin, CreateView):
    model = Attachments
    form_class = CompanyAttachmentForm
    http_method_names = ["post"]

    def post(self, request, *args, **kwargs):
        self.object = None
        self.company = get_object_or_404(
            Company, id=request.POST.get('companyid'))
        if (
            request.user == self.company.created_by or
            request.user.is_superuser or
            request.user.role == 'ADMIN' or
            request.user in self.company.assigned_to.all()
        ):
            form = self.get_form()
            if form.is_valid():
                return self.form_valid(form)

            return self.form_invalid(form)

        data = {
            'error': "You don't have permission to add attachment \
            for this company."}
        return JsonResponse(data)

    def form_valid(self, form):
        attachment = form.save(commit=False)
        attachment.created_by = self.request.user
        attachment.file_name = attachment.attachment.name
        attachment.company = self.company
        attachment.save()
        return JsonResponse({
            "attachment_id": attachment.id,
            "attachment": attachment.file_name,
            "attachment_url": attachment.attachment.url,
            "download_url": reverse('common:download_attachment',
                                    kwargs={'pk': attachment.id}),
            "attachment_display": attachment.get_file_type_display(),
            "created_on": attachment.created_on,
            "created_on_arrow": attachment.created_on_arrow,
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
            data = {"acd": request.POST.get("attachment_id")}
            return JsonResponse(data)

        data = {
            'error': "You don't have permission to delete this attachment."}
        return JsonResponse(data)

@login_required
def create_mail(request):
    if request.method == 'GET':
        company = get_object_or_404(Company, pk=request.GET.get('company_id'))
        contacts_list = list(company.contacts.all().values('email'))
        TIMEZONE_CHOICES = [(tz, tz) for tz in pytz.common_timezones]
        email_form = EmailForm(company=company)
        return render(request, 'create_mail_companies.html', {'company_id': request.GET.get('company_id'),
            'contacts_list': contacts_list, 'email_form': email_form,
            "timezones": TIMEZONE_CHOICES, "settings_timezone": settings.TIME_ZONE})

    if request.method == 'POST':
        company = Company.objects.filter(id=request.POST.get('company_id')).first()
        if company:
            form = EmailForm(request.POST, company=company)
            if form.is_valid():
                contacts = form.data.get('recipients').split(',')
                email_obj = Email.objects.create(
                    from_company=company,
                    message_body=form.cleaned_data.get('message_body'),
                    message_subject=form.cleaned_data.get('message_subject'),
                    from_email=form.cleaned_data.get('from_email'),
                    timezone=form.cleaned_data.get('timezone'),
                )
                email_obj.recipients.add(*contacts)
                if request.POST.get('scheduled_later') != 'true':
                    send_email.delay(email_obj.id)
                else:
                    email_obj.scheduled_later = True
                    email_obj.scheduled_date_time = form.cleaned_data.get('scheduled_date_time')
                    email_obj.save()

                return JsonResponse({'error': False})
            else:
                return JsonResponse({'error': True, 'errors': form.errors})
        else:
            return JsonResponse({'error':True, 'message': "Company does not exist."})

# @login_required
# @sales_access_required
# def create_mail(request, pk):
#     company_obj = get_object_or_404(Company, pk=pk)
#     if request.method == 'GET':
#         context = {}
#         context['company_obj'] = company_obj
#         return render(request, 'create_email_for_contacts.html')


def get_contacts_for_company(request):
    company_id = request.POST.get('company_id')
    if company_id:
        company_obj = Company.objects.filter(pk=company_id).first()
        if company_obj:
            if company_obj.contacts.all():
                data = list(company_obj.contacts.values('id', 'email'))
                import json
                return HttpResponse(json.dumps(data))
        return JsonResponse({})
    return JsonResponse({})


def get_email_data_for_company(request):
    email_obj = Email.objects.filter(id=request.POST.get('email_company_id')).first()
    if email_obj:
        ctx  = {}
        ctx['subject'] = email_obj.message_subject
        ctx['body'] = email_obj.message_body
        ctx['created_on'] = email_obj.created_on
        ctx['contacts'] = list(email_obj.recipients.values('email'))
        ctx['error'] = False
        return JsonResponse(ctx)
    else:
        return JsonResponse({'error': True, 'data' : 'No emails found.'})