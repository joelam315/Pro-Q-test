from celery.task import task
from django.core.mail import EmailMessage
from django.shortcuts import reverse
from django.template.loader import render_to_string

from common.models import User
from customers.models import Customer
from marketing.models import BlockedDomain, BlockedEmail


@task
def send_email_to_assigned_user(recipients, customer_id, domain='demo.django-crm.io', protocol='http'):
    """ Send Mail To Users When they are assigned to a customer """
    customer = Customer.objects.get(id=customer_id)
    blocked_domains = BlockedDomain.objects.values_list('domain', flat=True)
    blocked_emails = BlockedEmail.objects.values_list('email', flat=True)
    created_by = customer.created_by
    for user in recipients:
        recipients_list = []
        user = User.objects.filter(id=user, is_active=True).first()
        if user:
            if (user.email not in blocked_emails) and (user.email.split('@')[-1] not in blocked_domains):
                recipients_list.append(user.email)
                context = {}
                context["url"] = protocol + '://' + domain + \
                    reverse('customers:view_customer', args=(customer.id,))
                context["user"] = user
                context["customer"] = customer
                context["created_by"] = created_by
                subject = 'Assigned a customer for you.'
                html_content = render_to_string(
                    'assigned_to/customer_assigned.html', context=context)

                msg = EmailMessage(
                    subject,
                    html_content,
                    to=recipients_list
                )
                msg.content_subtype = "html"
                msg.send()
