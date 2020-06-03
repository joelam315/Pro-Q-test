import json
import os
from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.generic import (
	CreateView, UpdateView, DetailView, TemplateView, View)
from common.models import User
from project_items.models import ProjectItem,SubProjectItem
from project_items.forms import ProjectItemForm,SubProjectItemForm
from project_items.utils import PROJECT_TYPE, PROJECT_STATUS
from django.core.exceptions import PermissionDenied
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.db import IntegrityError
from common.access_decorators_mixins import (
	sales_access_required, marketing_access_required, SalesAccessRequiredMixin, MarketingAccessRequiredMixin, AdminAccessRequiredMixin)

from rest_framework.authentication import SessionAuthentication, BasicAuthentication 
from rest_framework_simplejwt import authentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.core.files.base import ContentFile
from project_items.tasks import  create_project_item_history, create_sub_project_item_history
from project_items.serializers import ProjectItemSerializer, RequestProjectItemSerializer

class ProjectItemsListAPIView(APIView):
	authentication_classes = [authentication.JWTAuthentication]
	permission_classes = [IsAuthenticated]
	model = ProjectItem

	@swagger_auto_schema(
		operation_description="Return approved Function Item", 

		responses={
		200: ProjectItemSerializer(),
		401: "{\"detail\":\"Authentication credentials were not provided.\"}"})
	def post(self, request):
		ret={}
		ret["result"]=True
		data = json.loads(request.body)
		#return Response(data)
		
		try:
			project_item=ProjectItem.objects.filter(status="Approved")
		except IntegrityError as e:
			ret["result"]=False
			ret["reason"]=str(e).split("DETAIL:  ")[1]
			return Response(ret,status=403)
		results = [ob.as_json() for ob in project_item]
		return Response(json.dumps(results))


class ProjectItemsListView(SalesAccessRequiredMixin, LoginRequiredMixin, TemplateView):
	model = ProjectItem
	context_object_name = "project_item_list"
	template_name = "project_items.html"

	def get_queryset(self):
		queryset = self.model.objects.all()
		'''if (self.request.user.role != "ADMIN" and not
				self.request.user.is_superuser):
			queryset = queryset.filter(
				Q(created_by=self.request.user))'''

		request_post = self.request.POST
		if request_post:
			if request_post.get('name'):
				queryset = queryset.filter(
					name__icontains=request_post.get('name'))
			if request_post.get('type'):
				queryset = queryset.filter(
					type__icontains=request_post.get('type'))

		return queryset.distinct()

	def get_context_data(self, **kwargs):
		context = super(ProjectItemsListView, self).get_context_data(**kwargs)
		context["project_item_list"] = self.get_queryset()
		context["per_page"] = self.request.POST.get('per_page')
		context["users"] = User.objects.filter(
			is_active=True).order_by('email')
		search = False
		if (
			self.request.POST.get('name') or
			self.request.POST.get('type')
		):
			search = True
		context["search"] = search
		return context

	def post(self, request, *args, **kwargs):
		context = self.get_context_data(**kwargs)
		return self.render_to_response(context)

class GetAllProjectItemsTypeAPIView(APIView):
	authentication_classes = [authentication.JWTAuthentication]
	permission_classes = [IsAuthenticated]
	model = ProjectItem

	@swagger_auto_schema(
		operation_description="Return All Function Item Type", 

		responses={
		200: "[string]",
		401: "{\"detail\":\"Authentication credentials were not provided.\"}"})
	def post(self, request):
		ret={}
		ret["result"]=True
		#return Response(data)
		
		try:
			project_item_type=PROJECT_TYPE
		except IntegrityError as e:
			ret["result"]=False
			ret["reason"]=str(e).split("DETAIL:  ")[1]
			return Response(ret,status=403)
		return Response(json.dumps([type[0] for type in project_item_type]))

