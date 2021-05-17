from django import forms
from .models import Company, Email,ChargingStages
from common.models import Comment, Attachments, User
#from leads.models import Lead
from contacts.models import Contact
from django.db.models import Q
from teams.models import Teams


class CompanyForm(forms.ModelForm):
    #teams_queryset = []
    #teams = forms.MultipleChoiceField(choices=teams_queryset)
    
    def __init__(self, *args, **kwargs):
        company_view = kwargs.pop('company', False)
        request_user = kwargs.pop('request_user', None)
        super(CompanyForm, self).__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs = {"class": "form-control"}
        for key, value in self.fields.items():
            if key == 'phone':
                value.widget.attrs['placeholder'] = "+91-123-456-7890"
            else:
                value.widget.attrs['placeholder'] = value.label

        self.fields['br_approved'].widget.attrs['style']="width:auto;"

        self.fields['is_active'].widget.attrs['style']="width:auto;"
        
        self.fields["owner"].choices = [(user.get('id'), user.get('username')) for user in User.objects.filter(role="USER",is_superuser=False).values('id', 'username')]
        # lead is not mandatory while editing
        '''if self.instance.id:
            self.fields['lead'].required = False
        self.fields['lead'].required = False'''

    class Meta:
        model = Company
        fields = ('name','owner',"br_approved","logo_pic","br_pic","is_active")


class CompanyCommentForm(forms.ModelForm):
    comment = forms.CharField(max_length=255, required=True)

    class Meta:
        model = Comment
        fields = ('comment', 'company', 'commented_by')


class CompanyAttachmentForm(forms.ModelForm):
    attachment = forms.FileField(max_length=1001, required=True)

    class Meta:
        model = Attachments
        fields = ('attachment', 'company')


class EmailForm(forms.ModelForm):
    recipients = forms.CharField()
    # message_subject = forms.CharField(max_length=500)
    # message_body = forms.CharField(widget=forms.Textarea)
    # timezone = forms.CharField(max_length=200)
    # scheduled_date_time = forms.DateTimeField()
    # scheduled_later = forms.CharField(max_length=20)

    def __init__(self, *args, **kwargs):
        self.company_obj = kwargs.pop('company', False)
        super(EmailForm, self).__init__(*args, **kwargs)
        # self.fields['message_subject'].widget.attrs['class'] = 'form-control'
        # self.fields['message_subject'].widget.attrs['required'] = True
        # self.fields['message_subject'].widget.attrs['placeholder'] = 'Email Subject'

        # self.fields['recipient'].required = False
        self.fields['from_email'].required = True
        self.fields['message_subject'].required = True
        self.fields['message_body'].required = True

        self.fields['scheduled_date_time'].required = False
        self.fields['scheduled_later'].required = False
        self.fields['recipients'].required = True
        #self.fields['recipients'].query = self.company_obj.contacts.all()
        # self.fields['recipients'].choices = list((contact.get('id'), contact.get('email'))
        #     for contact in self.company_obj.contacts.values('id', 'email'))

    class Meta:
        model = Email
        fields = ['recipients', 'message_subject', 'from_email',
            'message_body', 'timezone', 'scheduled_date_time', 'scheduled_later']

    # def clean_recipients(self):
    #     recipients = self.cleaned_data.get('recipients')
    #     recipients = recipients.split(',')
    #     if len(recipients) == 0:
    #         raise forms.ValidationError('This field is required.')
    #     contacts = list(self.company_obj.contacts.values_list('id', flat=True))
    #     for recipient in recipients:
    #         if int(recipient) not in contacts:
    #             raise forms.ValidationError('{} is not a valid choice.'.format(recipient))
    #     return recipients

    def clean_scheduled_date_time(self):
        scheduled_date_time = self.cleaned_data.get('scheduled_date_time')
        if self.data.get('scheduled_later') not in ['', None, False, 'false']:
            if scheduled_date_time in ['', None]:
                raise forms.ValidationError('This Field is required.')

        if self.data.get('scheduled_later') == 'true':
            if scheduled_date_time in ['', None]:
                raise forms.ValidationError('This Field is required.')

        return scheduled_date_time


    def clean_message_body(self):
        message_body = self.cleaned_data.get('message_body')
        count = 0
        for i in message_body:
            if i == "{":
                count += 1
            elif i == "}":
                count -= 1
            if count < 0:
                raise forms.ValidationError('Brackets do not match, Enter valid tags.')
        if count != 0:
            raise forms.ValidationError('Brackets do not match, Enter valid tags.')
        return message_body

from django import forms



class ChargingStagesForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['descriptions'].delimiter = '|'  # Or whichever other character you want.

    class Meta:
        model = ChargingStages
        fields = '__all__'
