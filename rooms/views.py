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
from rooms.models import (
	RoomType,RoomProperty,RoomTypeFormula
)
from rooms.forms import RoomTypeForm, RoomTypeFormulaForm, RoomPropertyForm
from rooms.utils import DATA_TYPE

from project_items.models import Item
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
#from rooms.tasks import  create_project_room_history, create_sub_project_room_history

class RoomTypesListView(AdminAccessRequiredMixin, LoginRequiredMixin, TemplateView):
	model = RoomType
	context_object_name = "room_type_list"
	template_name = "room_types.html"

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
		context = super(RoomTypesListView, self).get_context_data(**kwargs)
		context["room_type_list"] = self.get_queryset()
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

class CreateRoomTypeView(AdminAccessRequiredMixin, LoginRequiredMixin, CreateView):
	model = RoomType
	form_class = RoomTypeForm
	template_name = "create_room_type.html"

	def dispatch(self, request, *args, **kwargs):
		return super(CreateRoomTypeView, self).dispatch(
			request, *args, **kwargs)

	def get_form_kwargs(self):
		kwargs = super(CreateRoomTypeView, self).get_form_kwargs()
		return kwargs

	def post(self, request, *args, **kwargs):
		self.object = None
		form = self.get_form()
		if form.is_valid():

			room_type_obj = form.save(commit=False)

			room_type_obj.save()
			form.save_m2m()
			return self.form_valid(form)

		return self.form_invalid(form)

	def form_valid(self, form):
		room_type_obj = form.save(commit=False)
		
		if self.request.is_ajax():
			return JsonResponse({'error': False})
		if self.request.POST.get("savenewform"):
			return redirect("rooms:add_room_type")

		return redirect('rooms:list_room_types')

	def form_invalid(self, form):
		if self.request.is_ajax():
			return JsonResponse({'error': True, 'room_type_errors': form.errors})
			#return JsonResponse({'error': True, 'project_room_errors': form.errors,
			#					 'address_errors': address_form.errors})
		return self.render_to_response(
			self.get_context_data(form=form))
			#self.get_context_data(form=form, address_form=address_form))

	def get_context_data(self, **kwargs):
		context = super(CreateRoomTypeView, self).get_context_data(**kwargs)
		context["room_type_form"] = context["form"]
		context["items"]=Item.objects.all()
		context["room_properties"]=RoomProperty.objects.all()

		return context

class RoomTypeDetailView(AdminAccessRequiredMixin, LoginRequiredMixin, DetailView):
	model = RoomType
	context_object_name = "room_type_record"
	template_name = "view_room_type.html"

	def get_queryset(self):
		queryset = super(RoomTypeDetailView, self).get_queryset()
		return queryset

	def get_context_data(self, **kwargs):
		context = super(RoomTypeDetailView, self).get_context_data(**kwargs)
		return context

class UpdateRoomTypeView(AdminAccessRequiredMixin, LoginRequiredMixin, UpdateView):
	model = RoomType
	form_class = RoomTypeForm
	template_name = "create_room_type.html"

	def dispatch(self, request, *args, **kwargs):
		return super(UpdateRoomTypeView, self).dispatch(
			request, *args, **kwargs)

	def get_form_kwargs(self):
		kwargs = super(UpdateRoomTypeView, self).get_form_kwargs()
		return kwargs

	def post(self, request, *args, **kwargs):
		self.object = self.get_object()
		room_type_obj=self.object
		#address_obj = self.object.address
		form = self.get_form()

		#address_form = BillingAddressForm(request.POST, instance=address_obj)
		#if form.is_valid() and address_form.is_valid():
		if form.is_valid():
			#addres_obj = address_form.save()
			
			#origin_status=self.object.status
			room_type_obj = form.save(commit=False)
			room_type_obj.save()
			form.save_m2m()
			return self.form_valid(form)
		return self.form_invalid(form)

	def form_valid(self, form):

		room_type_obj = form.save(commit=False)

		if self.request.is_ajax():
			return JsonResponse({'error': False})
		return redirect("rooms:list_room_types")

	def form_invalid(self, form):
		'''address_obj = self.object.address
		address_form = BillingAddressForm(
			self.request.POST, instance=address_obj)'''

		if self.request.is_ajax():
			return JsonResponse({'error': True, 'room_type_errors': form.errors})
			#return JsonResponse({'error': True, 'project_room_errors': form.errors,
			#					 'address_errors': address_form.errors})
		return self.render_to_response(
			#self.get_context_data(form=form, address_form=address_form))
			self.get_context_data(form=form))

	def get_context_data(self, **kwargs):
		context = super(UpdateRoomTypeView, self).get_context_data(**kwargs)
		context["room_type_obj"] = self.object
		context["room_type_formula_objs"]=self.object.room_type_formulas.all()
		context["items"]=Item.objects.all()
		context["room_properties"]=RoomProperty.objects.all()
		if (self.request.user.role != "ADMIN" and not self.request.user.is_superuser):
			raise PermissionDenied

		#context["address_obj"] = self.object.address
		context["room_type_form"] = context["form"]

		if "room_type_formula_form" in kwargs:
			context["room_type_formula_form"] = kwargs["room_type_formula_form"]
		else:
			if self.request.POST:
				context["room_type_formula_form"] = RoomTypeFormulaForm(self.request.POST)
			else:
				context["room_type_formula_form"] = RoomTypeFormulaForm()

		if "room_property_form" in kwargs:
			context["room_property_form"] = kwargs["room_property_form"]
		else:
			if self.request.POST:
				context["room_property_form"] = RoomPropertyForm(self.request.POST)
			else:
				context["room_property_form"] = RoomPropertyForm()

		return context



