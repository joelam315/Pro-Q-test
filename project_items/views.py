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
from project_items.models import (
	ItemType,ItemProperty,ItemTypeMaterial,Item,ItemFormula
)
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

class ItemTypesListView(SalesAccessRequiredMixin, LoginRequiredMixin, TemplateView):
	model = ProjectItem
	context_object_name = "item_type_list"
	template_name = "item_types.html"

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
			if request_post.get('is_active'):
				queryset = queryset.filter(
					type__icontains=request_post.get('is_active'))

		return queryset.distinct()

	def get_context_data(self, **kwargs):
		context = super(ProjectItemsListView, self).get_context_data(**kwargs)
		context["item_type_list"] = self.get_queryset()
		context["per_page"] = self.request.POST.get('per_page')
		#context["users"] = User.objects.filter(is_active=True).order_by('email')
		search = False
		if (
			self.request.POST.get('name') or
			self.request.POST.get('is_active')
		):
			search = True
		context["search"] = search
		return context

	def post(self, request, *args, **kwargs):
		context = self.get_context_data(**kwargs)
		return self.render_to_response(context)

class CreateItemTypeView(AdminAccessRequiredMixin, LoginRequiredMixin, CreateView):
	model = ItemType
	form_class = ItemTypeForm
	template_name = "create_item_type.html"

	def dispatch(self, request, *args, **kwargs):
		return super(CreateItemTypeView, self).dispatch(
			request, *args, **kwargs)

	def get_form_kwargs(self):
		kwargs = super(CreateItemTypeView, self).get_form_kwargs()
		return kwargs

	def post(self, request, *args, **kwargs):
		self.object = None
		form = self.get_form()
		#address_form = BillingAddressForm(request.POST)

		#if form.is_valid() and address_form.is_valid():
		if form.is_valid():
			#address_obj = address_form.save()

			item_type_obj = form.save(commit=False)

			#project_item_obj.address = address_obj
			#item_type_obj.created_by = self.request.user
			#project_item_obj.last_updated_by=self.request.user
			item_type_obj.save()

			return self.form_valid(form)

		return self.form_invalid(form)

	def form_valid(self, form):
		item_type_obj = form.save(commit=False)
		
		if self.request.is_ajax():
			return JsonResponse({'error': False})
		if self.request.POST.get("savenewform"):
			return redirect("item_types:add_item_type")

		return redirect('item_types:list')

	def form_invalid(self, form):
		
		if self.request.is_ajax():
			return JsonResponse({'error': True, 'item_type_errors': form.errors})
			#return JsonResponse({'error': True, 'project_item_errors': form.errors,
			#					 'address_errors': address_form.errors})
		return self.render_to_response(
			self.get_context_data(form=form))
			#self.get_context_data(form=form, address_form=address_form))

	def get_context_data(self, **kwargs):
		context = super(CreateItemTypeView, self).get_context_data(**kwargs)
		context["item_type_form"] = context["form"]

		return context

class ItemTypeDetailView(SalesAccessRequiredMixin, LoginRequiredMixin, DetailView):
	model = ProjectItem
	context_object_name = "item_type_record"
	template_name = "view_item_type.html"

	def get_queryset(self):
		queryset = super(ItemTypeDetailView, self).get_queryset()
		return queryset

	def get_context_data(self, **kwargs):
		context = super(ItemTypeDetailView, self).get_context_data(**kwargs)
		return context

class UpdateItemTypeView(AdminAccessRequiredMixin, LoginRequiredMixin, UpdateView):
	model = ItemType
	form_class = ItemTypeForm
	template_name = "create_item_type.html"

	def dispatch(self, request, *args, **kwargs):
		return super(UpdateItemTypeView, self).dispatch(
			request, *args, **kwargs)

	def get_form_kwargs(self):
		kwargs = super(UpdateItemTypeView, self).get_form_kwargs()
		return kwargs

	def post(self, request, *args, **kwargs):
		self.object = self.get_object()
		item_type_obj=self.object
		#address_obj = self.object.address
		form = self.get_form()

		#address_form = BillingAddressForm(request.POST, instance=address_obj)
		#if form.is_valid() and address_form.is_valid():
		if form.is_valid():
			#addres_obj = address_form.save()
			
			#origin_status=self.object.status
			item_type_obj = form.save(commit=False)
			item_type_obj.save()
			return self.form_valid(form)
		return self.form_invalid(form)

	def form_valid(self, form):

		item_type_obj = form.save(commit=False)

		if self.request.is_ajax():
			return JsonResponse({'error': False})
		return redirect("item_types:list")

	def form_invalid(self, form):
		'''address_obj = self.object.address
		address_form = BillingAddressForm(
			self.request.POST, instance=address_obj)'''

		if self.request.is_ajax():
			return JsonResponse({'error': True, 'item_type_errors': form.errors})
			#return JsonResponse({'error': True, 'project_item_errors': form.errors,
			#					 'address_errors': address_form.errors})
		return self.render_to_response(
			#self.get_context_data(form=form, address_form=address_form))
			self.get_context_data(form=form))

	def get_context_data(self, **kwargs):
		context = super(UpdateProjectItemView, self).get_context_data(**kwargs)
		context["item_type_obj"] = self.object
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