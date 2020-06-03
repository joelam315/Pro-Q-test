from django import forms
from customers.models import Customer
from common.models import Comment, Attachments
from teams.models import Teams


class CustomerForm(forms.ModelForm):
    teams_queryset = []
    teams = forms.MultipleChoiceField(choices=teams_queryset)

    def __init__(self, *args, **kwargs):
        assigned_users = kwargs.pop('assigned_to', [])
        super(CustomerForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs = {"class": "form-control"}
        self.fields['description'].widget.attrs.update({
            'rows': '6'})
        if assigned_users:
            self.fields['assigned_to'].queryset = assigned_users
        self.fields['assigned_to'].required = False

        for key, value in self.fields.items():
            if key == 'phone':
                value.widget.attrs['placeholder'] = "+852-91234567"
            else:
                value.widget.attrs['placeholder'] = value.label
        self.fields["teams"].choices = [(team.get('id'), team.get('name')) for team in Teams.objects.all().values('id', 'name')]
        self.fields["teams"].required = False

    class Meta:
        model = Customer
        fields = (
            'assigned_to', 'first_name',
            'last_name', 'email',
            'phone', 'address', 'description','profile_pic'
        )


class CustomerCommentForm(forms.ModelForm):
    comment = forms.CharField(max_length=255, required=True)

    class Meta:
        model = Comment
        fields = ('comment', 'customer', 'commented_by')


class CustomerAttachmentForm(forms.ModelForm):
    attachment = forms.FileField(max_length=1001, required=True)

    class Meta:
        model = Attachments
        fields = ('attachment', 'customer')