class RemoveRoomTypeView(AdminAccessRequiredMixin, LoginRequiredMixin, View):

	def get(self, request, *args, **kwargs):
		return self.post(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		room_type_id = kwargs.get("pk")
		self.object = get_object_or_404(RoomType, id=room_type_id)
		if (self.request.user.role != "ADMIN" and not
			self.request.user.is_superuser):
			raise PermissionDenied
		else:
			self.object.delete()
			if self.request.is_ajax():
				return JsonResponse({'error': False})
			return redirect("rooms:list_room_types")


class CreateRoomTypeFormulaView(AdminAccessRequiredMixin, LoginRequiredMixin, CreateView):
	model = RoomTypeFormula
	form_class = RoomTypeFormulaForm

	def dispatch(self, request, *args, **kwargs):
		return super(CreateRoomTypeFormulaView, self).dispatch(
			request, *args, **kwargs)

	def get_form_kwargs(self):
		kwargs = super(CreateRoomTypeFormulaView, self).get_form_kwargs()
		return kwargs

	def post(self, request, *args, **kwargs):
		self.object = None
		form = self.get_form()

		if form.is_valid():
			room_type_formula_obj = form.save(commit=False)
			room_type_formula_obj.save()
			return self.form_valid(form)

		return self.form_invalid(form)

	def form_valid(self, form):
		room_type_formula_obj = form.save(commit=False)

		if self.request.is_ajax():
			return JsonResponse({'error': False,'id':room_type_formula_obj.id})

		return JsonResponse({'error': False,'id':room_type_formula_obj.id})

	def form_invalid(self, form):
		#address_form = BillingAddressForm(self.request.POST)
		room_type_formula_form=RoomTypeFormulaForm(self.request.POST)
		if self.request.is_ajax():
			return JsonResponse({'error': True, 'room_type_formula_errors':room_type_formula_form.errors})
			#return JsonResponse({'error': True, 'function_item_errors': form.errors,
			#					 'address_errors': address_form.errors})
		return self.render_to_response(
			self.get_context_data(form=form))
			#self.get_context_data(form=form, address_form=address_form))

	def get_context_data(self, **kwargs):
		context = super(CreateRoomTypeFormulaView, self).get_context_data(**kwargs)
		context["room_type_formula_form"] = context["form"]

		return context

class UpdateRoomTypeFormulaView(AdminAccessRequiredMixin, LoginRequiredMixin, UpdateView):
	model = RoomTypeFormula
	form_class = RoomTypeFormulaForm

	def dispatch(self, request, *args, **kwargs):
		return super(UpdateRoomTypeFormulaView, self).dispatch(
			request, *args, **kwargs)

	def get_form_kwargs(self):
		kwargs = super(UpdateRoomTypeFormulaView, self).get_form_kwargs()

		return kwargs

	def post(self, request, *args, **kwargs):
		
		self.object = self.get_object()
		room_type_formula_obj=self.object
		form = self.get_form()
		

		if form.is_valid():
			
			room_type_formula_obj = form.save(commit=False)
			
			room_type_formula_obj.save()
			return self.form_valid(form)
		return self.form_invalid(form)

	def form_valid(self, form):
		
		room_type_formula_obj = form.save(commit=False)

		if self.request.is_ajax():
			return JsonResponse({'error': False,'id':room_type_formula_obj.id})
		return JsonResponse({'error': False,'id':room_type_formula_obj.id})

	def form_invalid(self, form):

		if self.request.is_ajax():
			return JsonResponse({'error': True, 'room_type_formula_errors': form.errors})

		return self.render_to_response(
			self.get_context_data(form=form))

	def get_context_data(self, **kwargs):
		context = super(UpdateRoomTypeFormulaView, self).get_context_data(**kwargs)
		context["room_type_formula_obj"] = self.object

		if (self.request.user.role != "ADMIN" and not
				self.request.user.is_superuser):
			#if self.request.user.id not in user_assgn_list:
			#	raise PermissionDenied
			raise PermissionDenied

		context["room_type_formula_form"] = context["form"]

		return context

class RemoveRoomTypeFormulaView(AdminAccessRequiredMixin, LoginRequiredMixin, View):

	def get(self, request, *args, **kwargs):
		return self.post(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		room_type_formula_id = request.POST.get('pk')
		self.object = get_object_or_404(RoomTypeFormula, id=room_type_formula_id)
		if (self.request.user.role != "ADMIN" and not
			self.request.user.is_superuser):
			raise PermissionDenied
		else:

			self.object.delete()
			if self.request.is_ajax():
				return JsonResponse({'error': False})
			return JsonResponse({'error': False})

class RoomPropertiesListView(AdminAccessRequiredMixin, LoginRequiredMixin, TemplateView):
	model = RoomProperty
	context_object_name = "room_property_list"
	template_name = "room_properties.html"

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
		context = super(RoomPropertiesListView, self).get_context_data(**kwargs)
		context["room_property_list"] = self.get_queryset()
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

class RoomPropertyDetailView(AdminAccessRequiredMixin, LoginRequiredMixin, DetailView):
	model = RoomProperty
	context_object_name = "room_property_record"
	template_name = "view_room_property.html"

	def get_queryset(self):
		queryset = super(RoomPropertyDetailView, self).get_queryset()
		return queryset

	def get_context_data(self, **kwargs):
		context = super(RoomPropertyDetailView, self).get_context_data(**kwargs)
		return context

class CreateRoomPropertyView(AdminAccessRequiredMixin, LoginRequiredMixin, CreateView):
	model = RoomProperty
	form_class = RoomPropertyForm
	template_name = "create_room_property.html"

	def dispatch(self, request, *args, **kwargs):
		return super(CreateRoomPropertyView, self).dispatch(
			request, *args, **kwargs)

	def get_form_kwargs(self):
		kwargs = super(CreateRoomPropertyView, self).get_form_kwargs()
		return kwargs

	def post(self, request, *args, **kwargs):
		self.object = None
		form = self.get_form()

		if form.is_valid():
			room_property_obj = form.save(commit=False)
			room_property_obj.save()
			return self.form_valid(form)

		return self.form_invalid(form)

	def form_valid(self, form):
		room_property_obj = form.save(commit=False)

		if self.request.is_ajax():
			return JsonResponse({'error': False,'id':room_property_obj.id})
		if self.request.POST.get("savenewform"):
			return redirect("rooms:add_room_property")

		return redirect("rooms:list_room_properties")

	def form_invalid(self, form):
		#address_form = BillingAddressForm(self.request.POST)
		room_property_form=RoomPropertyForm(self.request.POST)
		if self.request.is_ajax():
			return JsonResponse({'error': True, 'room_property_errors':room_property_form.errors})
			#return JsonResponse({'error': True, 'function_item_errors': form.errors,
			#					 'address_errors': address_form.errors})
		return self.render_to_response(
			self.get_context_data(form=form))
			#self.get_context_data(form=form, address_form=address_form))

	def get_context_data(self, **kwargs):
		context = super(CreateRoomPropertyView, self).get_context_data(**kwargs)
		context["room_property_form"] = context["form"]

		return context

class UpdateRoomPropertyView(AdminAccessRequiredMixin, LoginRequiredMixin, UpdateView):
	model = RoomProperty
	form_class = RoomPropertyForm
	template_name = "create_room_property.html"

	def dispatch(self, request, *args, **kwargs):
		return super(UpdateRoomPropertyView, self).dispatch(
			request, *args, **kwargs)

	def get_form_kwargs(self):
		kwargs = super(UpdateRoomPropertyView, self).get_form_kwargs()

		return kwargs

	def post(self, request, *args, **kwargs):
		
		self.object = self.get_object()
		room_property_obj=self.object
		form = self.get_form()
		

		if form.is_valid():
			
			room_property_obj = form.save(commit=False)
			
			room_property_obj.save()
			return self.form_valid(form)
		return self.form_invalid(form)

	def form_valid(self, form):
		
		room_property_obj = form.save(commit=False)

		if self.request.is_ajax():
			return JsonResponse({'error': False,'id':room_property_obj.id})
		return redirect("rooms:list_room_properties")

	def form_invalid(self, form):

		if self.request.is_ajax():
			return JsonResponse({'error': True, 'room_property_errors': form.errors})

		return self.render_to_response(
			self.get_context_data(form=form))

	def get_context_data(self, **kwargs):
		context = super(UpdateRoomPropertyView, self).get_context_data(**kwargs)
		context["room_property_obj"] = self.object

		if (self.request.user.role != "ADMIN" and not
				self.request.user.is_superuser):
			#if self.request.user.id not in user_assgn_list:
			#	raise PermissionDenied
			raise PermissionDenied

		context["room_property_form"] = context["form"]

		return context

class RemoveRoomPropertyView(AdminAccessRequiredMixin, LoginRequiredMixin, View):

	def get(self, request, *args, **kwargs):
		return self.post(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		room_property_id = kwargs.get("pk")
		self.object = get_object_or_404(RoomProperty, id=room_property_id)
		if (self.request.user.role != "ADMIN" and not
			self.request.user.is_superuser):
			raise PermissionDenied
		else:

			self.object.delete()
			if self.request.is_ajax():
				return JsonResponse({'error': False})
			return redirect("rooms:list_room_properties")