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
from function_items.models import FunctionItem,SubFunctionItem
from function_items.forms import FunctionItemForm,SubFunctionItemForm
from function_items.utils import FUNCTION_TYPE, FUNCTION_STATUS
from django.core.exceptions import PermissionDenied
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.db import IntegrityError
from common.access_decorators_mixins import (
	sales_access_required, marketing_access_required, SalesAccessRequiredMixin, AdminAccessRequiredMixin,MarketingAccessRequiredMixin, AdminAccessRequiredMixin)

from rest_framework.authentication import SessionAuthentication, BasicAuthentication 
from rest_framework_simplejwt import authentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.core.files.base import ContentFile
from function_items.tasks import  create_function_item_history, create_sub_function_item_history
from function_items.serializers import FunctionItemSerializer, RequestFunctionItemSerializer

class FunctionItemsListAPIView(APIView):
	authentication_classes = [authentication.JWTAuthentication]
	permission_classes = [IsAuthenticated]
	model = FunctionItem

	@swagger_auto_schema(
		operation_description="Return approved Function Item", 

		responses={
		200: FunctionItemSerializer(),
		401: "{\"detail\":\"Authentication credentials were not provided.\"}"})
	def post(self, request):
		ret={}
		ret["result"]=True
		data = json.loads(request.body)
		#return Response(data)
		
		try:
			function_item=FunctionItem.objects.filter(status="Approved")
		except IntegrityError as e:
			ret["result"]=False
			ret["reason"]=str(e).split("DETAIL:  ")[1]
			return Response(ret,status=403)
		results = [ob.as_json() for ob in function_item]
		return Response(json.dumps(results))


class FunctionItemsListView(AdminAccessRequiredMixin, LoginRequiredMixin, TemplateView):
	model = FunctionItem
	context_object_name = "function_item_list"
	template_name = "function_items.html"

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
		context = super(FunctionItemsListView, self).get_context_data(**kwargs)
		context["function_item_list"] = self.get_queryset()
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

class GetAllFunctionItemsTypeAPIView(APIView):
	authentication_classes = [authentication.JWTAuthentication]
	permission_classes = [IsAuthenticated]
	model = FunctionItem

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
			function_item_type=FUNCTION_TYPE
		except IntegrityError as e:
			ret["result"]=False
			ret["reason"]=str(e).split("DETAIL:  ")[1]
			return Response(ret,status=403)
		return Response(json.dumps([type[0] for type in function_item_type]))

class CreateFunctionItemView(AdminAccessRequiredMixin, LoginRequiredMixin, CreateView):
	model = FunctionItem
	form_class = FunctionItemForm
	template_name = "create_function_item.html"

	def dispatch(self, request, *args, **kwargs):
		if self.request.user.role == 'ADMIN' or self.request.user.is_superuser:
			self.users = User.objects.filter(is_active=True).order_by('email')
		else:
			self.users = User.objects.filter(role='ADMIN').order_by('email')
		return super(CreateFunctionItemView, self).dispatch(
			request, *args, **kwargs)

	def get_form_kwargs(self):
		kwargs = super(CreateFunctionItemView, self).get_form_kwargs()
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

			function_item_obj = form.save(commit=False)

			#function_item_obj.address = address_obj
			function_item_obj.created_by = self.request.user
			function_item_obj.last_updated_by=self.request.user
			function_item_obj.save()

			return self.form_valid(form)

		return self.form_invalid(form)

	def form_valid(self, form):
		function_item_obj = form.save(commit=False)
		if self.request.POST.getlist('assigned_to', []):
			pass
			# for assigned_to_user in assigned_to_list:
			#	 user = get_object_or_404(User, pk=assigned_to_user)
			#	 mail_subject = 'Assigned to function_item.'
			#	 message = render_to_string(
			#		 'assigned_to/function_item_assigned.html', {
			#			 'user': user,
			#			 'domain': current_site.domain,
			#			 'protocol': self.request.scheme,
			#			 'function_item': function_item_obj
			#		 })
			#	 email = EmailMessage(mail_subject, message, to=[user.email])
			#	 email.content_subtype = "html"
			#	 email.send()

		#assigned_to_list = list(function_item_obj.assigned_to.all().values_list('id', flat=True))
		#current_site=get_current_site(self.request)
		#recipients = assigned_to_list
		#send_email_to_assigned_user.delay(recipients, function_item_obj.id, domain=current_site.domain,
		#	protocol=self.request.scheme)

		create_function_item_history(function_item_obj.id, self.request.user.id, [])
		if self.request.is_ajax():
			return JsonResponse({'error': False})
		if self.request.POST.get("savenewform"):
			return redirect("function_items:add_function_item")

		return redirect('function_items:list')

	def form_invalid(self, form):
		#address_form = BillingAddressForm(self.request.POST)
		sub_function_item_form=SubFunctionItemForm(self.request.POST)
		if self.request.is_ajax():
			return JsonResponse({'error': True, 'function_item_errors': form.errors})
			#return JsonResponse({'error': True, 'function_item_errors': form.errors,
			#					 'address_errors': address_form.errors})
		return self.render_to_response(
			self.get_context_data(form=form))
			#self.get_context_data(form=form, address_form=address_form))

	def get_context_data(self, **kwargs):
		context = super(CreateFunctionItemView, self).get_context_data(**kwargs)
		context["function_item_form"] = context["form"]
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
		#context["types"] = FUNCTION_TYPE
		#context["status"]=FUNCTION_STATUS
		return context

