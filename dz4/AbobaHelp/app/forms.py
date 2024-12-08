import app.models
from django import forms

from django.contrib.auth.models import User
from app.models import Profile

from django.db import DatabaseError, transaction


WIDGET_CLASSES = "form-control mt-2"

class LoginForm(forms.Form):
    template_name = "my_form_template.html"

    login = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    
    # set css classes
    login.widget.attrs.update({'class': WIDGET_CLASSES})
    password.widget.attrs.update({'class': WIDGET_CLASSES})
    
    def clean_login(self) -> str:
        login = self.cleaned_data["login"].strip()

        if not login.isalnum():
            raise forms.ValidationError("Login must be alphanumeric")

        return self.cleaned_data["login"].strip()
    
    def clean_password(self) -> str:
        return self.cleaned_data["password"].strip()
    

class SignupForm(forms.Form):
    template_name = "my_form_template.html"

    login = forms.CharField(min_length=3, max_length=16)
    email = forms.EmailField(required=False)
    nickname = forms.CharField(min_length=3, max_length=16)
    password = forms.CharField(min_length=6, widget=forms.PasswordInput)
    repeat_password = forms.CharField(min_length=6, widget=forms.PasswordInput)
    avatar = forms.ImageField(required=False)

    # set css classes
    login.widget.attrs.update({'class': WIDGET_CLASSES})
    email.widget.attrs.update({'class': WIDGET_CLASSES})
    nickname.widget.attrs.update({'class': WIDGET_CLASSES})
    password.widget.attrs.update({'class': WIDGET_CLASSES})
    repeat_password.widget.attrs.update({'class': WIDGET_CLASSES})
    avatar.widget.attrs.update({'class': WIDGET_CLASSES})

    def clean_email(self) -> str:
        return self.cleaned_data["email"].strip()

    def clean_login(self) -> str:
        login = self.cleaned_data["login"].strip()
        if not login.isalnum():
            raise forms.ValidationError("Login must be alphanumeric")
        if (User.objects.filter(username=login).exists()):
            raise forms.ValidationError("Login already used")
        return self.cleaned_data["login"].strip()
    
    def clean_password(self) -> str:
        return self.cleaned_data["password"].strip()
    
    def clean_repeat_password(self) -> str:
        return self.cleaned_data["repeat_password"].strip()
    
    def clean(self):
        cleaned_data = super().clean()
        print(cleaned_data)
        if cleaned_data["password"] != cleaned_data["repeat_password"]:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data
    
    def save(self) -> User|None:
        try:
            with transaction.atomic():
                user = User.objects.create_user(
                    username=self.cleaned_data["login"],
                    email=self.cleaned_data["email"],
                    password=self.cleaned_data["password"]
                )
                profile = Profile.objects.create(user=user, nickname=self.cleaned_data["nickname"], avatar=self.cleaned_data["avatar"])
                user.save()
                profile.save()
                return user
        except DatabaseError:
            return None
        

class UserSettingsForm(forms.Form):
    template_name = "my_form_template.html"
    
    login = forms.CharField(label="Login reminder", disabled=True)
    email = forms.EmailField(required=False)
    nickname = forms.CharField(min_length=3, max_length=16)
    password = forms.CharField(help_text="Leave blank if you don't want to change the password", min_length=6, widget=forms.PasswordInput, required=False)
    repeat_password = forms.CharField(min_length=6, widget=forms.PasswordInput, required=False)
    avatar = forms.ImageField(required=False)
    
    # set css classes
    login.widget.attrs.update({'class': WIDGET_CLASSES, "autocomplete": ""})
    email.widget.attrs.update({'class': WIDGET_CLASSES, "autocomplete": ""})
    nickname.widget.attrs.update({'class': WIDGET_CLASSES, "autocomplete": ""})
    password.widget.attrs.update({'class': WIDGET_CLASSES, "autocomplete": ""})
    repeat_password.widget.attrs.update({'class': WIDGET_CLASSES, "autocomplete": ""})
    avatar.widget.attrs.update({'class': WIDGET_CLASSES, "autocomplete": ""})

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.fields["login"].initial = user.username
        self.fields["email"].initial = user.email
        self.fields["nickname"].initial = user.profile.nickname
        self.fields["avatar"].initial = user.profile.avatar


    def clean_email(self) -> str:
        return self.cleaned_data["email"].strip()
    
    def clean_nickname(self) -> str:
        return self.cleaned_data["nickname"].strip()

    def clean_password(self) -> str:
        return self.cleaned_data["password"].strip()
    
    def clean_repeat_password(self) -> str:
        return self.cleaned_data["repeat_password"].strip()
    
    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data["password"] != cleaned_data["repeat_password"]:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data
    
    def save(self):
        try:
            with transaction.atomic():
                self.user.email = self.cleaned_data["email"]
                if (self.cleaned_data["password"] != ""):
                    self.user.set_password(self.cleaned_data["password"])
                self.user.save()
                profile = self.user.profile
                profile.nickname = self.cleaned_data["nickname"]
                if (self.cleaned_data["avatar"] != ""):
                    profile.avatar = self.cleaned_data["avatar"]
                profile.save()
            return True
        except DatabaseError:
            return False
        

class AskQuestionForm(forms.ModelForm):
    template_name = "my_form_template.html"

    class Meta:
        model = app.models.Question
        fields = ["title", "text", "tags"]
        widgets = {
            "title": forms.TextInput(attrs={"class": WIDGET_CLASSES}),
            "text": forms.Textarea(attrs={"class": WIDGET_CLASSES}),
            "tags": forms.SelectMultiple(attrs={"class": WIDGET_CLASSES})
        }


class AnswerQuestionForm(forms.ModelForm):
    template_name = "my_form_template.html"

    class Meta:
        model = app.models.Answer
        fields = ["text"]
        widgets = {
            "text": forms.Textarea(attrs={"class": WIDGET_CLASSES})
        }