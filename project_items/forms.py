from django import forms
from project_items.models import ProjectItem, SubProjectItem


class ProjectItemForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ProjectItemForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs = {"class": "form-control"}
        self.fields['description'].widget.attrs.update({
            'rows': '6'})
        self.fields["type"].choices = [
            ("", "--Type--"), ] + list(self.fields["type"].choices)[0:]

        for key, value in self.fields.items():
        #    if key == 'phone':
        #        value.widget.attrs['placeholder'] = "+852-91234567"
        #    else:
                value.widget.attrs['placeholder'] = value.label


    class Meta:
        model = ProjectItem
        fields = (
            'name',
            'type', 
            'price',
            'description',
            'status'
        )

class SubProjectItemForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(SubProjectItemForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs = {"class": "form-control"}
        self.fields['description'].widget.attrs.update({
            'rows': '6'})

        for key, value in self.fields.items():
        #    if key == 'phone':
        #        value.widget.attrs['placeholder'] = "+852-91234567"
        #    else:
                value.widget.attrs['placeholder'] = value.label


    class Meta:
        model = SubProjectItem
        fields = (
            'name',
            'price',
            'description',
            'status',
            'related_project_item',

        )

class UpdateSubProjectItemForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(UpdateSubProjectItemForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs = {"class": "form-control"}
        self.fields['description'].widget.attrs.update({
            'rows': '6'})

        for key, value in self.fields.items():
        #    if key == 'phone':
        #        value.widget.attrs['placeholder'] = "+852-91234567"
        #    else:
                value.widget.attrs['placeholder'] = value.label


    class Meta:
        model = SubProjectItem
        fields = (
            'name',
            'price',
            'description',
            'status',

        )