class CreateProjectItemView(AdminAccessRequiredMixin, LoginRequiredMixin, CreateView):
	model = ProjectItem
	form_class = ProjectItemForm
	template_name = "create_project_item.html"

	def dispatch(self, request, *args, **kwargs):
		if self.request.user.role == 'ADMIN' or self.request.user.is_superuser:
			self.users = User.objects.filter(is_active=True).order_by('email')
		else:
			self.users = User.objects.filter(role='ADMIN').order_by('email')
		return super(CreateProjectItemView, self).dispatch(
			request, *args, **kwargs)

	def get_form_kwargs(self):
		kwargs = super(CreateProjectItemView, self).get_form_kwargs()
		if self.request.user.role == 'ADMIN' or self.request.user.is_superuser:
			self.users = User.objects.filter(is_active=True).order_by('email')
		return kwargs

	def post(self, request, *args, **kwargs):
		self.object = None
		form = self.get_form()
		#address_form = BillingAddressForm(request.POST)

		#if form.is_valid() and address_form.is_valid():
		if form.is_valid():
			#address_obj = address_form.save()

			project_item_obj = form.save(commit=False)

			#project_item_obj.address = address_obj
			project_item_obj.created_by = self.request.user
			project_item_obj.last_updated_by=self.request.user
			project_item_obj.save()

			return self.form_valid(form)

		return self.form_invalid(form)

	def form_valid(self, form):
		project_item_obj = form.save(commit=False)
		if self.request.POST.getlist('assigned_to', []):
			pass
			# for assigned_to_user in assigned_to_list:
			#	 user = get_object_or_404(User, pk=assigned_to_user)
			#	 mail_subject = 'Assigned to project_item.'
			#	 message = render_to_string(
			#		 'assigned_to/project_item_assigned.html', {
			#			 'user': user,
			#			 'domain': current_site.domain,
			#			 'protocol': self.request.scheme,
			#			 'project_item': project_item_obj
			#		 })
			#	 email = EmailMessage(mail_subject, message, to=[user.email])
			#	 email.content_subtype = "html"
			#	 email.send()

		#assigned_to_list = list(project_item_obj.assigned_to.all().values_list('id', flat=True))
		#current_site=get_current_site(self.request)
		#recipients = assigned_to_list
		#send_email_to_assigned_user.delay(recipients, project_item_obj.id, domain=current_site.domain,
		#	protocol=self.request.scheme)

		create_project_item_history(project_item_obj.id, self.request.user.id, [])
		if self.request.is_ajax():
			return JsonResponse({'error': False})
		if self.request.POST.get("savenewform"):
			return redirect("project_items:add_project_item")

		return redirect('project_items:list')

	def form_invalid(self, form):
		#address_form = BillingAddressForm(self.request.POST)
		sub_project_item_form=SubProjectItemForm(self.request.POST)
		if self.request.is_ajax():
			return JsonResponse({'error': True, 'project_item_errors': form.errors})
			#return JsonResponse({'error': True, 'project_item_errors': form.errors,
			#					 'address_errors': address_form.errors})
		return self.render_to_response(
			self.get_context_data(form=form))
			#self.get_context_data(form=form, address_form=address_form))

	def get_context_data(self, **kwargs):
		context = super(CreateProjectItemView, self).get_context_data(**kwargs)
		context["project_item_form"] = context["form"]
		context["users"] = self.users

		#context["countries"] = COUNTRIES
		#context["assignedto_list"] = [
		#	int(i) for i in self.request.POST.getlist('assigned_to', []) if i]
		#if "address_form" in kwargs:
		#	context["address_form"] = kwargs["address_form"]
		#else:
		#	if self.request.POST:
		#		context["address_form"] = BillingAddressForm(self.request.POST)
		#	else:
		#		context["address_form"] = BillingAddressForm()
		#context["types"] = PROJECT_TYPE
		#context["status"]=PROJECT_STATUS
		return context

class CreateSubProjectItemView(AdminAccessRequiredMixin, LoginRequiredMixin, CreateView):
	model = SubProjectItem
	form_class = SubProjectItemForm
	#template_name = "create_project_item.html"

	def dispatch(self, request, *args, **kwargs):
		if self.request.user.role == 'ADMIN' or self.request.user.is_superuser:
			self.users = User.objects.filter(is_active=True).order_by('email')
		else:
			self.users = User.objects.filter(role='ADMIN').order_by('email')
		return super(CreateSubProjectItemView, self).dispatch(
			request, *args, **kwargs)

	def get_form_kwargs(self):
		kwargs = super(CreateSubProjectItemView, self).get_form_kwargs()
		if self.request.user.role == 'ADMIN' or self.request.user.is_superuser:
			self.users = User.objects.filter(is_active=True).order_by('email')
		return kwargs

	def post(self, request, *args, **kwargs):
		self.object = None
		form = self.get_form()

		if form.is_valid():

			#sub_project_item_obj=sub_project_item_form.save()
			#project_item_obj=form.cleaned_data.get("related_project_item")
			sub_project_item_obj = form.save(commit=False)
			#sub_project_item_obj.related_project_item=project_item_obj
			#project_item_obj.address = address_obj
			sub_project_item_obj.created_by = self.request.user
			sub_project_item_obj.last_updated_by=self.request.user
			sub_project_item_obj.save()
			create_sub_project_item_history(sub_project_item_obj.id, self.request.user.id, [])

			return self.form_valid(form)

		return self.form_invalid(form)

	def form_valid(self, form):
		sub_project_item_obj = form.save(commit=False)

		if self.request.is_ajax():
			return JsonResponse({'error': False,'id':sub_project_item_obj.id})

		return JsonResponse({'error': False,'id':sub_project_item_obj.id})

	def form_invalid(self, form):
		#address_form = BillingAddressForm(self.request.POST)
		sub_project_item_form=SubProjectItemForm(self.request.POST)
		if self.request.is_ajax():
			return JsonResponse({'error': True, 'sub_project_item_errors':sub_project_item_form.errors})
			#return JsonResponse({'error': True, 'project_item_errors': form.errors,
			#					 'address_errors': address_form.errors})
		return self.render_to_response(
			self.get_context_data(form=form))
			#self.get_context_data(form=form, address_form=address_form))

	def get_context_data(self, **kwargs):
		context = super(CreateSubProjectItemView, self).get_context_data(**kwargs)
		context["sub_project_item_form"] = context["form"]
		context["users"] = self.users

		return context

