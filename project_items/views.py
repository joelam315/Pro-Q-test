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
from project_items.forms import ItemTypeForm, ItemTypeMaterialForm
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
#from project_items.tasks import  create_project_item_history, create_sub_project_item_history

class ItemTypesListView(SalesAccessRequiredMixin, LoginRequiredMixin, TemplateView):
	model = ItemType
	context_object_name = "item_type_list"
	template_name = "item_types.html"

	def get_queryset(self):
		queryset = self.model.objects.all()

		request_post = self.request.POST
		if request_post:
			if request_post.get('name'):
				queryset = queryset.filter(
					name__icontains=request_post.get('name'))
			if request_post.get('is_active'):
				queryset = queryset.filter(
					is_active__icontains=request_post.get('is_active'))

		return queryset.distinct()

	def get_context_data(self, **kwargs):
		context = super(ItemTypesListView, self).get_context_data(**kwargs)
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
		if form.is_valid():

			item_type_obj = form.save(commit=False)

			item_type_obj.save()

			return self.form_valid(form)

		return self.form_invalid(form)

	def form_valid(self, form):
		item_type_obj = form.save(commit=False)
		
		if self.request.is_ajax():
			return JsonResponse({'error': False})
		if self.request.POST.get("savenewform"):
			return redirect("project_items:add_item_type")

		return redirect('project_items:list_item_types')

	def form_invalid(self, form):
		item_type_material_form=ItemTypeMaterialForm(self.request.POST)
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
	model = ItemType
	context_object_name = "item_type_record"
	template_name = "view_item_type.html"

	def get_queryset(self):
		queryset = super(ItemTypeDetailView, self).get_queryset()
		return queryset

	def get_context_data(self, **kwargs):
		context = super(ItemTypeDetailView, self).get_context_data(**kwargs)
		context['item_type_material']=self.object.item_type_materials.all()
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
		return redirect("project_items:list_item_types")

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
		context = super(UpdateItemTypeView, self).get_context_data(**kwargs)
		context["item_type_obj"] = self.object
		context["item_type_material_objs"]=self.object.item_type_materials.all()
		if (self.request.user.role != "ADMIN" and not self.request.user.is_superuser):
			raise PermissionDenied

		#context["address_obj"] = self.object.address
		context["item_type_form"] = context["form"]
		if "item_type_material_form" in kwargs:
			context["item_type_material_form"] = kwargs["item_type_material_form"]
		else:
			if self.request.POST:
				context["item_type_material_form"] = ItemTypeMaterialForm(self.request.POST)
			else:
				context["item_type_material_form"] = ItemTypeMaterialForm()

		return context



class RemoveItemTypeView(AdminAccessRequiredMixin, LoginRequiredMixin, View):

	def get(self, request, *args, **kwargs):
		return self.post(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		item_type_id = kwargs.get("pk")
		self.object = get_object_or_404(ItemType, id=item_type_id)
		if (self.request.user.role != "ADMIN" and not
			self.request.user.is_superuser):
			raise PermissionDenied
		else:
			self.object.delete()
			if self.request.is_ajax():
				return JsonResponse({'error': False})
			return redirect("project_items:list_item_types")

class CreateItemTypeMaterialView(AdminAccessRequiredMixin, LoginRequiredMixin, CreateView):
	model = ItemTypeMaterial
	form_class = ItemTypeMaterialForm

	def dispatch(self, request, *args, **kwargs):
		return super(CreateItemTypeMaterialView, self).dispatch(
			request, *args, **kwargs)

	def get_form_kwargs(self):
		kwargs = super(CreateItemTypeMaterialView, self).get_form_kwargs()
		return kwargs

	def post(self, request, *args, **kwargs):
		self.object = None
		form = self.get_form()

		if form.is_valid():
			item_type_material_obj = form.save(commit=False)
			item_type_material_obj.save()
			return self.form_valid(form)

		return self.form_invalid(form)

	def form_valid(self, form):
		item_type_material_obj = form.save(commit=False)

		if self.request.is_ajax():
			return JsonResponse({'error': False,'id':item_type_material_obj.id})

		return JsonResponse({'error': False,'id':item_type_material_obj.id})

	def form_invalid(self, form):
		#address_form = BillingAddressForm(self.request.POST)
		item_type_material_form=ItemTypeMaterialForm(self.request.POST)
		if self.request.is_ajax():
			return JsonResponse({'error': True, 'item_type_material_errors':item_type_material_form.errors})
			#return JsonResponse({'error': True, 'function_item_errors': form.errors,
			#					 'address_errors': address_form.errors})
		return self.render_to_response(
			self.get_context_data(form=form))
			#self.get_context_data(form=form, address_form=address_form))

	def get_context_data(self, **kwargs):
		context = super(CreateItemTypeMaterialView, self).get_context_data(**kwargs)
		context["item_type_material_form"] = context["form"]

		return context

class UpdateItemTypeMaterialView(AdminAccessRequiredMixin, LoginRequiredMixin, UpdateView):
	model = ItemTypeMaterial
	form_class = ItemTypeMaterialForm

	def dispatch(self, request, *args, **kwargs):
		return super(UpdateItemTypeMaterialView, self).dispatch(
			request, *args, **kwargs)

	def get_form_kwargs(self):
		kwargs = super(UpdateItemTypeMaterialView, self).get_form_kwargs()

		return kwargs

	def post(self, request, *args, **kwargs):
		
		self.object = self.get_object()
		item_type_material_obj=self.object
		form = self.get_form()
		

		if form.is_valid():
			
			item_type_material_obj = form.save(commit=False)
			
			item_type_material_obj.save()
			return self.form_valid(form)
		return self.form_invalid(form)

	def form_valid(self, form):
		
		item_type_material_obj = form.save(commit=False)

		if self.request.is_ajax():
			return JsonResponse({'error': False,'id':item_type_material_obj.id})
		return JsonResponse({'error': False,'id':item_type_material_obj.id})

	def form_invalid(self, form):

		if self.request.is_ajax():
			return JsonResponse({'error': True, 'item_type_material_errors': form.errors})

		return self.render_to_response(
			self.get_context_data(form=form))

	def get_context_data(self, **kwargs):
		context = super(UpdateItemTypeMaterialView, self).get_context_data(**kwargs)
		context["item_type_material_obj"] = self.object

		if (self.request.user.role != "ADMIN" and not
				self.request.user.is_superuser):
			#if self.request.user.id not in user_assgn_list:
			#	raise PermissionDenied
			raise PermissionDenied

		context["item_type_material_form"] = context["form"]
		context["users"] = self.users

		return context

class RemoveItemTypeMaterialView(AdminAccessRequiredMixin, LoginRequiredMixin, View):

	def get(self, request, *args, **kwargs):
		return self.post(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		item_type_material_id = request.POST.get('pk')
		self.object = get_object_or_404(ItemTypeMaterial, id=item_type_material_id)
		if (self.request.user.role != "ADMIN" and not
			self.request.user.is_superuser):
			raise PermissionDenied
		else:

			self.object.delete()
			if self.request.is_ajax():
				return JsonResponse({'error': False})
			return JsonResponse({'error': False})