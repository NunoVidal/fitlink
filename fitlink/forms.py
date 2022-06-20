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

    class Meta:
        model = User
        fields = ("username", "email", "password1","password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

