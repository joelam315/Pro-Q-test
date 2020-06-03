import json
import io
import os

import pdfkit
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.template.loader import render_to_string
from django.views.generic import (CreateView, DeleteView, DetailView, FormView,
								  TemplateView, UpdateView, View)

from common.models import Address, Attachments, Comment, User
from common.tasks import send_email_user_mentions
from quotations.forms import (QuotationAddressForm, QuotationAttachmentForm,
							QuotationCommentForm, QuotationForm)
from quotations.models import Quotation, QuotationHistory
from quotations.tasks import send_email, send_quotation_email, send_quotation_email_cancel, create_quotation_history
from common.access_decorators_mixins import (
	sales_access_required, marketing_access_required, SalesAccessRequiredMixin, MarketingAccessRequiredMixin)
from teams.models import Teams
from function_items.models import FunctionItem, FunctionItemHistory,SubFunctionItem,SubFunctionItemHistory
from function_items.utils import FUNCTION_TYPE
from quotations.utils import QUOTATION_STATUS

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework_simplejwt import authentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django.shortcuts import get_object_or_404

@api_view(['POST'])
@authentication_classes([authentication.JWTAuthentication])
@permission_classes([IsAuthenticated])
def quotations_list_api(request):
	if request.user.role == 'ADMIN' or request.user.is_superuser:
		quotations = Quotation.objects.all().distinct()
	else:
		quotations = Quotation.objects.filter(Q(assigned_to=request.user)).distinct()

	results=[quotation.as_intro() for quotation in quotations]
	return Response(json.dumps(results))


@login_required
@sales_access_required
def quotations_list(request):

	if request.user.role == 'ADMIN' or request.user.is_superuser:
		users = User.objects.all()
	# elif request.user.google.all():
	#	 # users = User.objects.none()
	#	 # users = User.objects.filter(id=request.user.id)
	#	 users = User.objects.filter(Q(role='ADMIN') | Q(id=request.user.id))
	elif request.user.role == 'USER':
		users = User.objects.filter(Q(role='ADMIN') | Q(id=request.user.id))
	status = QUOTATION_STATUS
	if request.user.role == 'ADMIN' or request.user.is_superuser:
		quotations = Quotation.objects.all().distinct()
	else:
		quotations = Quotation.objects.filter(Q(assigned_to=request.user)).distinct()

	if request.method == 'GET':
		context = {}
		if request.user.role == 'ADMIN' or request.user.is_superuser:
			quotations = Quotation.objects.all().distinct()
		else:
			quotations = Quotation.objects.filter(Q(assigned_to=request.user)).distinct()
		context['quotations'] = quotations.order_by('-created_on')
		context['status'] = status
		context['users'] = users
		user_ids = list(quotations.values_list('created_by', flat=True))
		user_ids.append(request.user.id)
		context['created_by_users'] = users.filter(is_active=True, id__in=user_ids)
		today = datetime.today().date()
		context['today'] = today
		return render(request, 'quotations_list.html', context)

	if request.method == 'POST':
		context = {}
		context['status'] = status
		context['users'] = users
		quotations = Quotation.objects.filter()
		if request.user.role == 'ADMIN' or request.user.is_superuser:
			quotations = quotations
		else:
			quotations = quotations.filter(
				Q(created_by=request.user) | Q(assigned_to=request.user)).distinct()

		if request.POST.get('quotation_title_number', None):
			quotations = quotations.filter(
				Q(quotation_title__icontains=request.POST.get('quotation_title_number')) |
				Q(quotation_number__icontains=request.POST.get('quotation_title_number')))

		if request.POST.get('created_by', None):
			quotations = quotations.filter(
				created_by__id=request.POST.get('created_by'))

		if request.POST.getlist('assigned_to', None):
			quotations = quotations.filter(
				assigned_to__in=request.POST.getlist('assigned_to'))
			context['assigned_to'] = request.POST.getlist('assigned_to')

		if request.POST.get('status', None):
			quotations = quotations.filter(status=request.POST.get('status'))

		'''if request.POST.get('total_amount', None):
			quotations = quotations.filter(
				total_amount=request.POST.get('total_amount'))'''

		user_ids = list(quotations.values_list('created_by', flat=True))
		user_ids.append(request.user.id)
		context['created_by_users'] = users.filter(is_active=True, id__in=user_ids)
		context['quotations'] = quotations.distinct().order_by('id')
		today = datetime.today().date()
		context['today'] = today
		return render(request, 'quotations_list.html', context)

