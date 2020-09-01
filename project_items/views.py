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
from project_items.forms import ItemTypeForm, ItemTypeMaterialForm, ItemForm, ItemFormulaForm, ItemPropertyForm
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

class ItemTypesListView(AdminAccessRequiredMixin, LoginRequiredMixin, TemplateView):
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

class ItemTypeDetailView(AdminAccessRequiredMixin, LoginRequiredMixin, DetailView):
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

class ItemsListView(AdminAccessRequiredMixin, LoginRequiredMixin, TemplateView):
	model = Item
	context_object_name = "item_list"
	template_name = "items.html"

	def get_queryset(self):
		queryset = self.model.objects.all()

		request_post = self.request.POST
		if request_post:
			if request_post.get('name'):
				queryset = queryset.filter(
					name__icontains=request_post.get('name'))
			if request_post.get('item_type'):
				queryset = queryset.filter(
					item_type__name__icontains=request_post.get('item_type'))
			if request_post.get('value_based_price'):
				queryset = queryset.filter(
					value_based_price__icontains=request_post.get('value_based_price'))
			if request_post.get('is_active'):
				queryset = queryset.filter(
					is_active__icontains=request_post.get('is_active'))

		return queryset.distinct()

	def get_context_data(self, **kwargs):
		context = super(ItemsListView, self).get_context_data(**kwargs)
		context["item_list"] = self.get_queryset()
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

class CreateItemView(AdminAccessRequiredMixin, LoginRequiredMixin, CreateView):
	model = Item
	form_class = ItemForm
	template_name = "create_item.html"

	def dispatch(self, request, *args, **kwargs):
		return super(CreateItemView, self).dispatch(
			request, *args, **kwargs)

	def get_form_kwargs(self):
		kwargs = super(CreateItemView, self).get_form_kwargs()
		return kwargs

	def post(self, request, *args, **kwargs):
		self.object = None
		form = self.get_form()
		if form.is_valid():

			item_obj = form.save(commit=False)

			item_obj.save()
			form.save_m2m()
			return self.form_valid(form)

		return self.form_invalid(form)

	def form_valid(self, form):
		item_obj = form.save(commit=False)
		
		if self.request.is_ajax():
			return JsonResponse({'error': False})
		if self.request.POST.get("savenewform"):
			return redirect("project_items:add_item")

		return redirect('project_items:list_items')

	def form_invalid(self, form):
		item_form=ItemForm(self.request.POST)
		if self.request.is_ajax():
			return JsonResponse({'error': True, 'item_errors': form.errors})
			#return JsonResponse({'error': True, 'project_item_errors': form.errors,
			#					 'address_errors': address_form.errors})
		return self.render_to_response(
			self.get_context_data(form=form))
			#self.get_context_data(form=form, address_form=address_form))

	def get_context_data(self, **kwargs):
		context = super(CreateItemView, self).get_context_data(**kwargs)
		context["item_form"] = context["form"]
		context["item_properties"]=ItemProperty.objects.all()

		return context

class ItemDetailView(AdminAccessRequiredMixin, LoginRequiredMixin, DetailView):
	model = Item
	context_object_name = "item_record"
	template_name = "view_item.html"

	def get_queryset(self):
		queryset = super(ItemDetailView, self).get_queryset()
		return queryset

	def get_context_data(self, **kwargs):
		context = super(ItemDetailView, self).get_context_data(**kwargs)
		return context

