from .models import Exercicio
from bootstrap_modal_forms.forms import BSModalModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class ExercicioModelForm(BSModalModelForm):
    class Meta:
        model = Exercicio
        fields = ['titulo', 'descricao', 'img']

class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True, label='First name', help_text='Max 30 characters') 
    last_name = forms.CharField(max_length=30, required=True, label='Last name', help_text='Max 30 characters')

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password1","password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name= self.cleaned_data['first_name']
        user.last_name= self.cleaned_data['last_name']
        if commit:
            user.save()
        return user