@api_view(['POST'])
@authentication_classes([authentication.JWTAuthentication])
@permission_classes([IsAuthenticated])
def quotations_create_api(request):
	if request.user.role == 'ADMIN' or request.user.is_superuser:
		users = User.objects.all()

	elif request.user.role == 'USER':
		users = User.objects.filter(Q(role='ADMIN') | Q(id=request.user.id))

	ret={}
	ret["result"]=True
	data = json.loads(request.body)
	if data.get("quotation_title")==None:
		ret["result"]=False
		ret["reason"]="Missing quotation_title"
		return Response(ret,status=400)
	

	return Response(ret)



@login_required
@sales_access_required
def quotations_create(request):
	if request.method == 'GET':
		context = {}
		context["form"] = QuotationForm(request_user=request.user)
		# "prefix" use case in form, both from address and to address use the
		# same model and same model form, so the name attribute in the form will
		#  be same for the both forms and the address will be same for both
		# shipping and to address, so use prefix parameter to distinguish the
		# forms, don't remove this comment
		context["from_address_form"] = QuotationAddressForm(
			prefix='from')
		context["to_address_form"] = QuotationAddressForm(prefix='to')
		context['function_items']=FunctionItem.objects.filter(status="Approved")
		context['sub_function_items']=SubFunctionItem.objects.filter(status="Approved")
		context['function_item_type_choices']=FUNCTION_TYPE
		if request.user.role == 'ADMIN' or request.user.is_superuser:
			context['teams'] = Teams.objects.all()

		return render(request, 'quotation_create_1.html', context)

	if request.method == 'POST':
		form = QuotationForm(request.POST, request_user=request.user)
		from_address_form = QuotationAddressForm(
			request.POST, prefix='from')
		to_address_form = QuotationAddressForm(request.POST, prefix='to')
		if form.is_valid() and from_address_form.is_valid() and to_address_form.is_valid():
			from_address_obj = from_address_form.save()
			to_address_obj = to_address_form.save()
			quotation_obj = form.save(commit=False)
			quotation_obj.created_by = request.user
			quotation_obj.updated_by=request.user
			quotation_obj.from_address = from_address_obj
			quotation_obj.to_address = to_address_obj
			quotation_obj.save()
			form.save_m2m()

			if request.POST.getlist('teams', []):
				user_ids = Teams.objects.filter(id__in=request.POST.getlist('teams')).values_list('users', flat=True)
				assinged_to_users_ids = quotation_obj.assigned_to.all().values_list('id', flat=True)
				for user_id in user_ids:
					if user_id not in assinged_to_users_ids:
						quotation_obj.assigned_to.add(user_id)

			if request.POST.getlist('teams', []):
				quotation_obj.teams.add(*request.POST.getlist('teams'))

			create_quotation_history(quotation_obj.id, request.user.id, [])
			kwargs = {'domain': request.get_host(), 'protocol': request.scheme}
			assigned_to_list = list(quotation_obj.assigned_to.all().values_list('id', flat=True))
			send_email.delay(quotation_obj.id, assigned_to_list, **kwargs)
			if request.POST.get('from_company'):
				return JsonResponse({'error': False, 'success_url': reverse('companies:view_company',
					args=(request.POST.get('from_company'),))})
			return JsonResponse({'error': False, 'success_url': reverse('quotations:quotations_list')})
		else:
			return JsonResponse({'error': True, 'errors': form.errors,
								 'from_address_errors': from_address_form.errors,
								 'to_address_errors': to_address_form.errors})

@api_view(['POST'])
@authentication_classes([authentication.JWTAuthentication])
@permission_classes([IsAuthenticated])
def quotations_details_api(request):
	data = json.loads(request.body)
	ret={}
	ret["result"]=True
	if data.get("id")==None:
		ret["result"]=False
		ret["reason"]="Missing id"
		return Response(ret,status=400)
	if request.user.role == 'ADMIN' or request.user.is_superuser:
		users = User.objects.all()
	# elif request.user.google.all():
	#	# users = User.objects.none()
	#	# users = User.objects.filter(id=request.user.id)
	#	users = User.objects.filter(Q(role='ADMIN') | Q(id=request.user.id))
	elif request.user.role == 'USER':
		users = User.objects.filter(Q(role='ADMIN') | Q(id=request.user.id))
	status = QUOTATION_STATUS

	if request.user.role == 'ADMIN' or request.user.is_superuser:
		quotations = Quotation.objects.all().distinct()
	else:
		quotations = Quotation.objects.filter(Q(assigned_to=request.user)).distinct()
	
	quotation=get_object_or_404(quotations,id=data.get("id"))

	ret["result"]=quotation.as_json()
	return Response(ret)

