from celery.task import task
from django.conf import settings
from django.core.mail import EmailMessage
from django.shortcuts import reverse
from django.template.loader import render_to_string

from common.models import User
from projects.models import Project, ProjectHistory
from marketing.models import BlockedDomain, BlockedEmail
from function_items.models import FunctionItemHistory, SubFunctionItemHistory
from django.db.models import Max


@task
def send_email(project_id, recipients, domain='demo.django-crm.io', protocol='http'):
    project = Project.objects.filter(id=project_id).first()
    created_by = project.created_by
    blocked_domains = BlockedDomain.objects.values_list('domain', flat=True)
    blocked_emails = BlockedEmail.objects.values_list('email', flat=True)
    for user in recipients:
        recipients_list = []
        user = User.objects.filter(id=user, is_active=True).first()
        if user:
            if (user.email not in blocked_emails) and (user.email.split('@')[-1] not in blocked_domains):
                recipients_list.append(user.email)
                subject = 'Shared an project with you.'
                context = {}
                context['project_title'] = project.project_title
                context['project_id'] = project_id
                context['project_created_by'] = project.created_by
                context["url"] = protocol + '://' + domain + \
                    reverse('projects:project_details', args=(project.id,))

                context['user'] = user
                html_content = render_to_string(
                    'assigned_to_email_template.html', context=context)
                msg = EmailMessage(
                    subject=subject, body=html_content, to=recipients_list)
                msg.content_subtype = "html"
                msg.send()
    recipients = project.companies.filter(status='open')
    if recipients.count() > 0:
        subject = 'Shared an project with you.'
        context = {}
        context['project_title'] = project.project_title
        context['project_id'] = project_id
        context['project_created_by'] = project.created_by
        context["url"] = protocol + '://' + domain + \
            reverse('projects:project_details', args=(project.id,))
        for recipient in recipients:
            context['user'] = recipient.email
            html_content = render_to_string(
                'assigned_to_email_template.html', context=context)
            msg = EmailMessage(
                subject=subject, body=html_content, to=[recipient.email, ])
            msg.content_subtype = "html"
            msg.send()



@task
def send_project_email(project_id, domain='demo.django-crm.io', protocol='http'):
    project = Project.objects.filter(id=project_id).first()
    if project:
        subject = 'CRM Project : {0}'.format(project.project_title)
        recipients = [project.email]
        context = {}
        context['project'] = project
        context['url'] = protocol + '://' + domain + \
            reverse('projects:project_details', args=(project.id,))
        html_content = render_to_string(
            'project_detail_email.html', context=context)
        msg = EmailMessage(subject=subject, body=html_content,
                           to=recipients)
        msg.content_subtype = "html"
        msg.send()


@task
def send_project_email_cancel(project_id, domain='demo.django-crm.io', protocol='http'):
    project = Project.objects.filter(id=project_id).first()
    if project:
        subject = 'CRM Project : {0}'.format(project.project_title)
        recipients = [project.email]
        context = {}
        context['project'] = project
        context['url'] = protocol + '://' + domain + \
            reverse('projects:project_details', args=(project.id,))
        html_content = render_to_string(
            'project_cancelled.html', context=context)
        msg = EmailMessage(subject=subject, body=html_content,
                           to=recipients)
        msg.content_subtype = "html"
        msg.send()


@task
def create_project_history(original_project_id, updated_by_user_id, changed_fields):
    """original_project_id, updated_by_user_id, changed_fields"""
    original_project = Project.objects.filter(id=original_project_id).first()
    created_by = original_project.created_by
    updated_by_user = User.objects.get(id=updated_by_user_id)
    changed_data = [(' '.join(field.split('_')).title()) for field in changed_fields]
    if len(changed_data) > 1:
        changed_data = ', '.join(changed_data[:-1]) + ' and ' + changed_data[-1] + ' have changed.'
    elif len(changed_data) == 1:
        changed_data = ', '.join(changed_data) + ' has changed.'
    else:
        changed_data = None

    if original_project.project_history.count() == 0:
        changed_data = 'Project Created.'
    if original_project:
        project_history = ProjectHistory()
        project_history.project = original_project
        project_history.project_title = original_project.project_title
        project_history.project_number = original_project.project_number
        project_history.from_address = original_project.from_address
        project_history.to_address = original_project.to_address
        project_history.name = original_project.name
        project_history.email = original_project.email
        project_history.quantity = original_project.quantity
        project_history.rate = original_project.rate
        project_history.total_amount = original_project.total_amount()
        #project_history.currency = original_project.currency
        project_history.phone = original_project.phone
        project_history.updated_by = updated_by_user
        project_history.created_by = original_project.created_by
        project_history.amount_due = original_project.amount_due
        project_history.amount_paid = original_project.amount_paid
        project_history.is_email_sent = original_project.is_email_sent
        project_history.status = original_project.status
        project_history.details = changed_data
        project_history.due_date = original_project.due_date
        project_history.save()

        lastest_function_items_history=FunctionItemHistory.objects.values('function_item').annotate(max_id=Max('id')).order_by()
        function_items_historys=lastest_function_items_history.filter(function_item__in=original_project.function_items.all())
        lastest_sub_function_items_history=SubFunctionItemHistory.objects.values('sub_function_item').annotate(max_id=Max('id')).order_by()
        sub_function_items_historys=lastest_sub_function_items_history.filter(sub_function_item__in=original_project.sub_function_items.all())
        project_history.function_items.set([history['max_id'] for history in function_items_historys.all()])
        project_history.sub_function_items.set([history['max_id'] for history in sub_function_items_historys.all()])
        project_history.assigned_to.set(original_project.assigned_to.all())
