from django import forms
from project_items.models import (
    ItemType,ItemProperty,ItemTypeMaterial,Item,ItemFormula
)


class ItemTypeForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ItemTypeForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs = {"class": "form-control"}

        self.fields['is_active'].widget.attrs['style']="width:auto;"
        '''self.fields['description'].widget.attrs.update({
            'rows': '6'})
        self.fields["type"].choices = [
            ("", "--Type--"), ] + list(self.fields["type"].choices)[0:]'''

        for key, value in self.fields.items():
        #    if key == 'phone':
        #        value.widget.attrs['placeholder'] = "+852-91234567"
        #    else:
                value.widget.attrs['placeholder'] = value.label


    class Meta:
        model = ItemType
        fields = (
            'name',
            'is_active'
        )