@login_required
@sales_access_required
def quotation_details(request, quotation_id):
	quotation = get_object_or_404(Quotation.objects.select_related(
		'from_address', 'to_address'), pk=quotation_id)

	user_assigned_company = False
	user_assigned_companies = set(request.user.company_assigned_users.values_list('id', flat=True))
	quotation_companies = set(quotation.companies.values_list('id', flat=True))
	if user_assigned_companies.intersection(quotation_companies):
		user_assigned_company = True

	if not ((request.user.role == 'ADMIN') or
		(request.user.is_superuser) or
		(quotation.created_by == request.user) or
		(request.user in quotation.assigned_to.all()) or
		user_assigned_company):
		raise PermissionDenied

	if request.method == 'GET':
		context = {}
		context['quotation'] = quotation
		context['attachments'] = quotation.quotation_attachment.all()
		context['comments'] = quotation.quotation_comments.all()
		context['function_item_type_choices']=FUNCTION_TYPE
		context['quotation_history'] = quotation.quotation_history.all()
		if request.user.is_superuser or request.user.role == 'ADMIN':
			context['users_mention'] = list(
				User.objects.filter(is_active=True).values('username'))
		elif request.user != quotation.created_by:
			context['users_mention'] = [
				{'username': quotation.created_by.username}]
		else:
			context['users_mention'] = list(
				quotation.assigned_to.all().values('username'))
		return render(request, 'quotations_detail_1.html', context)

@login_required
@sales_access_required
def quotation_history_details(request, quotation_history_id):
	quotation_history = get_object_or_404(QuotationHistory.objects.select_related(
		'from_address', 'to_address'), pk=quotation_history_id)

	user_assigned_company = False
	'''user_assigned_companies = set(request.user.company_assigned_users.values_list('id', flat=True))
	quotation_companies = set(quotation_history.companies.values_list('id', flat=True))
	if user_assigned_companies.intersection(quotation_companies):
		user_assigned_company = True'''

	if not ((request.user.role == 'ADMIN') or
		(request.user.is_superuser) or
		(quotation_history.created_by == request.user) or
		(request.user in quotation_history.assigned_to.all()) or
		user_assigned_company):
		raise PermissionDenied

	if request.method == 'GET':
		context = {}
		context['quotation_history'] = quotation_history
		context['function_item_type_choices']=FUNCTION_TYPE
		if request.user.is_superuser or request.user.role == 'ADMIN':
			context['users_mention'] = list(
				User.objects.filter(is_active=True).values('username'))
		elif request.user != quotation_history.created_by:
			context['users_mention'] = [
				{'username': quotation_history.created_by.username}]
		else:
			context['users_mention'] = list(
				quotation_history.assigned_to.all().values('username'))
		return render(request, 'quotations_history_detail_1.html', context)


