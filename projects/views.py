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
from projects.forms import (ProjectAddressForm, ProjectAttachmentForm,
							ProjectCommentForm, ProjectForm)
from projects.models import Project, ProjectHistory
from projects.tasks import send_email, send_project_email, send_project_email_cancel, create_project_history
from common.access_decorators_mixins import (
	sales_access_required, marketing_access_required, SalesAccessRequiredMixin, MarketingAccessRequiredMixin)
from teams.models import Teams
from function_items.models import FunctionItem, FunctionItemHistory,SubFunctionItem,SubFunctionItemHistory
from function_items.utils import FUNCTION_TYPE
from projects.utils import PROJECT_STATUS

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework_simplejwt import authentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django.shortcuts import get_object_or_404

@api_view(['POST'])
@authentication_classes([authentication.JWTAuthentication])
@permission_classes([IsAuthenticated])
def projects_list_api(request):
	if request.user.role == 'ADMIN' or request.user.is_superuser:
		projects = Project.objects.all().distinct()
	else:
		projects = Project.objects.filter(Q(assigned_to=request.user)).distinct()

	results=[project.as_intro() for project in projects]
	return Response(json.dumps(results))


@login_required
@sales_access_required
def projects_list(request):

	if request.user.role == 'ADMIN' or request.user.is_superuser:
		users = User.objects.all()
	# elif request.user.google.all():
	#	 # users = User.objects.none()
	#	 # users = User.objects.filter(id=request.user.id)
	#	 users = User.objects.filter(Q(role='ADMIN') | Q(id=request.user.id))
	elif request.user.role == 'USER':
		users = User.objects.filter(Q(role='ADMIN') | Q(id=request.user.id))
	status = PROJECT_STATUS
	if request.user.role == 'ADMIN' or request.user.is_superuser:
		projects = Project.objects.all().distinct()
	else:
		projects = Project.objects.filter(Q(assigned_to=request.user)).distinct()

	if request.method == 'GET':
		context = {}
		if request.user.role == 'ADMIN' or request.user.is_superuser:
			projects = Project.objects.all().distinct()
		else:
			projects = Project.objects.filter(Q(assigned_to=request.user)).distinct()
		context['projects'] = projects.order_by('-created_on')
		context['status'] = status
		context['users'] = users
		user_ids = list(projects.values_list('created_by', flat=True))
		user_ids.append(request.user.id)
		context['created_by_users'] = users.filter(is_active=True, id__in=user_ids)
		today = datetime.today().date()
		context['today'] = today
		return render(request, 'projects_list.html', context)

	if request.method == 'POST':
		context = {}
		context['status'] = status
		context['users'] = users
		projects = Project.objects.filter()
		if request.user.role == 'ADMIN' or request.user.is_superuser:
			projects = projects
		else:
			projects = projects.filter(
				Q(created_by=request.user) | Q(assigned_to=request.user)).distinct()

		if request.POST.get('project_title_number', None):
			projects = projects.filter(
				Q(project_title__icontains=request.POST.get('project_title_number')) |
				Q(project_number__icontains=request.POST.get('project_title_number')))

		if request.POST.get('created_by', None):
			projects = projects.filter(
				created_by__id=request.POST.get('created_by'))

		if request.POST.getlist('assigned_to', None):
			projects = projects.filter(
				assigned_to__in=request.POST.getlist('assigned_to'))
			context['assigned_to'] = request.POST.getlist('assigned_to')

		if request.POST.get('status', None):
			projects = projects.filter(status=request.POST.get('status'))

		'''if request.POST.get('total_amount', None):
			projects = projects.filter(
				total_amount=request.POST.get('total_amount'))'''

		user_ids = list(projects.values_list('created_by', flat=True))
		user_ids.append(request.user.id)
		context['created_by_users'] = users.filter(is_active=True, id__in=user_ids)
		context['projects'] = projects.distinct().order_by('id')
		today = datetime.today().date()
		context['today'] = today
		return render(request, 'projects_list.html', context)

