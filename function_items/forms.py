from django import forms
from function_items.models import FunctionItem, SubFunctionItem


class FunctionItemForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(FunctionItemForm, self).__init__(*args, **kwargs)
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
        model = FunctionItem
        fields = (
            'name',
            'type', 
            'price',
            'description',
            'status'
        )

class SubFunctionItemForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(SubFunctionItemForm, self).__init__(*args, **kwargs)
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
        model = SubFunctionItem
        fields = (
            'name',
            'price',
            'description',
            'status',
            'related_function_item',

        )

class UpdateSubFunctionItemForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(UpdateSubFunctionItemForm, self).__init__(*args, **kwargs)
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
        model = SubFunctionItem
        fields = (
            'name',
            'price',
            'description',
            'status',

        )

