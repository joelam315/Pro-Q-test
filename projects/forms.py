from django import forms
from projects.models import Project
from common.models import User, Comment, Attachments, Address
from django.db.models import Q
from teams.models import Teams
from companies.models import Company
from function_items.models import FunctionItem

class ProjectForm(forms.ModelForm):
    teams_queryset = []
    teams = forms.MultipleChoiceField(choices=teams_queryset)

    def __init__(self, *args, **kwargs):
        request_user = kwargs.pop('request_user', None)
        assigned_users = kwargs.pop('assigned_to', [])
        super(ProjectForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs = {"class": "form-control"}
            field.required = False

        #self.fields['function_items'].queryset=FunctionItem.objects.all()

        if request_user.role == 'ADMIN' or request_user.is_superuser:
            self.fields['assigned_to'].queryset = User.objects.filter(
                is_active=True)
            self.fields["teams"].choices = [(team.get('id'), team.get(
                'name')) for team in Teams.objects.all().values('id', 'name')]
            self.fields['companies'].queryset = Company.objects.filter(
                status='open')
        # elif request_user.google.all():
        #     self.fields['assigned_to'].queryset = User.objects.none()
        #     self.fields['companies'].queryset = Company.objects.filter(status='open').filter(
        #         Q(created_by=request_user) | Q(assigned_to=request_user))
        elif request_user.role == 'USER':
            self.fields['assigned_to'].queryset = User.objects.filter(
                role='ADMIN')
            self.fields['companies'].queryset = Company.objects.filter(status='open').filter(
                Q(created_by=request_user) | Q(assigned_to=request_user))
        else:
            pass

        self.fields["teams"].required = False
        self.fields['phone'].widget.attrs.update({
            'placeholder': '+852-91234567'})
        self.fields['project_title'].required = True
        self.fields['project_number'].required = True
        #self.fields['currency'].required = True
        self.fields['email'].required = True
        #self.fields['total_amount'].required = True
        self.fields['due_date'].required = True
        self.fields['companies'].required = False
        self.fields['function_items'].required=True

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')

        if quantity in [None, '']:
            raise forms.ValidationError('This field is required')

        return quantity

    def clean_project_number(self):
        project_number = self.cleaned_data.get('project_number')
        if Project.objects.filter(project_number=project_number).exclude(id=self.instance.id).exists():
            raise forms.ValidationError(
                'Project with this Project Number already exists.')

        return project_number

    class Meta:
        model = Project
        fields = ('project_title', 'project_number',
                  'from_address', 'to_address', 'name',
                  'email', 'phone', 'status', 'assigned_to',
                  'quantity', 'rate',
                  'details', 'due_date', 'companies','function_items','sub_function_items'
                  )


class ProjectCommentForm(forms.ModelForm):
    comment = forms.CharField(max_length=255, required=True)

    class Meta:
        model = Comment
        fields = ('comment', 'task', 'commented_by')


class ProjectAttachmentForm(forms.ModelForm):
    attachment = forms.FileField(max_length=1001, required=True)

    class Meta:
        model = Attachments
        fields = ('attachment', 'task')


class ProjectAddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ('address_line', 'street', 'city',
                  'state', 'postcode', 'country')

    def __init__(self, *args, **kwargs):
        super(ProjectAddressForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs = {"class": "form-control"}
        self.fields['address_line'].widget.attrs.update({
            'placeholder': 'Address Line'})
        self.fields['street'].widget.attrs.update({
            'placeholder': 'Street'})
        self.fields['city'].widget.attrs.update({
            'placeholder': 'City'})
        self.fields['state'].widget.attrs.update({
            'placeholder': 'State'})
        self.fields['postcode'].widget.attrs.update({
            'placeholder': 'Postcode'})
        self.fields["country"].choices = [
            ("", "--Country--"), ] + list(self.fields["country"].choices)[1:]