@api_view(['POST'])
@authentication_classes([authentication.JWTAuthentication])
@permission_classes([IsAuthenticated])
def projects_create_api(request):
	if request.user.role == 'ADMIN' or request.user.is_superuser:
		users = User.objects.all()

	elif request.user.role == 'USER':
		users = User.objects.filter(Q(role='ADMIN') | Q(id=request.user.id))

	ret={}
	ret["result"]=True
	data = json.loads(request.body)
	if data.get("project_title")==None:
		ret["result"]=False
		ret["reason"]="Missing project_title"
		return Response(ret,status=400)
	

	return Response(ret)



@login_required
@sales_access_required
def projects_create(request):
	if request.method == 'GET':
		context = {}
		context["form"] = ProjectForm(request_user=request.user)
		# "prefix" use case in form, both from address and to address use the
		# same model and same model form, so the name attribute in the form will
		#  be same for the both forms and the address will be same for both
		# shipping and to address, so use prefix parameter to distinguish the
		# forms, don't remove this comment
		context["from_address_form"] = ProjectAddressForm(
			prefix='from')
		context["to_address_form"] = ProjectAddressForm(prefix='to')
		context['function_items']=FunctionItem.objects.filter(status="Approved")
		context['sub_function_items']=SubFunctionItem.objects.filter(status="Approved")
		context['function_item_type_choices']=FUNCTION_TYPE
		if request.user.role == 'ADMIN' or request.user.is_superuser:
			context['teams'] = Teams.objects.all()

		return render(request, 'project_create_1.html', context)

	if request.method == 'POST':
		form = ProjectForm(request.POST, request_user=request.user)
		from_address_form = ProjectAddressForm(
			request.POST, prefix='from')
		to_address_form = ProjectAddressForm(request.POST, prefix='to')
		if form.is_valid() and from_address_form.is_valid() and to_address_form.is_valid():
			from_address_obj = from_address_form.save()
			to_address_obj = to_address_form.save()
			project_obj = form.save(commit=False)
			project_obj.created_by = request.user
			project_obj.updated_by=request.user
			project_obj.from_address = from_address_obj
			project_obj.to_address = to_address_obj
			project_obj.save()
			form.save_m2m()

			if request.POST.getlist('teams', []):
				user_ids = Teams.objects.filter(id__in=request.POST.getlist('teams')).values_list('users', flat=True)
				assinged_to_users_ids = project_obj.assigned_to.all().values_list('id', flat=True)
				for user_id in user_ids:
					if user_id not in assinged_to_users_ids:
						project_obj.assigned_to.add(user_id)

			if request.POST.getlist('teams', []):
				project_obj.teams.add(*request.POST.getlist('teams'))

			create_project_history(project_obj.id, request.user.id, [])
			kwargs = {'domain': request.get_host(), 'protocol': request.scheme}
			assigned_to_list = list(project_obj.assigned_to.all().values_list('id', flat=True))
			send_email.delay(project_obj.id, assigned_to_list, **kwargs)
			if request.POST.get('from_company'):
				return JsonResponse({'error': False, 'success_url': reverse('companies:view_company',
					args=(request.POST.get('from_company'),))})
			return JsonResponse({'error': False, 'success_url': reverse('projects:projects_list')})
		else:
			return JsonResponse({'error': True, 'errors': form.errors,
								 'from_address_errors': from_address_form.errors,
								 'to_address_errors': to_address_form.errors})

@api_view(['POST'])
@authentication_classes([authentication.JWTAuthentication])
@permission_classes([IsAuthenticated])
def projects_details_api(request):
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
	status = PROJECT_STATUS

	if request.user.role == 'ADMIN' or request.user.is_superuser:
		projects = Project.objects.all().distinct()
	else:
		projects = Project.objects.filter(Q(assigned_to=request.user)).distinct()
	
	project=get_object_or_404(projects,id=data.get("id"))

	ret["result"]=project.as_json()
	return Response(ret)

