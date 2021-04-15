from django.urls import path
from . import views
from .forms import RefazerSenha
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',views.introducao, name='introducao'),
    path('entrar',views.entrar, name='entrar'),
    path('sair',views.sair, name='sair'),
    path('aluno',views.aluno, name='aluno'),
    path('escola',views.escola, name='escola'),

    path('refazer_senha', auth_views.PasswordResetView.as_view(form_class=RefazerSenha), name='password_reset'),
    path('refazer_senha/enviado', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('refazer_senha/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('refazer_senha/feito/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]