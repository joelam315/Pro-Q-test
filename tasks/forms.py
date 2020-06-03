from django import forms
from tasks.models import Task
from companies.models import Company
from contacts.models import Contact
from common.models import User, Attachments, Comment
from django.db.models import Q
from teams.models import Teams


class TaskForm(forms.ModelForm):
    teams_queryset = []
    teams = forms.MultipleChoiceField(choices=teams_queryset)

    def __init__(self, *args, **kwargs):
        # assigned_users = kwargs.pop('assigned_to', [])
        request_user = kwargs.pop('request_user', None)
        self.obj_instance = kwargs.get('instance', None)
        super(TaskForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs = {"class": "form-control"}

        if request_user.role == 'USER':
            self.fields["company"].queryset = Company.objects.filter(
                Q(assigned_to__in=[request_user]) | Q(created_by=request_user)).filter(status="open")

            self.fields["contacts"].queryset = Contact.objects.filter(
                Q(assigned_to__in=[request_user]) | Q(created_by=request_user))

        if request_user.role == 'ADMIN' or request_user.is_superuser:
            self.fields["company"].queryset = Company.objects.filter(
                status="open")

            self.fields["contacts"].queryset = Contact.objects.filter()
            self.fields["teams"].choices = [(team.get('id'), team.get(
                'name')) for team in Teams.objects.all().values('id', 'name')]

        self.fields["teams"].required = False
        self.fields['assigned_to'].required = False
        # if assigned_users:
        #     self.fields['assigned_to'].queryset = assigned_users
        # else:
        #     self.fields.get('assigned_to').queryset = User.objects.none()
        self.fields['title'].required = True
        self.fields['status'].required = True
        self.fields['priority'].required = True
        self.fields['company'].required = False
        self.fields['contacts'].required = False
        self.fields['due_date'].required = False

        # self.fields['company'].widget.attrs = {'data-id': [list(company.contacts.values_list(
        #     'id', flat=True)) for company in self.fields["company"].queryset]}

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if Task.objects.filter(title=title).exclude(id=self.instance.id).exists():
            raise forms.ValidationError(
                'Task with this Title already exists.')
        return title

    class Meta:
        model = Task
        fields = (
            'title', 'status', 'priority', 'assigned_to', 'company', 'contacts',
            'due_date'
        )


class TaskCommentForm(forms.ModelForm):
    comment = forms.CharField(max_length=255, required=True)

    class Meta:
        model = Comment
        fields = ('comment', 'task', 'commented_by')


class TaskAttachmentForm(forms.ModelForm):
    attachment = forms.FileField(max_length=1001, required=True)

    class Meta:
        model = Attachments
        fields = ('attachment', 'task')