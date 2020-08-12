from celery.task import task
from django.conf import settings
from django.shortcuts import reverse
from django.template.loader import render_to_string

from common.models import User
#from project_items.models import ProjectItem, ProjectItemHistory, SubProjectItem, SubProjectItemHistory

'''@task
def create_project_item_history(original_project_item_id, updated_by_user_id, changed_fields):
    """original_project_item_id, updated_by_user_id, changed_fields"""
    original_project_item = ProjectItem.objects.filter(id=original_project_item_id).first()

    updated_by_user = User.objects.get(id=updated_by_user_id)
    changed_data = [(' '.join(field.split('_')).title()) for field in changed_fields]
    if len(changed_data) > 1:
        changed_data = ', '.join(changed_data[:-1]) + ' and ' + changed_data[-1] + ' have changed.'
    elif len(changed_data) == 1:
        changed_data = ', '.join(changed_data) + ' has changed.'
    else:
        changed_data = None

    if original_project_item.project_item_history.count() == 0:
        changed_data = 'Function Item Created.'
    if original_project_item:
        project_item_history = ProjectItemHistory()
        project_item_history.project_item = original_project_item
        project_item_history.name = original_project_item.name
        project_item_history.price = original_project_item.price
        project_item_history.description = original_project_item.description
        project_item_history.type = original_project_item.type
        project_item_history.status = original_project_item.status
        project_item_history.changed_data=changed_data
        project_item_history.updated_by = updated_by_user

        project_item_history.save()

@task
def create_sub_project_item_history(original_sub_project_item_id, updated_by_user_id, changed_fields):
    """original_sub_project_item_id, updated_by_user_id, changed_fields"""
    original_sub_project_item = SubProjectItem.objects.filter(id=original_sub_project_item_id).first()

    updated_by_user = User.objects.get(id=updated_by_user_id)
    changed_data = [(' '.join(field.split('_')).title()) for field in changed_fields]
    if len(changed_data) > 1:
        changed_data = ', '.join(changed_data[:-1]) + ' and ' + changed_data[-1] + ' have changed.'
    elif len(changed_data) == 1:
        changed_data = ', '.join(changed_data) + ' has changed.'
    else:
        changed_data = None

    if original_sub_project_item.sub_project_item_history.count() == 0:
        changed_data = 'Sub Function Item Created.'
    if original_sub_project_item:
        sub_project_item_history = SubProjectItemHistory()
        sub_project_item_history.sub_project_item = original_sub_project_item
        sub_project_item_history.name = original_sub_project_item.name
        sub_project_item_history.price = original_sub_project_item.price
        sub_project_item_history.description = original_sub_project_item.description
        sub_project_item_history.status = original_sub_project_item.status
        sub_project_item_history.changed_data=changed_data
        sub_project_item_history.updated_by = updated_by_user

        sub_project_item_history.save()
'''