@login_required
@sales_access_required
def quotation_edit(request, quotation_id):
	quotation_obj = get_object_or_404(Quotation, pk=quotation_id)

	if not (request.user.role == 'ADMIN' or request.user.is_superuser or quotation_obj.created_by == request.user or request.user in quotation_obj.assigned_to.all()):
		raise PermissionDenied

	if request.method == 'GET':
		context = {}
		context['quotation_obj'] = quotation_obj
		context['teams'] = Teams.objects.all()
		context['attachments'] = quotation_obj.quotation_attachment.all()
		context['function_items']=FunctionItem.objects.filter(status="Approved")
		context['function_item_type_choices']=FUNCTION_TYPE
		context['sub_function_items']=SubFunctionItem.objects.filter(status="Approved")
		context['form'] = QuotationForm(
			instance=quotation_obj, request_user=request.user)
		context['from_address_form'] = QuotationAddressForm(prefix='from',
														  instance=quotation_obj.from_address)
		context['to_address_form'] = QuotationAddressForm(prefix='to',
														instance=quotation_obj.to_address)
		return render(request, 'quotation_create_1.html', context)

	if request.method == 'POST':
		form = QuotationForm(request.POST, instance=quotation_obj,
						   request_user=request.user)
		from_address_form = QuotationAddressForm(
			request.POST, instance=quotation_obj.from_address, prefix='from')
		to_address_form = QuotationAddressForm(
			request.POST, instance=quotation_obj.to_address, prefix='to')
		previous_assigned_to_users = list(quotation_obj.assigned_to.all().values_list('id', flat=True))
		if form.is_valid() and from_address_form.is_valid() and to_address_form.is_valid():
			form_changed_data = form.changed_data
			form_changed_data.remove('from_address')
			form_changed_data.remove('to_address')
			form_changed_data = form_changed_data + ['from_' + field for field in from_address_form.changed_data]
			form_changed_data = form_changed_data + ['to_' + field for field in to_address_form.changed_data]
			# if form_changed_data:
			#	 create_quotation_history(quotation_obj.id, request.user.id, form_changed_data)
			from_address_obj = from_address_form.save()
			to_address_obj = to_address_form.save()
			quotation_obj = form.save(commit=False)
			quotation_obj.updated_by = request.user
			quotation_obj.updated_on=datetime.now()
			quotation_obj.from_address = from_address_obj
			quotation_obj.to_address = to_address_obj
			quotation_obj.save()
			form.save_m2m()
			if form_changed_data:
				create_quotation_history(quotation_obj.id, request.user.id, form_changed_data)

			if request.POST.getlist('teams', []):
				user_ids = Teams.objects.filter(id__in=request.POST.getlist('teams')).values_list('users', flat=True)
				assinged_to_users_ids = quotation_obj.assigned_to.all().values_list('id', flat=True)
				for user_id in user_ids:
					if user_id not in assinged_to_users_ids:
						quotation_obj.assigned_to.add(user_id)

			if request.POST.getlist('teams', []):
				quotation_obj.teams.clear()
				quotation_obj.teams.add(*request.POST.getlist('teams'))
			else:
				quotation_obj.teams.clear()

			kwargs = {'domain': request.get_host(), 'protocol': request.scheme}

			assigned_to_list = list(quotation_obj.assigned_to.all().values_list('id', flat=True))
			recipients = list(set(assigned_to_list) - set(previous_assigned_to_users))
			# send_email_to_assigned_user.delay(recipients, company_object.id, domain=current_site.domain,
			#	 protocol=self.request.scheme)

			send_email.delay(quotation_obj.id, recipients, **kwargs)
			if request.POST.get('from_company'):
				return JsonResponse({'error': False, 'success_url': reverse('companies:view_company',
					args=(request.POST.get('from_company'),))})
			return JsonResponse({'error': False, 'success_url': reverse('quotations:quotations_list')})
		else:
			return JsonResponse({'error': True, 'errors': form.errors,
								 'from_address_errors': from_address_form.errors,
								 'to_address_errors': to_address_form.errors})


@login_required
@sales_access_required
def quotation_delete(request, quotation_id):
	quotation = get_object_or_404(Quotation, pk=quotation_id)
	if not (request.user.role == 'ADMIN' or request.user.is_superuser or quotation.created_by == request.user):
		raise PermissionDenied

	if request.method == 'GET':
		quotation.delete()
		if request.GET.get('view_company'):
			return redirect(reverse('companies:view_company', args=(request.GET.get('view_company'),)))
		return redirect('quotations:quotations_list')


@login_required
@sales_access_required
def quotation_send_mail(request, quotation_id):
	quotation = get_object_or_404(Quotation, pk=quotation_id)
	if not (request.user.role == 'ADMIN' or request.user.is_superuser or quotation.created_by == request.user):
		raise PermissionDenied

	if request.method == 'GET':
		Quotation.objects.filter(id=quotation_id).update(
			is_email_sent=True, status='Sent')
		kwargs = {'domain': request.get_host(), 'protocol': request.scheme}
		send_quotation_email.delay(quotation_id, **kwargs)
		return redirect('quotations:quotations_list')

@login_required
@sales_access_required
def quotation_change_status_request_to_approve_signed(request, quotation_id):
	quotation = get_object_or_404(Quotation, pk=quotation_id)
	if not (request.user.role == 'ADMIN' or request.user.is_superuser or quotation.created_by == request.user):
		raise PermissionDenied

	if request.method == 'GET':
		Quotation.objects.filter(id=quotation_id).update(status='Requested to Approve Signed')
		kwargs = {'domain': request.get_host(), 'protocol': request.scheme}
		# send_quotation_email.delay(quotation_id, **kwargs)
		return redirect('quotations:quotations_list')