class UpdateItemView(AdminAccessRequiredMixin, LoginRequiredMixin, UpdateView):
	model = Item
	form_class = ItemForm
	template_name = "create_item.html"

	def dispatch(self, request, *args, **kwargs):
		return super(UpdateItemView, self).dispatch(
			request, *args, **kwargs)

	def get_form_kwargs(self):
		kwargs = super(UpdateItemView, self).get_form_kwargs()
		return kwargs

	def post(self, request, *args, **kwargs):
		self.object = self.get_object()
		item_obj=self.object
		#address_obj = self.object.address
		form = self.get_form()

		#address_form = BillingAddressForm(request.POST, instance=address_obj)
		#if form.is_valid() and address_form.is_valid():
		if form.is_valid():
			#addres_obj = address_form.save()
			
			#origin_status=self.object.status
			item_obj = form.save(commit=False)
			item_obj.save()
			form.save_m2m()
			return self.form_valid(form)
		return self.form_invalid(form)

	def form_valid(self, form):

		item_obj = form.save(commit=False)

		if self.request.is_ajax():
			return JsonResponse({'error': False})
		return redirect("project_items:list_items")

	def form_invalid(self, form):
		'''address_obj = self.object.address
		address_form = BillingAddressForm(
			self.request.POST, instance=address_obj)'''

		if self.request.is_ajax():
			return JsonResponse({'error': True, 'item_errors': form.errors})
			#return JsonResponse({'error': True, 'project_item_errors': form.errors,
			#					 'address_errors': address_form.errors})
		return self.render_to_response(
			#self.get_context_data(form=form, address_form=address_form))
			self.get_context_data(form=form))

	def get_context_data(self, **kwargs):
		context = super(UpdateItemView, self).get_context_data(**kwargs)
		context["item_obj"] = self.object
		context["item_formula_objs"]=self.object.item_formulas.all()
		context["item_properties"]=ItemProperty.objects.all()
		if (self.request.user.role != "ADMIN" and not self.request.user.is_superuser):
			raise PermissionDenied

		#context["address_obj"] = self.object.address
		context["item_form"] = context["form"]
		if "item_formula_form" in kwargs:
			context["item_formula_form"] = kwargs["item_formula_form"]
		else:
			if self.request.POST:
				context["item_formula_form"] = ItemFormulaForm(self.request.POST)
			else:
				context["item_formula_form"] = ItemFormulaForm()

		if "item_property_form" in kwargs:
			context["item_property_form"] = kwargs["item_property_form"]
		else:
			if self.request.POST:
				context["item_property_form"] = ItemPropertyForm(self.request.POST)
			else:
				context["item_property_form"] = ItemPropertyForm()

		return context



