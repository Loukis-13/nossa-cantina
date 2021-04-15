from django import forms
from .models import User, Aluno, Escola, Itens
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core import validators

class CadAlu(forms.Form):
    CHOICES = (
        ('M', 'Manhã'),
        ('T', 'Tarde'),
        ('N', 'Noite'),
    )
    ca_escola = forms.CharField(label='Escola', label_suffix="", max_length=100)
    ca_periodo = forms.ChoiceField(choices=CHOICES, label='Periodo')
    ca_nome = forms.CharField(label='Nome', label_suffix="", max_length=100)
    ca_email = forms.EmailField(label='E-mail', label_suffix="", max_length=100)    
    ca_senha1 = forms.CharField(label='Senha', label_suffix="", max_length=32, widget=forms.PasswordInput)
    ca_senha2 = forms.CharField(label='Confirme a senha', label_suffix="", max_length=32, widget=forms.PasswordInput)#, validators=[validate_password])

    def clean_ca_escola(self):
        escola = self.cleaned_data['ca_escola']
        if not Escola.objects.filter(nome=escola).exists():
            raise ValidationError("Escola não cadastrada")
        return escola

    def clean_ca_email(self):
        email = self.cleaned_data['ca_email']
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email já cadastrado")
        return email

    def clean_ca_senha2(self):
        senha1 = self.cleaned_data['ca_senha1']
        senha2 = self.cleaned_data['ca_senha2']
        if senha1 != senha2:
            raise ValidationError("Senhas não combinam")
        return senha2

class CadEsc(forms.Form):
    ce_nome = forms.CharField(label='Nome', label_suffix="", max_length=100)
    ce_email = forms.EmailField(label='E-mail', label_suffix="", max_length=100)    
    ce_senha1 = forms.CharField(label='Senha', label_suffix="", max_length=32, widget=forms.PasswordInput)
    ce_senha2 = forms.CharField(label='Confirme a senha', label_suffix="", max_length=32, widget=forms.PasswordInput)#, validators=[validate_password])

    def clean_ce_nome(self):
        nome = self.cleaned_data['ce_nome']
        if Escola.objects.filter(nome=nome).exists():
            raise ValidationError("Escola já cadastrada")
        return nome

    def clean_ce_email(self):
        email = self.cleaned_data['ce_email']
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email já cadastrado")
        return email

    def clean_ce_senha2(self):
        senha1 = self.cleaned_data['ce_senha1']
        senha2 = self.cleaned_data['ce_senha2']
        if senha1 != senha2:
            raise ValidationError("Senhas não combinam")
        return senha2

class EntAlu(forms.Form):
    ea_email = forms.EmailField(label='E-mail', label_suffix="", max_length=100)    
    ea_senha = forms.CharField(label='Senha', label_suffix="", max_length=32, widget=forms.PasswordInput)

    def clean(self):
        email = self.cleaned_data.get('ea_email')
        senha = self.cleaned_data['ea_senha']
        if authenticate(email=email, password=senha):
            if User.objects.get(email=email).is_school == False:
                return True
        raise ValidationError("Nome ou senha incorretos")

class EntEsc(forms.Form):
    ee_email = forms.EmailField(label='E-mail', label_suffix="", max_length=100)   
    ee_senha = forms.CharField(label='Senha', label_suffix="", max_length=32, widget=forms.PasswordInput)

    def clean(self):
        email = self.cleaned_data.get('ee_email')
        senha = self.cleaned_data['ee_senha']
        if authenticate(email=email, password=senha):
            if User.objects.get(email=email).is_school == True:
                return True
        raise ValidationError("Nome ou senha incorretos")

class ItensForm(forms.Form):
    imagem = forms.ImageField(required=False, initial='indice.jpeg')
    nome = forms.CharField(max_length=20)
    preco = forms.DecimalField(min_value=0, max_value=99, decimal_places=2)

class Dinheiro(forms.Form):
    valor = forms.DecimalField(min_value=0.01, max_value=100, decimal_places=2)

from django.contrib.auth.forms import PasswordResetForm
class RefazerSenha(PasswordResetForm):
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            return email
        raise ValidationError("E-mail incorreto")