@login_required
@sales_access_required
def project_details(request, project_id):
	project = get_object_or_404(Project.objects.select_related(
		'from_address', 'to_address'), pk=project_id)

	user_assigned_company = False
	user_assigned_companies = set(request.user.company_assigned_users.values_list('id', flat=True))
	project_companies = set(project.companies.values_list('id', flat=True))
	if user_assigned_companies.intersection(project_companies):
		user_assigned_company = True

	if not ((request.user.role == 'ADMIN') or
		(request.user.is_superuser) or
		(project.created_by == request.user) or
		(request.user in project.assigned_to.all()) or
		user_assigned_company):
		raise PermissionDenied

	if request.method == 'GET':
		context = {}
		context['project'] = project
		context['attachments'] = project.project_attachment.all()
		context['comments'] = project.project_comments.all()
		context['function_item_type_choices']=FUNCTION_TYPE
		context['project_history'] = project.project_history.all()
		if request.user.is_superuser or request.user.role == 'ADMIN':
			context['users_mention'] = list(
				User.objects.filter(is_active=True).values('username'))
		elif request.user != project.created_by:
			context['users_mention'] = [
				{'username': project.created_by.username}]
		else:
			context['users_mention'] = list(
				project.assigned_to.all().values('username'))
		return render(request, 'projects_detail_1.html', context)

@login_required
@sales_access_required
def project_history_details(request, project_history_id):
	project_history = get_object_or_404(ProjectHistory.objects.select_related(
		'from_address', 'to_address'), pk=project_history_id)

	user_assigned_company = False
	'''user_assigned_companies = set(request.user.company_assigned_users.values_list('id', flat=True))
	project_companies = set(project_history.companies.values_list('id', flat=True))
	if user_assigned_companies.intersection(project_companies):
		user_assigned_company = True'''

	if not ((request.user.role == 'ADMIN') or
		(request.user.is_superuser) or
		(project_history.created_by == request.user) or
		(request.user in project_history.assigned_to.all()) or
		user_assigned_company):
		raise PermissionDenied

	if request.method == 'GET':
		context = {}
		context['project_history'] = project_history
		context['function_item_type_choices']=FUNCTION_TYPE
		if request.user.is_superuser or request.user.role == 'ADMIN':
			context['users_mention'] = list(
				User.objects.filter(is_active=True).values('username'))
		elif request.user != project_history.created_by:
			context['users_mention'] = [
				{'username': project_history.created_by.username}]
		else:
			context['users_mention'] = list(
				project_history.assigned_to.all().values('username'))
		return render(request, 'projects_history_detail_1.html', context)