class CreateSubFunctionItemView(AdminAccessRequiredMixin, LoginRequiredMixin, CreateView):
	model = SubFunctionItem
	form_class = SubFunctionItemForm
	#template_name = "create_function_item.html"

	def dispatch(self, request, *args, **kwargs):
		if self.request.user.role == 'ADMIN' or self.request.user.is_superuser:
			self.users = User.objects.filter(is_active=True).order_by('email')
		else:
			self.users = User.objects.filter(role='ADMIN').order_by('email')
		return super(CreateSubFunctionItemView, self).dispatch(
			request, *args, **kwargs)

	def get_form_kwargs(self):
		kwargs = super(CreateSubFunctionItemView, self).get_form_kwargs()
		if self.request.user.role == 'ADMIN' or self.request.user.is_superuser:
			self.users = User.objects.filter(is_active=True).order_by('email')
		return kwargs

	def post(self, request, *args, **kwargs):
		self.object = None
		form = self.get_form()

		if form.is_valid():

			#sub_function_item_obj=sub_function_item_form.save()
			#function_item_obj=form.cleaned_data.get("related_function_item")
			sub_function_item_obj = form.save(commit=False)
			#sub_function_item_obj.related_function_item=function_item_obj
			#function_item_obj.address = address_obj
			sub_function_item_obj.created_by = self.request.user
			sub_function_item_obj.last_updated_by=self.request.user
			sub_function_item_obj.save()
			create_sub_function_item_history(sub_function_item_obj.id, self.request.user.id, [])

			return self.form_valid(form)

		return self.form_invalid(form)

	def form_valid(self, form):
		sub_function_item_obj = form.save(commit=False)

		if self.request.is_ajax():
			return JsonResponse({'error': False,'id':sub_function_item_obj.id})

		return JsonResponse({'error': False,'id':sub_function_item_obj.id})

	def form_invalid(self, form):
		#address_form = BillingAddressForm(self.request.POST)
		sub_function_item_form=SubFunctionItemForm(self.request.POST)
		if self.request.is_ajax():
			return JsonResponse({'error': True, 'sub_function_item_errors':sub_function_item_form.errors})
			#return JsonResponse({'error': True, 'function_item_errors': form.errors,
			#					 'address_errors': address_form.errors})
		return self.render_to_response(
			self.get_context_data(form=form))
			#self.get_context_data(form=form, address_form=address_form))

	def get_context_data(self, **kwargs):
		context = super(CreateSubFunctionItemView, self).get_context_data(**kwargs)
		context["sub_function_item_form"] = context["form"]
		context["users"] = self.users

		return context

