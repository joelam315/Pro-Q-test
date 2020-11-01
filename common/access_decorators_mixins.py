import logging
from functools import wraps

from django.contrib.auth.mixins import AccessMixin, LoginRequiredMixin
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.shortcuts import redirect

from rest_framework_simplejwt.state import token_backend
from rest_framework_simplejwt.exceptions import TokenBackendError
from common.models import User



def sales_access_required(function):
    """ this function is a decorator used to authorize if a user has sales access """
    def wrap(request, *args, **kwargs):
        if request.user.role == 'ADMIN' or request.user.is_superuser or request.user.has_sales_access:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    return wrap


def marketing_access_required(function):
    """ this function is a decorator used to authorize if a user has marketing access """
    def wrap(request, *args, **kwargs):
        if request.user.role == 'ADMIN' or request.user.is_superuser or request.user.has_marketing_access:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    return wrap


class SalesAccessRequiredMixin(AccessMixin):
    """ Mixin used to authorize if a user has sales access  """

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        self.raise_exception = True
        if request.user.role == 'ADMIN' or request.user.is_superuser or request.user.has_sales_access:
            return super(SalesAccessRequiredMixin, self).dispatch(request, *args, **kwargs)
        else:
            return self.handle_no_permission()


class MarketingAccessRequiredMixin(AccessMixin):
    """ Mixin used to authorize if a user has marketing access  """

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        self.raise_exception = True
        if request.user.role == 'ADMIN' or request.user.is_superuser or request.user.has_marketing_access:
            return super(MarketingAccessRequiredMixin, self).dispatch(request, *args, **kwargs)
        else:
            return self.handle_no_permission()


def admin_login_required(function):
    """ this function is a decorator used to authorize if a user is admin """
    def wrap(request, *args, **kwargs):
        if request.user.role == 'ADMIN' or request.user.is_superuser:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    return wrap

class AdminAccessRequiredMixin(AccessMixin):
    """ Mixin used to authorize if a user has admin access  """

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        self.raise_exception = True
        if request.user.role == 'ADMIN' or request.user.is_superuser:
            return super(AdminAccessRequiredMixin, self).dispatch(request, *args, **kwargs)
        else:
            return self.handle_no_permission()

def app_login_required(function):
    def wrap(request, *args, **kwargs):
        try:
            token=request.META['HTTP_AUTHORIZATION'].split("Bearer")[1].strip()
        except KeyError:
            raise PermissionDenied
        except AttributeError:
            raise AttributeError
        try:
            user_id=token_backend.decode(token,verify=True)["user_id"]
        except TokenBackendError:
            raise PermissionDenied
        try:
            user=User.objects.get(pk=user_id)
        except ObjectDoesNotExist:
            raise PermissionDenied
        request.user=user
        return function(request, *args, **kwargs)
    return wrap