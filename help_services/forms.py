from django import forms
from .models import Answer
class ContactForm(forms.Form):
    name = forms.CharField(label='Имя', max_length=255, widget=forms.TextInput(attrs={"placeholder": "fullname", "class": "input-md input-rounded form-control", "maxlength": "100"}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={"placeholder": "email address", "class": "input-md input-rounded form-control", "maxlength": "100"}))
    content = forms.CharField(widget=forms.Textarea(attrs={"placeholder": "Message", "class": "form-control"}))

class UserQuestionForm(forms.ModelForm):
    title = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={"id": "inputHelpBlock", "class": "form-control input-circle input-lg no-border text-center mt25"}),
    )

    class Meta:
        model = Answer
        fields = ['title', 'text']