class RequestFunctionItemAPIView(APIView):
	authentication_classes = [authentication.JWTAuthentication]
	permission_classes = [IsAuthenticated]
	model = FunctionItem
	@swagger_auto_schema(
		operation_description="Create a Contact via API call", 
		request_body=RequestFunctionItemSerializer,

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
			function_item=FunctionItem.objects.create(
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

class RequestFunctionItemView(AdminAccessRequiredMixin, LoginRequiredMixin, CreateView):
	model = FunctionItem
	form_class = FunctionItemForm
	template_name = "create_function_item.html"

	def dispatch(self, request, *args, **kwargs):
		if self.request.user.role == 'ADMIN' or self.request.user.is_superuser:
			self.users = User.objects.filter(is_active=True).order_by('email')
		else:
			self.users = User.objects.filter(role='ADMIN').order_by('email')
		return super(RequestFunctionItemView, self).dispatch(
			request, *args, **kwargs)

	def get_form_kwargs(self):
		kwargs = super(RequestFunctionItemView, self).get_form_kwargs()
		if self.request.user.role == 'ADMIN' or self.request.user.is_superuser:
			self.users = User.objects.filter(is_active=True).order_by('email')
		return kwargs

	def post(self, request, *args, **kwargs):
		self.object = None
		form = self.get_form()

		if form.is_valid():
			#address_obj = address_form.save()
			function_item_obj = form.save(commit=False)
			#function_item_obj.address = address_obj
			function_item_obj.created_by = self.request.user
			function_item_obj.last_updated_by=self.request.user
			function_item_obj.save()

			return self.form_valid(form)

		return self.form_invalid(form)

	def form_valid(self, form):
		function_item_obj = form.save(commit=False)
		if self.request.POST.getlist('assigned_to', []):
			pass

		if self.request.POST.get("status")!="Requested":
			form.errors="Status must be \"Requested\""
			return self.form_invalid(form)

		if self.request.is_ajax():
			return JsonResponse({'error': False})
		if self.request.POST.get("savenewform"):
			return redirect("function_items:request_function_item")

		return redirect('function_items:list')

	def form_invalid(self, form):
		if self.request.is_ajax():
			return JsonResponse({'error': True, 'function_item_errors': form.errors})

		return self.render_to_response(
			self.get_context_data(form=form))

	def get_context_data(self, **kwargs):
		context = super(RequestFunctionItemView, self).get_context_data(**kwargs)
		context["function_item_form"] = context["form"]
		context["users"] = self.users
		return context

class FunctionItemDetailView(AdminAccessRequiredMixin, LoginRequiredMixin, DetailView):
	model = FunctionItem
	context_object_name = "function_item_record"
	template_name = "view_function_item.html"

	def get_queryset(self):
		queryset = super(FunctionItemDetailView, self).get_queryset()
		return queryset

	def get_context_data(self, **kwargs):
		context = super(FunctionItemDetailView, self).get_context_data(**kwargs)
		context['function_item_history'] = self.object.function_item_history.all()
		return context

class UpdateFunctionItemView(AdminAccessRequiredMixin, LoginRequiredMixin, UpdateView):
	model = FunctionItem
	form_class = FunctionItemForm
	template_name = "create_function_item.html"

	def dispatch(self, request, *args, **kwargs):
		if self.request.user.role == 'ADMIN' or self.request.user.is_superuser:
			self.users = User.objects.filter(is_active=True).order_by('email')
		else:
			self.users = User.objects.filter(role='ADMIN').order_by('email')
		return super(UpdateFunctionItemView, self).dispatch(
			request, *args, **kwargs)

	def get_form_kwargs(self):
		kwargs = super(UpdateFunctionItemView, self).get_form_kwargs()
		'''if self.request.user.role == 'ADMIN' or self.request.user.is_superuser:
			self.users = User.objects.filter(is_active=True).order_by('email')
			kwargs.update({"assigned_to": self.users})'''
		return kwargs

	def post(self, request, *args, **kwargs):
		self.object = self.get_object()
		function_item_obj=self.object
		#address_obj = self.object.address
		form = self.get_form()

		#address_form = BillingAddressForm(request.POST, instance=address_obj)
		#if form.is_valid() and address_form.is_valid():
		if form.is_valid():
			#addres_obj = address_form.save()
			
			origin_status=self.object.status
			function_item_obj = form.save(commit=False)

			if 'status' in form.changed_data and form.cleaned_data["status"]=="Approved":
				function_item_obj.approved_by=self.request.user
				function_item_obj.approved_on=datetime.now()
			function_item_obj.status=form.cleaned_data["status"]
			#function_item_obj.address = addres_obj
			function_item_obj.last_updated_by=self.request.user
			function_item_obj.last_updated_on=datetime.now()
			function_item_obj.save()
			if form.changed_data:
				create_function_item_history(function_item_obj.id, self.request.user.id, form.changed_data)
			return self.form_valid(form)
		return self.form_invalid(form)

	def form_valid(self, form):

		function_item_obj = form.save(commit=False)

		if self.request.is_ajax():
			return JsonResponse({'error': False})
		return redirect("function_items:list")

	def form_invalid(self, form):
		'''address_obj = self.object.address
		address_form = BillingAddressForm(
			self.request.POST, instance=address_obj)'''

		if self.request.is_ajax():
			return JsonResponse({'error': True, 'function_item_errors': form.errors})
			#return JsonResponse({'error': True, 'function_item_errors': form.errors,
			#					 'address_errors': address_form.errors})
		return self.render_to_response(
			#self.get_context_data(form=form, address_form=address_form))
			self.get_context_data(form=form))

	def get_context_data(self, **kwargs):
		context = super(UpdateFunctionItemView, self).get_context_data(**kwargs)
		context["function_item_obj"] = self.object
		context["sub_function_item_objs"] = self.object.sub_function_items.all()
		'''user_assgn_list = [
			assigned_to.id for assigned_to in context["function_item_obj"].assigned_to.all()]
		if self.request.user == context['function_item_obj'].created_by:
			user_assgn_list.append(self.request.user.id)'''
		if (self.request.user.role != "ADMIN" and not
				self.request.user.is_superuser):
			#if self.request.user.id not in user_assgn_list:
			#	raise PermissionDenied
			raise PermissionDenied

		#context["address_obj"] = self.object.address
		context["function_item_form"] = context["form"]
		context["users"] = self.users
		if "sub_function_item_form" in kwargs:
			context["sub_function_item_form"] = kwargs["sub_function_item_form"]
		else:
			if self.request.POST:
				context["sub_function_item_form"] = SubFunctionItemForm(self.request.POST)
			else:
				context["sub_function_item_form"] = SubFunctionItemForm()
		#context["types"] = FUNCTION_TYPE
		#context["status"]=FUNCTION_STATUS
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

class UpdateSubFunctionItemView(AdminAccessRequiredMixin, LoginRequiredMixin, UpdateView):
	model = SubFunctionItem
	form_class = SubFunctionItemForm

	def dispatch(self, request, *args, **kwargs):
		if self.request.user.role == 'ADMIN' or self.request.user.is_superuser:
			self.users = User.objects.filter(is_active=True).order_by('email')
		else:
			self.users = User.objects.filter(role='ADMIN').order_by('email')
		return super(UpdateSubFunctionItemView, self).dispatch(
			request, *args, **kwargs)

	def get_form_kwargs(self):
		kwargs = super(UpdateSubFunctionItemView, self).get_form_kwargs()

		return kwargs

	def post(self, request, *args, **kwargs):
		
		#sub_function_item_id = form.cleaned_data["id"]
		#self.object = get_object_or_404(SubFunctionItem, id=sub_function_item_id)
		self.object = self.get_object()
		sub_function_item_obj=self.object
		form = self.get_form()
		

		if form.is_valid():
			
			origin_status=self.object.status
			sub_function_item_obj = form.save(commit=False)
			
			if 'status' in form.changed_data and form.cleaned_data["status"]=="Approved":
				sub_function_item_obj.approved_by=self.request.user
				sub_function_item_obj.approved_on=datetime.now()
			sub_function_item_obj.status=form.cleaned_data["status"]
			sub_function_item_obj.last_updated_by=self.request.user
			sub_function_item_obj.last_updated_on=datetime.now()
			sub_function_item_obj.save()
			if form.changed_data:
				create_sub_function_item_history(sub_function_item_obj.id, self.request.user.id, form.changed_data)
			return self.form_valid(form)
		return self.form_invalid(form)

	def form_valid(self, form):
		
		sub_function_item_obj = form.save(commit=False)

		if self.request.is_ajax():
			return JsonResponse({'error': False,'id':sub_function_item_obj.id})
		return JsonResponse({'error': False,'id':sub_function_item_obj.id})

	def form_invalid(self, form):

		if self.request.is_ajax():
			return JsonResponse({'error': True, 'sub_function_item_errors': form.errors})
			#return JsonResponse({'error': True, 'function_item_errors': form.errors,
			#					 'address_errors': address_form.errors})
		return self.render_to_response(
			#self.get_context_data(form=form, address_form=address_form))
			self.get_context_data(form=form))

	def get_context_data(self, **kwargs):
		context = super(UpdateSubFunctionItemView, self).get_context_data(**kwargs)
		context["sub_function_item_obj"] = self.object

		if (self.request.user.role != "ADMIN" and not
				self.request.user.is_superuser):
			#if self.request.user.id not in user_assgn_list:
			#	raise PermissionDenied
			raise PermissionDenied

		context["sub_function_item_form"] = context["form"]
		context["users"] = self.users

		return context

class RemoveFunctionItemView(AdminAccessRequiredMixin, LoginRequiredMixin, View):

	def get(self, request, *args, **kwargs):
		return self.post(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		function_item_id = kwargs.get("pk")
		self.object = get_object_or_404(FunctionItem, id=function_item_id)
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
			return redirect("function_items:list")

class RemoveSubFunctionItemView(AdminAccessRequiredMixin, LoginRequiredMixin, View):

	def get(self, request, *args, **kwargs):
		return self.post(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		sub_function_item_id = request.POST.get('pk')
		self.object = get_object_or_404(SubFunctionItem, id=sub_function_item_id)
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