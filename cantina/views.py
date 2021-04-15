from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.cache import never_cache
from django.utils.timezone import localtime, now

from .forms import CadAlu, CadEsc, EntAlu, EntEsc, ItensForm, Dinheiro
from .models import User, Aluno, Escola, Itens, Mensagem, Pedido

import decimal

#tags
from django.template.defaulttags import register
from random import choice

@register.filter
def get_range(value):
    return range(value)

@register.filter
def get_sort(lst, key_name):
    return sorted(lst, key=lambda item: getattr(item, key_name))

@register.filter
def horario(x):
    h = int(localtime(now()).strftime('%H'))
    p={'M':6, 'T':12, 'N':19}
    if p[x]<=h<=p[x]+5:
        return True
    return False

@register.filter
def periodo (x):
    return {'M':'Manhã','T':'Tarde','N':'Noite'}[x]

@register.simple_tag
def get_rand():
    return choice(range(10))
#tags

@never_cache
def entrar(request):
    if request.user.is_authenticated:
        if request.user.is_school:
            return redirect('escola')
        else:
            return redirect('aluno')

    cadalu = CadAlu()
    cadesc = CadEsc()
    entalu = EntAlu()
    entesc = EntEsc()
    if request.method == 'POST':
        if 'alu_cad_bt' in request.POST:
            cadalu = CadAlu(request.POST)
            if cadalu.is_valid():
                escola = Escola.objects.get(nome=request.POST['ca_escola'])
                periodo = request.POST['ca_periodo']
                nome = request.POST['ca_nome']
                email = request.POST['ca_email']
                senha = request.POST['ca_senha1']

                usr_aluno = User.objects.create_aluno(email=email, password=senha)
                aluno = Aluno(escola=escola, periodo=periodo, nome=nome, usuario=usr_aluno)
                aluno.save()

                user = authenticate(request, email=email, password=senha)
                if user is not None:
                    login(request, user)
                    return HttpResponseRedirect("/aluno")

        elif 'esc_cad_bt' in request.POST:
            cadesc = CadEsc(request.POST)
            if cadesc.is_valid():
                nome = request.POST['ce_nome']
                email = request.POST['ce_email']
                senha = request.POST['ce_senha1']

                usr_escola = User.objects.create_escola(
                    email=email, password=senha)
                escola = Escola(nome=nome, usuario=usr_escola)
                escola.save()

                user = authenticate(request, email=email, password=senha)
                if user is not None:
                    login(request, user)
                    return HttpResponseRedirect("/escola")

        elif 'alu_ent_bt' in request.POST:
            entalu = EntAlu(request.POST)
            if entalu.is_valid():
                email = request.POST['ea_email']
                senha = request.POST['ea_senha']

                user = authenticate(request, email=email, password=senha)
                if user is not None:
                    login(request, user)
                    return HttpResponseRedirect("/aluno")

        elif 'esc_ent_bt' in request.POST:
            entesc = EntEsc(request.POST)
            if entesc.is_valid():
                email = request.POST['ee_email']
                senha = request.POST['ee_senha']

                user = authenticate(request, email=email, password=senha)
                if user is not None:
                    login(request, user)
                    return HttpResponseRedirect("/escola")
    x = {
        'cadalu': cadalu,
        'cadesc': cadesc,
        'entalu': entalu,
        'entesc': entesc,
        'escola': Escola.objects.all(),
    }
    return render(request, 'cantina/nossa_cantina_entrar.html', x)


def sair(request):
    logout(request)
    return redirect('entrar')