@login_required
@sales_access_required
def quotation_change_status_signed(request, quotation_id):
	quotation = get_object_or_404(Quotation, pk=quotation_id)
	if not (request.user.role == 'ADMIN' or request.user.is_superuser):
		raise PermissionDenied

	if request.method == 'GET':
		Quotation.objects.filter(id=quotation_id).update(status='Signed')
		kwargs = {'domain': request.get_host(), 'protocol': request.scheme}
		# send_quotation_email.delay(quotation_id, **kwargs)
		return redirect('quotations:quotations_list')

@login_required
@sales_access_required
def quotation_change_status_request_to_approve_paid(request, quotation_id):
	quotation = get_object_or_404(Quotation, pk=quotation_id)
	if not (request.user.role == 'ADMIN' or request.user.is_superuser or quotation.created_by == request.user):
		raise PermissionDenied

	if request.method == 'GET':
		Quotation.objects.filter(id=quotation_id).update(status='Requested to Approve Paid')
		kwargs = {'domain': request.get_host(), 'protocol': request.scheme}
		# send_quotation_email.delay(quotation_id, **kwargs)
		return redirect('quotations:quotations_list')


@login_required
@sales_access_required
def quotation_change_status_paid(request, quotation_id):
	quotation = get_object_or_404(Quotation, pk=quotation_id)
	if not (request.user.role == 'ADMIN' or request.user.is_superuser):
		raise PermissionDenied

	if request.method == 'GET':
		Quotation.objects.filter(id=quotation_id).update(status='Paid')
		kwargs = {'domain': request.get_host(), 'protocol': request.scheme}
		# send_quotation_email.delay(quotation_id, **kwargs)
		return redirect('quotations:quotations_list')

@login_required
@sales_access_required
def quotation_change_status_cancelled(request, quotation_id):
	quotation = get_object_or_404(Quotation, pk=quotation_id)
	if not (request.user.role == 'ADMIN' or request.user.is_superuser or quotation.created_by == request.user):
		raise PermissionDenied

	if request.method == 'GET':
		Quotation.objects.filter(id=quotation_id).update(status='Cancelled')
		kwargs = {'domain': request.get_host(), 'protocol': request.scheme}
		send_quotation_email_cancel.delay(quotation_id, **kwargs)
		return redirect('quotations:quotations_list')

@login_required
@sales_access_required
def quotation_download(request, quotation_id):
	quotation = get_object_or_404(Quotation.objects.select_related(
		'from_address', 'to_address'), pk=quotation_id)
	if not (request.user.role == 'ADMIN' or request.user.is_superuser or quotation.created_by == request.user or request.user in quotation.assigned_to.all()):
		raise PermissionDenied

	if request.method == 'GET':
		context = {}
		context['quotation'] = quotation
		html = render_to_string('quotation_download_pdf.html', context=context)
		pdfkit.from_string(html, 'out.pdf', options={'encoding': "UTF-8"})
		pdf = open("out.pdf", 'rb')
		response = HttpResponse(pdf.read(), content_type='application/pdf')
		response['Content-Disposition'] = 'attachment; filename=Quotation.pdf'
		pdf.close()
		os.remove("out.pdf")
		return response


class AddCommentView(LoginRequiredMixin, CreateView):
	model = Comment
	form_class = QuotationCommentForm
	http_method_names = ["post"]

	def post(self, request, *args, **kwargs):
		self.object = None
		self.quotation = get_object_or_404(
			Quotation, id=request.POST.get('quotation_id'))
		if (
			request.user == self.quotation.created_by or request.user.is_superuser or
			request.user.role == 'ADMIN'
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
		comment.quotation = self.quotation
		comment.save()
		comment_id = comment.id
		current_site = get_current_site(self.request)
		send_email_user_mentions.delay(comment_id, 'quotations', domain=current_site.domain,
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
			form = QuotationCommentForm(request.POST, instance=self.comment_obj)
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
		send_email_user_mentions.delay(comment_id, 'quotations', domain=current_site.domain,
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
	form_class = QuotationAttachmentForm
	http_method_names = ["post"]

	def post(self, request, *args, **kwargs):
		self.object = None
		self.quotation = get_object_or_404(
			Quotation, id=request.POST.get('quotation_id'))
		if (
			request.user == self.quotation.created_by or
			request.user.is_superuser or
			request.user.role == 'ADMIN'
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
		attachment.quotation = self.quotation
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