class RequestProjectItemAPIView(APIView):
	authentication_classes = [authentication.JWTAuthentication]
	permission_classes = [IsAuthenticated]
	model = ProjectItem
	@swagger_auto_schema(
		operation_description="Create a Contact via API call", 
		request_body=RequestProjectItemSerializer,

		responses={
		200: "{\"result\":true}",
		400: "{\"result\":false,\"reason\":\"Missing name\"}"+
			"\n{\"result\":false,\"reason\":\"Missing type\"}",
		401: "{\"detail\":\"Authentication credentials were not provided.\"}",
		403: "{\"result\":false,\"reason\":\"{Key ([feild])=([field_value]) already exists.\"}"})

	def post(self, request):
		ret={}
		ret["result"]=True
		data = json.loads(request.body)
		img = None
		#return Response(data)
		if data.get("name")==None:
			ret["result"]=False
			ret["reason"]="Missing name"
			return Response(ret,status=400)
		if  data.get("type")==None:
			ret["result"]=False
			ret["reason"]="Missing type"
			return Response(ret,status=400)

		try:
			project_item=ProjectItem.objects.create(
				name=data.get("name"),
				type=data.get("type"),
				price=data.get("price") if data.get("price") else 0,
				description=data.get("description"),
				created_by=request.user,
				last_updated_by=request.user)
		except IntegrityError as e:
			ret["result"]=False
			ret["reason"]=str(e)
			return Response(ret,status=403)

		return Response(ret)

class RequestProjectItemView(SalesAccessRequiredMixin, LoginRequiredMixin, CreateView):
	model = ProjectItem
	form_class = ProjectItemForm
	template_name = "create_project_item.html"

	def dispatch(self, request, *args, **kwargs):
		if self.request.user.role == 'ADMIN' or self.request.user.is_superuser:
			self.users = User.objects.filter(is_active=True).order_by('email')
		else:
			self.users = User.objects.filter(role='ADMIN').order_by('email')
		return super(RequestProjectItemView, self).dispatch(
			request, *args, **kwargs)

	def get_form_kwargs(self):
		kwargs = super(RequestProjectItemView, self).get_form_kwargs()
		if self.request.user.role == 'ADMIN' or self.request.user.is_superuser:
			self.users = User.objects.filter(is_active=True).order_by('email')
		return kwargs

	def post(self, request, *args, **kwargs):
		self.object = None
		form = self.get_form()

		if form.is_valid():
			#address_obj = address_form.save()
			project_item_obj = form.save(commit=False)
			#project_item_obj.address = address_obj
			project_item_obj.created_by = self.request.user
			project_item_obj.last_updated_by=self.request.user
			project_item_obj.save()

			return self.form_valid(form)

		return self.form_invalid(form)

	def form_valid(self, form):
		project_item_obj = form.save(commit=False)
		if self.request.POST.getlist('assigned_to', []):
			pass

		if self.request.POST.get("status")!="Requested":
			form.errors="Status must be \"Requested\""
			return self.form_invalid(form)

		if self.request.is_ajax():
			return JsonResponse({'error': False})
		if self.request.POST.get("savenewform"):
			return redirect("project_items:request_project_item")

		return redirect('project_items:list')

	def form_invalid(self, form):
		if self.request.is_ajax():
			return JsonResponse({'error': True, 'project_item_errors': form.errors})

		return self.render_to_response(
			self.get_context_data(form=form))

	def get_context_data(self, **kwargs):
		context = super(RequestProjectItemView, self).get_context_data(**kwargs)
		context["project_item_form"] = context["form"]
		context["users"] = self.users
		return context

