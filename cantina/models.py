from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from .manager import UserManager

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    is_school = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    username = None

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

class Escola(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=50, null=False, unique=True)
    imagem = models.ImageField(upload_to='imagens_escola', default='indice.jpeg')

    def __str__(self):
        return self.nome

class Aluno(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    escola = models.ForeignKey(Escola, on_delete=models.CASCADE)
    nome = models.CharField(max_length=50, null=False)
    dinheiro = models.DecimalField(default=00.00 ,max_digits=5, decimal_places=2, null=False)
    imagem = models.ImageField(upload_to='imagens_aluno', default='indice.jpeg')
    periodo = models.CharField(max_length=10, null=False)

    def __str__(self):
        return (self.escola, self.nome)

class Itens(models.Model):
    escola = models.ForeignKey(Escola, on_delete=models.CASCADE)
    nome = models.CharField(max_length=20)
    preco = models.DecimalField(max_digits=4, decimal_places=2)
    imagem = models.ImageField(upload_to='itens_da_cantina', default='indice.jpeg')

class Mensagem(models.Model):
    escola = models.ForeignKey(Escola, on_delete=models.CASCADE)
    texto = models.CharField(max_length=255)

    def __str__(self):
        return (self.escola)

class Pedido(models.Model):
    escola = models.ForeignKey(Escola, on_delete=models.CASCADE)
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    pedidos = models.CharField(max_length=255)
    data = models.DateField(auto_now=False, auto_now_add=True)
    entregue = models.BooleanField(default=False)
    valor = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return (self.pedidos)