@login_required
@sales_access_required
def project_edit(request, project_id):
	project_obj = get_object_or_404(Project, pk=project_id)

	if not (request.user.role == 'ADMIN' or request.user.is_superuser or project_obj.created_by == request.user or request.user in project_obj.assigned_to.all()):
		raise PermissionDenied

	if request.method == 'GET':
		context = {}
		context['project_obj'] = project_obj
		context['teams'] = Teams.objects.all()
		context['attachments'] = project_obj.project_attachment.all()
		context['function_items']=FunctionItem.objects.filter(status="Approved")
		context['function_item_type_choices']=FUNCTION_TYPE
		context['sub_function_items']=SubFunctionItem.objects.filter(status="Approved")
		context['form'] = ProjectForm(
			instance=project_obj, request_user=request.user)
		context['from_address_form'] = ProjectAddressForm(prefix='from',
														  instance=project_obj.from_address)
		context['to_address_form'] = ProjectAddressForm(prefix='to',
														instance=project_obj.to_address)
		return render(request, 'project_create_1.html', context)

	if request.method == 'POST':
		form = ProjectForm(request.POST, instance=project_obj,
						   request_user=request.user)
		from_address_form = ProjectAddressForm(
			request.POST, instance=project_obj.from_address, prefix='from')
		to_address_form = ProjectAddressForm(
			request.POST, instance=project_obj.to_address, prefix='to')
		previous_assigned_to_users = list(project_obj.assigned_to.all().values_list('id', flat=True))
		if form.is_valid() and from_address_form.is_valid() and to_address_form.is_valid():
			form_changed_data = form.changed_data
			form_changed_data.remove('from_address')
			form_changed_data.remove('to_address')
			form_changed_data = form_changed_data + ['from_' + field for field in from_address_form.changed_data]
			form_changed_data = form_changed_data + ['to_' + field for field in to_address_form.changed_data]
			# if form_changed_data:
			#	 create_project_history(project_obj.id, request.user.id, form_changed_data)
			from_address_obj = from_address_form.save()
			to_address_obj = to_address_form.save()
			project_obj = form.save(commit=False)
			project_obj.updated_by = request.user
			project_obj.updated_on=datetime.now()
			project_obj.from_address = from_address_obj
			project_obj.to_address = to_address_obj
			project_obj.save()
			form.save_m2m()
			if form_changed_data:
				create_project_history(project_obj.id, request.user.id, form_changed_data)

			if request.POST.getlist('teams', []):
				user_ids = Teams.objects.filter(id__in=request.POST.getlist('teams')).values_list('users', flat=True)
				assinged_to_users_ids = project_obj.assigned_to.all().values_list('id', flat=True)
				for user_id in user_ids:
					if user_id not in assinged_to_users_ids:
						project_obj.assigned_to.add(user_id)

			if request.POST.getlist('teams', []):
				project_obj.teams.clear()
				project_obj.teams.add(*request.POST.getlist('teams'))
			else:
				project_obj.teams.clear()

			kwargs = {'domain': request.get_host(), 'protocol': request.scheme}

			assigned_to_list = list(project_obj.assigned_to.all().values_list('id', flat=True))
			recipients = list(set(assigned_to_list) - set(previous_assigned_to_users))
			# send_email_to_assigned_user.delay(recipients, company_object.id, domain=current_site.domain,
			#	 protocol=self.request.scheme)

			send_email.delay(project_obj.id, recipients, **kwargs)
			if request.POST.get('from_company'):
				return JsonResponse({'error': False, 'success_url': reverse('companies:view_company',
					args=(request.POST.get('from_company'),))})
			return JsonResponse({'error': False, 'success_url': reverse('projects:projects_list')})
		else:
			return JsonResponse({'error': True, 'errors': form.errors,
								 'from_address_errors': from_address_form.errors,
								 'to_address_errors': to_address_form.errors})


@login_required
@sales_access_required
def project_delete(request, project_id):
	project = get_object_or_404(Project, pk=project_id)
	if not (request.user.role == 'ADMIN' or request.user.is_superuser or project.created_by == request.user):
		raise PermissionDenied

	if request.method == 'GET':
		project.delete()
		if request.GET.get('view_company'):
			return redirect(reverse('companies:view_company', args=(request.GET.get('view_company'),)))
		return redirect('projects:projects_list')


@login_required
@sales_access_required
def project_send_mail(request, project_id):
	project = get_object_or_404(Project, pk=project_id)
	if not (request.user.role == 'ADMIN' or request.user.is_superuser or project.created_by == request.user):
		raise PermissionDenied

	if request.method == 'GET':
		Project.objects.filter(id=project_id).update(
			is_email_sent=True, status='Sent')
		kwargs = {'domain': request.get_host(), 'protocol': request.scheme}
		send_project_email.delay(project_id, **kwargs)
		return redirect('projects:projects_list')

@login_required
@sales_access_required
def project_change_status_request_to_approve_signed(request, project_id):
	project = get_object_or_404(Project, pk=project_id)
	if not (request.user.role == 'ADMIN' or request.user.is_superuser or project.created_by == request.user):
		raise PermissionDenied

	if request.method == 'GET':
		Project.objects.filter(id=project_id).update(status='Requested to Approve Signed')
		kwargs = {'domain': request.get_host(), 'protocol': request.scheme}
		# send_project_email.delay(project_id, **kwargs)
		return redirect('projects:projects_list')