class ProjectItemDetailView(SalesAccessRequiredMixin, LoginRequiredMixin, DetailView):
	model = ProjectItem
	context_object_name = "project_item_record"
	template_name = "view_project_item.html"

	def get_queryset(self):
		queryset = super(ProjectItemDetailView, self).get_queryset()
		return queryset

	def get_context_data(self, **kwargs):
		context = super(ProjectItemDetailView, self).get_context_data(**kwargs)
		context['project_item_history'] = self.object.project_item_history.all()
		return context

class UpdateProjectItemView(AdminAccessRequiredMixin, LoginRequiredMixin, UpdateView):
	model = ProjectItem
	form_class = ProjectItemForm
	template_name = "create_project_item.html"

	def dispatch(self, request, *args, **kwargs):
		if self.request.user.role == 'ADMIN' or self.request.user.is_superuser:
			self.users = User.objects.filter(is_active=True).order_by('email')
		else:
			self.users = User.objects.filter(role='ADMIN').order_by('email')
		return super(UpdateProjectItemView, self).dispatch(
			request, *args, **kwargs)

	def get_form_kwargs(self):
		kwargs = super(UpdateProjectItemView, self).get_form_kwargs()
		'''if self.request.user.role == 'ADMIN' or self.request.user.is_superuser:
			self.users = User.objects.filter(is_active=True).order_by('email')
			kwargs.update({"assigned_to": self.users})'''
		return kwargs

	def post(self, request, *args, **kwargs):
		self.object = self.get_object()
		project_item_obj=self.object
		#address_obj = self.object.address
		form = self.get_form()

		#address_form = BillingAddressForm(request.POST, instance=address_obj)
		#if form.is_valid() and address_form.is_valid():
		if form.is_valid():
			#addres_obj = address_form.save()
			
			origin_status=self.object.status
			project_item_obj = form.save(commit=False)

			if 'status' in form.changed_data and form.cleaned_data["status"]=="Approved":
				project_item_obj.approved_by=self.request.user
				project_item_obj.approved_on=datetime.now()
			project_item_obj.status=form.cleaned_data["status"]
			#project_item_obj.address = addres_obj
			project_item_obj.last_updated_by=self.request.user
			project_item_obj.last_updated_on=datetime.now()
			project_item_obj.save()
			if form.changed_data:
				create_project_item_history(project_item_obj.id, self.request.user.id, form.changed_data)
			return self.form_valid(form)
		return self.form_invalid(form)

	def form_valid(self, form):

		project_item_obj = form.save(commit=False)

		if self.request.is_ajax():
			return JsonResponse({'error': False})
		return redirect("project_items:list")

	def form_invalid(self, form):
		'''address_obj = self.object.address
		address_form = BillingAddressForm(
			self.request.POST, instance=address_obj)'''

		if self.request.is_ajax():
			return JsonResponse({'error': True, 'project_item_errors': form.errors})
			#return JsonResponse({'error': True, 'project_item_errors': form.errors,
			#					 'address_errors': address_form.errors})
		return self.render_to_response(
			#self.get_context_data(form=form, address_form=address_form))
			self.get_context_data(form=form))

	def get_context_data(self, **kwargs):
		context = super(UpdateProjectItemView, self).get_context_data(**kwargs)
		context["project_item_obj"] = self.object
		context["sub_project_item_objs"] = self.object.sub_project_items.all()
		'''user_assgn_list = [
			assigned_to.id for assigned_to in context["project_item_obj"].assigned_to.all()]
		if self.request.user == context['project_item_obj'].created_by:
			user_assgn_list.append(self.request.user.id)'''
		if (self.request.user.role != "ADMIN" and not
				self.request.user.is_superuser):
			#if self.request.user.id not in user_assgn_list:
			#	raise PermissionDenied
			raise PermissionDenied

		#context["address_obj"] = self.object.address
		context["project_item_form"] = context["form"]
		context["users"] = self.users
		if "sub_project_item_form" in kwargs:
			context["sub_project_item_form"] = kwargs["sub_project_item_form"]
		else:
			if self.request.POST:
				context["sub_project_item_form"] = SubProjectItemForm(self.request.POST)
			else:
				context["sub_project_item_form"] = SubProjectItemForm()
		#context["types"] = PROJECT_TYPE
		#context["status"]=PROJECT_STATUS
		#context["countries"] = COUNTRIES
		#context["teams"] = Teams.objects.all()
		#context["assignedto_list"] = [
		#	int(i) for i in self.request.POST.getlist('assigned_to', []) if i]
		'''if "address_form" in kwargs:
			context["address_form"] = kwargs["address_form"]
		else:
			if self.request.POST:
				context["address_form"] = BillingAddressForm(
					self.request.POST, instance=context["address_obj"])
			else:
				context["address_form"] = BillingAddressForm(
					instance=context["address_obj"])'''
		return context

