from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(label='message title')
    email = forms.EmailField(label='your email')
    message = forms.CharField(label='message')