@login_required
@sales_access_required
def project_change_status_signed(request, project_id):
	project = get_object_or_404(Project, pk=project_id)
	if not (request.user.role == 'ADMIN' or request.user.is_superuser):
		raise PermissionDenied

	if request.method == 'GET':
		Project.objects.filter(id=project_id).update(status='Signed')
		kwargs = {'domain': request.get_host(), 'protocol': request.scheme}
		# send_project_email.delay(project_id, **kwargs)
		return redirect('projects:projects_list')

@login_required
@sales_access_required
def project_change_status_request_to_approve_paid(request, project_id):
	project = get_object_or_404(Project, pk=project_id)
	if not (request.user.role == 'ADMIN' or request.user.is_superuser or project.created_by == request.user):
		raise PermissionDenied

	if request.method == 'GET':
		Project.objects.filter(id=project_id).update(status='Requested to Approve Paid')
		kwargs = {'domain': request.get_host(), 'protocol': request.scheme}
		# send_project_email.delay(project_id, **kwargs)
		return redirect('projects:projects_list')


@login_required
@sales_access_required
def project_change_status_paid(request, project_id):
	project = get_object_or_404(Project, pk=project_id)
	if not (request.user.role == 'ADMIN' or request.user.is_superuser):
		raise PermissionDenied

	if request.method == 'GET':
		Project.objects.filter(id=project_id).update(status='Paid')
		kwargs = {'domain': request.get_host(), 'protocol': request.scheme}
		# send_project_email.delay(project_id, **kwargs)
		return redirect('projects:projects_list')

@login_required
@sales_access_required
def project_change_status_cancelled(request, project_id):
	project = get_object_or_404(Project, pk=project_id)
	if not (request.user.role == 'ADMIN' or request.user.is_superuser or project.created_by == request.user):
		raise PermissionDenied

	if request.method == 'GET':
		Project.objects.filter(id=project_id).update(status='Cancelled')
		kwargs = {'domain': request.get_host(), 'protocol': request.scheme}
		send_project_email_cancel.delay(project_id, **kwargs)
		return redirect('projects:projects_list')

@login_required
@sales_access_required
def project_download(request, project_id):
	project = get_object_or_404(Project.objects.select_related(
		'from_address', 'to_address'), pk=project_id)
	if not (request.user.role == 'ADMIN' or request.user.is_superuser or project.created_by == request.user or request.user in project.assigned_to.all()):
		raise PermissionDenied

	if request.method == 'GET':
		context = {}
		context['project'] = project
		html = render_to_string('project_download_pdf.html', context=context)
		pdfkit.from_string(html, 'out.pdf', options={'encoding': "UTF-8"})
		pdf = open("out.pdf", 'rb')
		response = HttpResponse(pdf.read(), content_type='application/pdf')
		response['Content-Disposition'] = 'attachment; filename=Project.pdf'
		pdf.close()
		os.remove("out.pdf")
		return response


class AddCommentView(LoginRequiredMixin, CreateView):
	model = Comment
	form_class = ProjectCommentForm
	http_method_names = ["post"]

	def post(self, request, *args, **kwargs):
		self.object = None
		self.project = get_object_or_404(
			Project, id=request.POST.get('project_id'))
		if (
			request.user == self.project.created_by or request.user.is_superuser or
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
		comment.project = self.project
		comment.save()
		comment_id = comment.id
		current_site = get_current_site(self.request)
		send_email_user_mentions.delay(comment_id, 'projects', domain=current_site.domain,
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
			form = ProjectCommentForm(request.POST, instance=self.comment_obj)
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
		send_email_user_mentions.delay(comment_id, 'projects', domain=current_site.domain,
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
	form_class = ProjectAttachmentForm
	http_method_names = ["post"]

	def post(self, request, *args, **kwargs):
		self.object = None
		self.project = get_object_or_404(
			Project, id=request.POST.get('project_id'))
		if (
			request.user == self.project.created_by or
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
		attachment.project = self.project
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
