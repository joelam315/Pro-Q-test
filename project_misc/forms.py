from django import forms
from project_misc.models import Misc


class MiscForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(MiscForm, self).__init__(*args, **kwargs)
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
        model = Misc
        fields = (
            'name',
            'suggested_unit_price',
            'is_active'
        )