class UpdateSubProjectItemView(AdminAccessRequiredMixin, LoginRequiredMixin, UpdateView):
	model = SubProjectItem
	form_class = SubProjectItemForm

	def dispatch(self, request, *args, **kwargs):
		if self.request.user.role == 'ADMIN' or self.request.user.is_superuser:
			self.users = User.objects.filter(is_active=True).order_by('email')
		else:
			self.users = User.objects.filter(role='ADMIN').order_by('email')
		return super(UpdateSubProjectItemView, self).dispatch(
			request, *args, **kwargs)

	def get_form_kwargs(self):
		kwargs = super(UpdateSubProjectItemView, self).get_form_kwargs()

		return kwargs

	def post(self, request, *args, **kwargs):
		
		#sub_project_item_id = form.cleaned_data["id"]
		#self.object = get_object_or_404(SubProjectItem, id=sub_project_item_id)
		self.object = self.get_object()
		sub_project_item_obj=self.object
		form = self.get_form()
		

		if form.is_valid():
			
			origin_status=self.object.status
			sub_project_item_obj = form.save(commit=False)
			
			if 'status' in form.changed_data and form.cleaned_data["status"]=="Approved":
				sub_project_item_obj.approved_by=self.request.user
				sub_project_item_obj.approved_on=datetime.now()
			sub_project_item_obj.status=form.cleaned_data["status"]
			sub_project_item_obj.last_updated_by=self.request.user
			sub_project_item_obj.last_updated_on=datetime.now()
			sub_project_item_obj.save()
			if form.changed_data:
				create_sub_project_item_history(sub_project_item_obj.id, self.request.user.id, form.changed_data)
			return self.form_valid(form)
		return self.form_invalid(form)

	def form_valid(self, form):
		
		sub_project_item_obj = form.save(commit=False)

		if self.request.is_ajax():
			return JsonResponse({'error': False,'id':sub_project_item_obj.id})
		return JsonResponse({'error': False,'id':sub_project_item_obj.id})

	def form_invalid(self, form):

		if self.request.is_ajax():
			return JsonResponse({'error': True, 'sub_project_item_errors': form.errors})
			#return JsonResponse({'error': True, 'project_item_errors': form.errors,
			#					 'address_errors': address_form.errors})
		return self.render_to_response(
			#self.get_context_data(form=form, address_form=address_form))
			self.get_context_data(form=form))

	def get_context_data(self, **kwargs):
		context = super(UpdateSubProjectItemView, self).get_context_data(**kwargs)
		context["sub_project_item_obj"] = self.object

		if (self.request.user.role != "ADMIN" and not
				self.request.user.is_superuser):
			#if self.request.user.id not in user_assgn_list:
			#	raise PermissionDenied
			raise PermissionDenied

		context["sub_project_item_form"] = context["form"]
		context["users"] = self.users

		return context

class RemoveProjectItemView(AdminAccessRequiredMixin, LoginRequiredMixin, View):

	def get(self, request, *args, **kwargs):
		return self.post(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		project_item_id = kwargs.get("pk")
		self.object = get_object_or_404(ProjectItem, id=project_item_id)
		if (self.request.user.role != "ADMIN" and not
			self.request.user.is_superuser and
				self.request.user != self.object.created_by):
			raise PermissionDenied
		else:
			#if self.object.address_id:
			#	self.object.address.delete()
			self.object.delete()
			if self.request.is_ajax():
				return JsonResponse({'error': False})
			return redirect("project_items:list")

class RemoveSubProjectItemView(AdminAccessRequiredMixin, LoginRequiredMixin, View):

	def get(self, request, *args, **kwargs):
		return self.post(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		sub_project_item_id = request.POST.get('pk')
		self.object = get_object_or_404(SubProjectItem, id=sub_project_item_id)
		if (self.request.user.role != "ADMIN" and not
			self.request.user.is_superuser and
				self.request.user != self.object.created_by):
			raise PermissionDenied
		else:
			#if self.object.address_id:
			#	self.object.address.delete()
			self.object.delete()
			if self.request.is_ajax():
				return JsonResponse({'error': False})
			return JsonResponse({'error': False})