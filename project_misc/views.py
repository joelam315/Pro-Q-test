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
from project_misc.models import Misc
from project_misc.forms import MiscForm
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

class MiscListView(AdminAccessRequiredMixin,LoginRequiredMixin,TemplateView):
	model=Misc
	context_object_name="misc_list"
	template_name="miscs.html"

	def get_queryset(self):
		queryset = self.model.objects.all()

		request_post = self.request.POST
		if request_post:
			if request_post.get('name'):
				queryset = queryset.filter(
					name__icontains=request_post.get('name'))
			if request_post.get('suggested_unit_price'):
				queryset = queryset.filter(
					suggested_unit_price__icontains=request_post.get('suggested_unit_price'))
			if request_post.get('is_active'):
				queryset = queryset.filter(
					is_active__icontains=request_post.get('is_active'))

		return queryset.distinct()

	def get_context_data(self, **kwargs):
		context = super(MiscListView, self).get_context_data(**kwargs)
		context["misc_list"] = self.get_queryset()
		context["per_page"] = self.request.POST.get('per_page')
		#context["users"] = User.objects.filter(is_active=True).order_by('email')
		search = False
		if (
			self.request.POST.get('name') or
			self.request.POST.get('suggested_unit_price') or
			self.request.POST.get('is_active')
		):
			search = True
		context["search"] = search
		return context

	def post(self, request, *args, **kwargs):
		context = self.get_context_data(**kwargs)
		return self.render_to_response(context)

class CreateMiscView(AdminAccessRequiredMixin, LoginRequiredMixin, CreateView):
	model = Misc
	form_class = MiscForm
	template_name = "create_misc.html"

	def dispatch(self, request, *args, **kwargs):
		return super(CreateMiscView, self).dispatch(
			request, *args, **kwargs)

	def get_form_kwargs(self):
		kwargs = super(CreateMiscView, self).get_form_kwargs()
		return kwargs

	def post(self, request, *args, **kwargs):
		self.object = None
		form = self.get_form()
		if form.is_valid():

			misc_obj = form.save(commit=False)

			misc_obj.save()

			return self.form_valid(form)

		return self.form_invalid(form)

	def form_valid(self, form):
		misc_obj = form.save(commit=False)
		
		if self.request.is_ajax():
			return JsonResponse({'error': False})
		if self.request.POST.get("savenewform"):
			return redirect("project_misc:add_misc")

		return redirect('project_misc:list_miscs')

	def form_invalid(self, form):
		if self.request.is_ajax():
			return JsonResponse({'error': True, 'misc_errors': form.errors})
			#return JsonResponse({'error': True, 'project_item_errors': form.errors,
			#					 'address_errors': address_form.errors})
		return self.render_to_response(
			self.get_context_data(form=form))
			#self.get_context_data(form=form, address_form=address_form))

	def get_context_data(self, **kwargs):
		context = super(CreateMiscView, self).get_context_data(**kwargs)
		context["misc_form"] = context["form"]

		return context

class MiscDetailView(AdminAccessRequiredMixin, LoginRequiredMixin, DetailView):
	model = Misc
	context_object_name = "misc_record"
	template_name = "view_misc.html"

	def get_queryset(self):
		queryset = super(MiscDetailView, self).get_queryset()
		return queryset

	def get_context_data(self, **kwargs):
		context = super(MiscDetailView, self).get_context_data(**kwargs)
		return context

class UpdateMiscView(AdminAccessRequiredMixin, LoginRequiredMixin, UpdateView):
	model = Misc
	form_class = MiscForm
	template_name = "create_misc.html"

	def dispatch(self, request, *args, **kwargs):
		return super(UpdateMiscView, self).dispatch(
			request, *args, **kwargs)

	def get_form_kwargs(self):
		kwargs = super(UpdateMiscView, self).get_form_kwargs()
		return kwargs

	def post(self, request, *args, **kwargs):
		self.object = self.get_object()
		misc_obj=self.object
		#address_obj = self.object.address
		form = self.get_form()

		#address_form = BillingAddressForm(request.POST, instance=address_obj)
		#if form.is_valid() and address_form.is_valid():
		if form.is_valid():
			#addres_obj = address_form.save()
			
			#origin_status=self.object.status
			misc_obj = form.save(commit=False)
			misc_obj.save()
			return self.form_valid(form)
		return self.form_invalid(form)

	def form_valid(self, form):

		misc_obj = form.save(commit=False)

		if self.request.is_ajax():
			return JsonResponse({'error': False})
		return redirect("project_misc:list_miscs")

	def form_invalid(self, form):
		'''address_obj = self.object.address
		address_form = BillingAddressForm(
			self.request.POST, instance=address_obj)'''

		if self.request.is_ajax():
			return JsonResponse({'error': True, 'misc_errors': form.errors})
			#return JsonResponse({'error': True, 'project_item_errors': form.errors,
			#					 'address_errors': address_form.errors})
		return self.render_to_response(
			#self.get_context_data(form=form, address_form=address_form))
			self.get_context_data(form=form))

	def get_context_data(self, **kwargs):
		context = super(UpdateMiscView, self).get_context_data(**kwargs)
		context["misc_obj"] = self.object
		if (self.request.user.role != "ADMIN" and not self.request.user.is_superuser):
			raise PermissionDenied

		#context["address_obj"] = self.object.address
		context["misc_form"] = context["form"]

		return context



class RemoveMiscView(AdminAccessRequiredMixin, LoginRequiredMixin, View):

	def get(self, request, *args, **kwargs):
		return self.post(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		misc_id = kwargs.get("pk")
		self.object = get_object_or_404(Misc, id=misc_id)
		if (self.request.user.role != "ADMIN" and not
			self.request.user.is_superuser):
			raise PermissionDenied
		else:
			self.object.delete()
			if self.request.is_ajax():
				return JsonResponse({'error': False})
			return redirect("project_misc:list_miscs")