@login_required(redirect_field_name='entrar')
def aluno(request):
    if request.user.is_school:
        return redirect('escola')

    valor = Dinheiro()
    if request.method == 'POST':
        if 'pedido' in request.POST:
            nomes = request.POST['nomes']
            total = request.POST['total']

            # if request.user.aluno.dinheiro < decimal.Decimal(total):
            #     return HttpResponseRedirect("/aluno")

            ped=Pedido(escola=request.user.aluno.escola, aluno=request.user.aluno, pedidos=nomes, valor=total)
            # request.user.aluno.dinheiro-=decimal.Decimal(total)

            # request.user.aluno.save()
            ped.save()
            return HttpResponseRedirect("/aluno")

        if 'foto_aluno' in request.FILES:
            if request.user.aluno.imagem != 'indice.jpeg':
                request.user.aluno.imagem.delete()
            request.user.aluno.imagem = request.FILES.get('foto_aluno')
            request.user.aluno.save()
            return HttpResponseRedirect("/aluno")

        valor = Dinheiro(request.POST)
        if valor.is_valid():
            request.user.aluno.dinheiro+=decimal.Decimal(request.POST['valor'])
            request.user.aluno.save()
            return HttpResponseRedirect("/aluno")

    x = {
        'aluno': request.user.aluno,
        'itens': Itens.objects.filter(escola=request.user.aluno.escola),
        'mensagens': Mensagem.objects.filter(escola=request.user.aluno.escola),
        'dinheiro': valor,
        'pedidos':Pedido.objects.filter(aluno=request.user.aluno),
    }
    return render(request, 'cantina/nossa_cantina_pag_aluno.html', x)


@login_required(redirect_field_name='entrar')
def escola(request):
    if not request.user.is_school:
        return redirect('aluno')

    form = ItensForm()
    if request.method == 'POST':
        if 'entregar' in request.POST:
            it = Pedido.objects.get(id=request.POST['id'])
            it.entregue = True
            it.save()
            return HttpResponseRedirect("/escola")

        if 'desentregar' in request.POST:
            it = Pedido.objects.get(id=request.POST['id'])
            it.entregue = False
            it.save()
            return HttpResponseRedirect("/escola")

        if 'del' in request.POST:
            Itens.objects.get(id=request.POST['del']).imagem.delete()
            Itens.objects.get(id=request.POST['del']).delete()
            return HttpResponseRedirect("/escola")

        if 'men' in request.POST:
            escola = request.user.escola
            texto = request.POST['texto']
            if texto == "":
                return HttpResponseRedirect("/escola")
            men = Mensagem(escola=escola, texto=texto)
            men.save()
            return HttpResponseRedirect("/escola")

        if 'ex_me' in request.POST:
            Mensagem.objects.get(id=request.POST['ex_me']).delete()
            return HttpResponseRedirect("/escola")
        
        if 'foto_escola' in request.FILES:
            if request.user.escola.imagem != 'indice.jpeg':
                request.user.escola.imagem.delete()
            request.user.escola.imagem = request.FILES.get('foto_escola')
            request.user.escola.save()
            return HttpResponseRedirect("/escola")

        form = ItensForm(request.POST)
        if 'mod' in request.POST:
            if form.is_valid:
                z = Itens.objects.get(id=request.POST['mod'])
                z.nome = request.POST['nome']
                z.preco = request.POST['preco']
                imagem = request.FILES.get('imagem')
                if imagem:
                    z.imagem.delete()
                    z.imagem = imagem
                z.save()
                return HttpResponseRedirect("/escola")

        if 'add' in request.POST:
            if form.is_valid:
                nome = request.POST['nome']
                preco = request.POST['preco']
                imagem = request.FILES.get('imagem')
                escola = request.user.escola

                item = Itens(escola=escola, nome=nome, preco=preco)
                if imagem:
                    item.imagem = imagem
                item.save()
                return HttpResponseRedirect("/escola")
    x = {
        'escola': request.user.escola,
        'itens': Itens.objects.filter(escola=request.user.escola),
        'itens_form': form,
        'mensagens': Mensagem.objects.filter(escola=request.user.escola),
        'pedidos':Pedido.objects.filter(escola=request.user.escola),
    }
    return render(request, 'cantina/nossa_cantina_pag_escola.html', x)

def introducao(request):
    return render(request, 'cantina/nossa_cantina_introducao.html')