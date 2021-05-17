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
            'item_type_materials',
            'is_active'
        )

class ItemTypeMaterialForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ItemTypeMaterialForm,self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs={"class": "form-control"}
        
        self.fields['is_active'].widget.attrs['style']="width:auto;"

        for key, value in self.fields.items():
            value.widget.attrs['placeholder'] = value.label

    def clean_name(self):
        return self.cleaned_data.get("name","").strip()

    class Meta:
        model=ItemTypeMaterial
        fields=(
            'name',
            'item_type',
            'value_based_price',
            'is_active'
        )

class ItemForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ItemForm,self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs={"class": "form-control"}
        
        self.fields['is_active'].widget.attrs['style']="width:auto;"

        for key, value in self.fields.items():
            value.widget.attrs['placeholder'] = value.label

        self.fields['item_properties_sort'].required=False

    class Meta:
        model=Item
        fields=(
            'name',
            'item_properties',
            'item_properties_sort',
            'item_type',
            'value_based_price',
            'is_active',
            'item_formulas',
            'index'
        )

class ItemPropertyForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ItemPropertyForm,self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs={"class": "form-control"}

        for key, value in self.fields.items():
            value.widget.attrs['placeholder'] = value.label

    class Meta:
        model=ItemProperty
        fields=(
            'name',
            'symbol'
        )

class ItemFormulaForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ItemFormulaForm,self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs={"class": "form-control"}
        
        self.fields['is_active'].widget.attrs['style']="width:auto;"

        for key, value in self.fields.items():
            value.widget.attrs['placeholder'] = value.label

    class Meta:
        model=ItemFormula
        fields=(
            'name',
            'item',
            'formula',
            'is_active'
        )