class RemoveItemView(AdminAccessRequiredMixin, LoginRequiredMixin, View):

	def get(self, request, *args, **kwargs):
		return self.post(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		item_id = kwargs.get("pk")
		self.object = get_object_or_404(Item, id=item_id)
		if (self.request.user.role != "ADMIN" and not
			self.request.user.is_superuser):
			raise PermissionDenied
		else:
			self.object.delete()
			if self.request.is_ajax():
				return JsonResponse({'error': False})
			return redirect("project_items:list_item")

class CreateItemFormulaView(AdminAccessRequiredMixin, LoginRequiredMixin, CreateView):
	model = ItemFormula
	form_class = ItemFormulaForm

	def dispatch(self, request, *args, **kwargs):
		return super(CreateItemFormulaView, self).dispatch(
			request, *args, **kwargs)

	def get_form_kwargs(self):
		kwargs = super(CreateItemFormulaView, self).get_form_kwargs()
		return kwargs

	def post(self, request, *args, **kwargs):
		self.object = None
		form = self.get_form()

		if form.is_valid():
			item_formula_obj = form.save(commit=False)
			item_formula_obj.save()
			return self.form_valid(form)

		return self.form_invalid(form)

	def form_valid(self, form):
		item_formula_obj = form.save(commit=False)

		if self.request.is_ajax():
			return JsonResponse({'error': False,'id':item_formula_obj.id})

		return JsonResponse({'error': False,'id':item_formula_obj.id})

	def form_invalid(self, form):
		#address_form = BillingAddressForm(self.request.POST)
		item_formula_form=ItemFormulaForm(self.request.POST)
		if self.request.is_ajax():
			return JsonResponse({'error': True, 'item_formula_errors':item_formula_form.errors})
			#return JsonResponse({'error': True, 'function_item_errors': form.errors,
			#					 'address_errors': address_form.errors})
		return self.render_to_response(
			self.get_context_data(form=form))
			#self.get_context_data(form=form, address_form=address_form))

	def get_context_data(self, **kwargs):
		context = super(CreateItemFormulaView, self).get_context_data(**kwargs)
		context["item_formula_form"] = context["form"]

		return context

class UpdateItemFormulaView(AdminAccessRequiredMixin, LoginRequiredMixin, UpdateView):
	model = ItemFormula
	form_class = ItemFormulaForm

	def dispatch(self, request, *args, **kwargs):
		return super(UpdateItemFormulaView, self).dispatch(
			request, *args, **kwargs)

	def get_form_kwargs(self):
		kwargs = super(UpdateItemFormulaView, self).get_form_kwargs()

		return kwargs

	def post(self, request, *args, **kwargs):
		
		self.object = self.get_object()
		item_formula_obj=self.object
		form = self.get_form()
		

		if form.is_valid():
			
			item_formula_obj = form.save(commit=False)
			
			item_formula_obj.save()
			return self.form_valid(form)
		return self.form_invalid(form)

	def form_valid(self, form):
		
		item_formula_obj = form.save(commit=False)

		if self.request.is_ajax():
			return JsonResponse({'error': False,'id':item_formula_obj.id})
		return JsonResponse({'error': False,'id':item_formula_obj.id})

	def form_invalid(self, form):

		if self.request.is_ajax():
			return JsonResponse({'error': True, 'item_formula_errors': form.errors})

		return self.render_to_response(
			self.get_context_data(form=form))

	def get_context_data(self, **kwargs):
		context = super(UpdateItemFormulaView, self).get_context_data(**kwargs)
		context["item_formula_obj"] = self.object

		if (self.request.user.role != "ADMIN" and not
				self.request.user.is_superuser):
			#if self.request.user.id not in user_assgn_list:
			#	raise PermissionDenied
			raise PermissionDenied

		context["item_formula_form"] = context["form"]

		return context

class RemoveItemFormulaView(AdminAccessRequiredMixin, LoginRequiredMixin, View):

	def get(self, request, *args, **kwargs):
		return self.post(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		item_formula_id = request.POST.get('pk')
		self.object = get_object_or_404(ItemFormula, id=item_formula_id)
		if (self.request.user.role != "ADMIN" and not
			self.request.user.is_superuser):
			raise PermissionDenied
		else:

			self.object.delete()
			if self.request.is_ajax():
				return JsonResponse({'error': False})
			return JsonResponse({'error': False})

class ItemPropertiesListView(AdminAccessRequiredMixin, LoginRequiredMixin, TemplateView):
	model = ItemProperty
	context_object_name = "item_property_list"
	template_name = "item_properties.html"

	def get_queryset(self):
		queryset = self.model.objects.all()

		request_post = self.request.POST
		if request_post:
			if request_post.get('name'):
				queryset = queryset.filter(
					name__icontains=request_post.get('name'))
			if request_post.get('symbol'):
				queryset = queryset.filter(
					symbol__icontains=request_post.get('symbol'))

		return queryset.distinct()

	def get_context_data(self, **kwargs):
		context = super(ItemPropertiesListView, self).get_context_data(**kwargs)
		context["item_property_list"] = self.get_queryset()
		context["per_page"] = self.request.POST.get('per_page')
		#context["users"] = User.objects.filter(is_active=True).order_by('email')
		search = False
		if (
			self.request.POST.get('name') or
			self.request.POST.get('symbol')
		):
			search = True
		context["search"] = search
		return context

	def post(self, request, *args, **kwargs):
		context = self.get_context_data(**kwargs)
		return self.render_to_response(context)

class ItemPropertyDetailView(AdminAccessRequiredMixin, LoginRequiredMixin, DetailView):
	model = ItemProperty
	context_object_name = "item_property_record"
	template_name = "view_item_property.html"

	def get_queryset(self):
		queryset = super(ItemPropertyDetailView, self).get_queryset()
		return queryset

	def get_context_data(self, **kwargs):
		context = super(ItemPropertyDetailView, self).get_context_data(**kwargs)
		return context

class CreateItemPropertyView(AdminAccessRequiredMixin, LoginRequiredMixin, CreateView):
	model = ItemProperty
	form_class = ItemPropertyForm
	template_name = "create_item_property.html"

	def dispatch(self, request, *args, **kwargs):
		return super(CreateItemPropertyView, self).dispatch(
			request, *args, **kwargs)

	def get_form_kwargs(self):
		kwargs = super(CreateItemPropertyView, self).get_form_kwargs()
		return kwargs

	def post(self, request, *args, **kwargs):
		self.object = None
		form = self.get_form()

		if form.is_valid():
			item_property_obj = form.save(commit=False)
			item_property_obj.save()
			return self.form_valid(form)

		return self.form_invalid(form)

	def form_valid(self, form):
		item_property_obj = form.save(commit=False)

		if self.request.is_ajax():
			return JsonResponse({'error': False,'id':item_property_obj.id})
		if self.request.POST.get("savenewform"):
			return redirect("project_items:add_item_property")

		return redirect("project_items:list_item_properties")

	def form_invalid(self, form):
		#address_form = BillingAddressForm(self.request.POST)
		item_property_form=ItemPropertyForm(self.request.POST)
		if self.request.is_ajax():
			return JsonResponse({'error': True, 'item_property_errors':item_property_form.errors})
			#return JsonResponse({'error': True, 'function_item_errors': form.errors,
			#					 'address_errors': address_form.errors})
		return self.render_to_response(
			self.get_context_data(form=form))
			#self.get_context_data(form=form, address_form=address_form))

	def get_context_data(self, **kwargs):
		context = super(CreateItemPropertyView, self).get_context_data(**kwargs)
		context["item_property_form"] = context["form"]

		return context

class UpdateItemPropertyView(AdminAccessRequiredMixin, LoginRequiredMixin, UpdateView):
	model = ItemProperty
	form_class = ItemPropertyForm
	template_name = "create_item_property.html"

	def dispatch(self, request, *args, **kwargs):
		return super(UpdateItemPropertyView, self).dispatch(
			request, *args, **kwargs)

	def get_form_kwargs(self):
		kwargs = super(UpdateItemPropertyView, self).get_form_kwargs()

		return kwargs

	def post(self, request, *args, **kwargs):
		
		self.object = self.get_object()
		item_property_obj=self.object
		form = self.get_form()
		

		if form.is_valid():
			
			item_property_obj = form.save(commit=False)
			
			item_property_obj.save()
			return self.form_valid(form)
		return self.form_invalid(form)

	def form_valid(self, form):
		
		item_property_obj = form.save(commit=False)

		if self.request.is_ajax():
			return JsonResponse({'error': False,'id':item_property_obj.id})
		return redirect("project_items:list_item_properties")

	def form_invalid(self, form):

		if self.request.is_ajax():
			return JsonResponse({'error': True, 'item_property_errors': form.errors})

		return self.render_to_response(
			self.get_context_data(form=form))

	def get_context_data(self, **kwargs):
		context = super(UpdateItemPropertyView, self).get_context_data(**kwargs)
		context["item_property_obj"] = self.object

		if (self.request.user.role != "ADMIN" and not
				self.request.user.is_superuser):
			#if self.request.user.id not in user_assgn_list:
			#	raise PermissionDenied
			raise PermissionDenied

		context["item_property_form"] = context["form"]

		return context

class RemoveItemPropertyView(AdminAccessRequiredMixin, LoginRequiredMixin, View):

	def get(self, request, *args, **kwargs):
		return self.post(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		item_property_id = kwargs.get("pk")
		self.object = get_object_or_404(ItemProperty, id=item_property_id)
		if (self.request.user.role != "ADMIN" and not
			self.request.user.is_superuser):
			raise PermissionDenied
		else:

			self.object.delete()
			if self.request.is_ajax():
				return JsonResponse({'error': False})
			return redirect("project_items:list_item_properties")