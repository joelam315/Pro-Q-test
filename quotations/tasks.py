from celery.task import task
from django.conf import settings
from django.core.mail import EmailMessage
from django.shortcuts import reverse
from django.template.loader import render_to_string

from common.models import User
from quotations.models import Quotation, QuotationHistory
from marketing.models import BlockedDomain, BlockedEmail
from function_items.models import FunctionItemHistory, SubFunctionItemHistory
from django.db.models import Max


@task
def send_email(quotation_id, recipients, domain='demo.django-crm.io', protocol='http'):
    quotation = Quotation.objects.filter(id=quotation_id).first()
    created_by = quotation.created_by
    blocked_domains = BlockedDomain.objects.values_list('domain', flat=True)
    blocked_emails = BlockedEmail.objects.values_list('email', flat=True)
    for user in recipients:
        recipients_list = []
        user = User.objects.filter(id=user, is_active=True).first()
        if user:
            if (user.email not in blocked_emails) and (user.email.split('@')[-1] not in blocked_domains):
                recipients_list.append(user.email)
                subject = 'Shared an quotation with you.'
                context = {}
                context['quotation_title'] = quotation.quotation_title
                context['quotation_id'] = quotation_id
                context['quotation_created_by'] = quotation.created_by
                context["url"] = protocol + '://' + domain + \
                    reverse('quotations:quotation_details', args=(quotation.id,))

                context['user'] = user
                html_content = render_to_string(
                    'assigned_to_email_template.html', context=context)
                msg = EmailMessage(
                    subject=subject, body=html_content, to=recipients_list)
                msg.content_subtype = "html"
                msg.send()
    recipients = quotation.companies.filter(status='open')
    if recipients.count() > 0:
        subject = 'Shared an quotation with you.'
        context = {}
        context['quotation_title'] = quotation.quotation_title
        context['quotation_id'] = quotation_id
        context['quotation_created_by'] = quotation.created_by
        context["url"] = protocol + '://' + domain + \
            reverse('quotations:quotation_details', args=(quotation.id,))
        for recipient in recipients:
            context['user'] = recipient.email
            html_content = render_to_string(
                'assigned_to_email_template.html', context=context)
            msg = EmailMessage(
                subject=subject, body=html_content, to=[recipient.email, ])
            msg.content_subtype = "html"
            msg.send()



@task
def send_quotation_email(quotation_id, domain='demo.django-crm.io', protocol='http'):
    quotation = Quotation.objects.filter(id=quotation_id).first()
    if quotation:
        subject = 'CRM Quotation : {0}'.format(quotation.quotation_title)
        recipients = [quotation.email]
        context = {}
        context['quotation'] = quotation
        context['url'] = protocol + '://' + domain + \
            reverse('quotations:quotation_details', args=(quotation.id,))
        html_content = render_to_string(
            'quotation_detail_email.html', context=context)
        msg = EmailMessage(subject=subject, body=html_content,
                           to=recipients)
        msg.content_subtype = "html"
        msg.send()


@task
def send_quotation_email_cancel(quotation_id, domain='demo.django-crm.io', protocol='http'):
    quotation = Quotation.objects.filter(id=quotation_id).first()
    if quotation:
        subject = 'CRM Quotation : {0}'.format(quotation.quotation_title)
        recipients = [quotation.email]
        context = {}
        context['quotation'] = quotation
        context['url'] = protocol + '://' + domain + \
            reverse('quotations:quotation_details', args=(quotation.id,))
        html_content = render_to_string(
            'quotation_cancelled.html', context=context)
        msg = EmailMessage(subject=subject, body=html_content,
                           to=recipients)
        msg.content_subtype = "html"
        msg.send()


@task
def create_quotation_history(original_quotation_id, updated_by_user_id, changed_fields):
    """original_quotation_id, updated_by_user_id, changed_fields"""
    original_quotation = Quotation.objects.filter(id=original_quotation_id).first()
    created_by = original_quotation.created_by
    updated_by_user = User.objects.get(id=updated_by_user_id)
    changed_data = [(' '.join(field.split('_')).title()) for field in changed_fields]
    if len(changed_data) > 1:
        changed_data = ', '.join(changed_data[:-1]) + ' and ' + changed_data[-1] + ' have changed.'
    elif len(changed_data) == 1:
        changed_data = ', '.join(changed_data) + ' has changed.'
    else:
        changed_data = None

    if original_quotation.quotation_history.count() == 0:
        changed_data = 'Quotation Created.'
    if original_quotation:
        quotation_history = QuotationHistory()
        quotation_history.quotation = original_quotation
        quotation_history.quotation_title = original_quotation.quotation_title
        quotation_history.quotation_number = original_quotation.quotation_number
        quotation_history.from_address = original_quotation.from_address
        quotation_history.to_address = original_quotation.to_address
        quotation_history.name = original_quotation.name
        quotation_history.email = original_quotation.email
        quotation_history.quantity = original_quotation.quantity
        quotation_history.rate = original_quotation.rate
        quotation_history.total_amount = original_quotation.total_amount()
        #quotation_history.currency = original_quotation.currency
        quotation_history.phone = original_quotation.phone
        quotation_history.updated_by = updated_by_user
        quotation_history.created_by = original_quotation.created_by
        quotation_history.amount_due = original_quotation.amount_due
        quotation_history.amount_paid = original_quotation.amount_paid
        quotation_history.is_email_sent = original_quotation.is_email_sent
        quotation_history.status = original_quotation.status
        quotation_history.details = changed_data
        quotation_history.due_date = original_quotation.due_date
        quotation_history.save()

        lastest_function_items_history=FunctionItemHistory.objects.values('function_item').annotate(max_id=Max('id')).order_by()
        function_items_historys=lastest_function_items_history.filter(function_item__in=original_quotation.function_items.all())
        lastest_sub_function_items_history=SubFunctionItemHistory.objects.values('sub_function_item').annotate(max_id=Max('id')).order_by()
        sub_function_items_historys=lastest_sub_function_items_history.filter(sub_function_item__in=original_quotation.sub_function_items.all())
        quotation_history.function_items.set([history['max_id'] for history in function_items_historys.all()])
        quotation_history.sub_function_items.set([history['max_id'] for history in sub_function_items_historys.all()])
        quotation_history.assigned_to.set(original_quotation.assigned_to.all())
