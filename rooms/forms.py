from django import forms
from rooms.models import (
    RoomType,RoomProperty,RoomTypeFormula
)


class RoomTypeForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(RoomTypeForm, self).__init__(*args, **kwargs)
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
        model = RoomType
        fields = (
            'name',
            'related_items',
            'room_properties',
            'room_type_formulas',
            'is_active'
        )



class RoomPropertyForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(RoomPropertyForm,self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs={"class": "form-control"}

        for key, value in self.fields.items():
            value.widget.attrs['placeholder'] = value.label

    class Meta:
        model=RoomProperty
        fields=(
            'name',
            'symbol',
            'data_type',
            'custom_properties',
            'custom_property_formulas'
        )

class RoomTypeFormulaForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(RoomTypeFormulaForm,self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs={"class": "form-control"}
        
        self.fields['is_active'].widget.attrs['style']="width:auto;"

        for key, value in self.fields.items():
            value.widget.attrs['placeholder'] = value.label

    class Meta:
        model=RoomTypeFormula
        fields=(
            'name',
            'room_type',
            'formula',
            'is_active'
        )