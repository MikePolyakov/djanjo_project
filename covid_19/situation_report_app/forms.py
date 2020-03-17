from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(label='message title')
    email = forms.EmailField(label='your email')
    message = forms.CharField(label='message')


class PostForm(forms.Form):
    name = forms.CharField(label='post title')
    text = forms.CharField(label='write your post')
    image = forms.ImageField(label='add photo')


class NewsForm(forms.Form):
    name = forms.CharField(label='article name')
    url = forms.CharField(label='web address')
    date = forms.CharField(label='YYYY-MM-DD format')
    source = forms.CharField(label='source name')
