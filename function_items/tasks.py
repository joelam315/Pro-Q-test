from celery.task import task
from django.conf import settings
from django.shortcuts import reverse
from django.template.loader import render_to_string

from common.models import User
from function_items.models import FunctionItem, FunctionItemHistory, SubFunctionItem, SubFunctionItemHistory

@task
def create_function_item_history(original_function_item_id, updated_by_user_id, changed_fields):
    """original_function_item_id, updated_by_user_id, changed_fields"""
    original_function_item = FunctionItem.objects.filter(id=original_function_item_id).first()

    updated_by_user = User.objects.get(id=updated_by_user_id)
    changed_data = [(' '.join(field.split('_')).title()) for field in changed_fields]
    if len(changed_data) > 1:
        changed_data = ', '.join(changed_data[:-1]) + ' and ' + changed_data[-1] + ' have changed.'
    elif len(changed_data) == 1:
        changed_data = ', '.join(changed_data) + ' has changed.'
    else:
        changed_data = None

    if original_function_item.function_item_history.count() == 0:
        changed_data = 'Function Item Created.'
    if original_function_item:
        function_item_history = FunctionItemHistory()
        function_item_history.function_item = original_function_item
        function_item_history.name = original_function_item.name
        function_item_history.price = original_function_item.price
        function_item_history.description = original_function_item.description
        function_item_history.type = original_function_item.type
        function_item_history.status = original_function_item.status
        function_item_history.changed_data=changed_data
        function_item_history.updated_by = updated_by_user

        function_item_history.save()

@task
def create_sub_function_item_history(original_sub_function_item_id, updated_by_user_id, changed_fields):
    """original_sub_function_item_id, updated_by_user_id, changed_fields"""
    original_sub_function_item = SubFunctionItem.objects.filter(id=original_sub_function_item_id).first()

    updated_by_user = User.objects.get(id=updated_by_user_id)
    changed_data = [(' '.join(field.split('_')).title()) for field in changed_fields]
    if len(changed_data) > 1:
        changed_data = ', '.join(changed_data[:-1]) + ' and ' + changed_data[-1] + ' have changed.'
    elif len(changed_data) == 1:
        changed_data = ', '.join(changed_data) + ' has changed.'
    else:
        changed_data = None

    if original_sub_function_item.sub_function_item_history.count() == 0:
        changed_data = 'Sub Function Item Created.'
    if original_sub_function_item:
        sub_function_item_history = SubFunctionItemHistory()
        sub_function_item_history.sub_function_item = original_sub_function_item
        sub_function_item_history.name = original_sub_function_item.name
        sub_function_item_history.price = original_sub_function_item.price
        sub_function_item_history.description = original_sub_function_item.description
        sub_function_item_history.status = original_sub_function_item.status
        sub_function_item_history.changed_data=changed_data
        sub_function_item_history.updated_by = updated_by_user

        sub_function_item_history.save()
