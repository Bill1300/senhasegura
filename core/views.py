from django.shortcuts import render, redirect
from .models import Senha
from django.http import HttpResponse

def home(request):
    senha = Senha.objects.all()
    return render(request, 'index.html', {'senhas': senha})

def save(request):
    titulo = request.POST.get('titulo').capitalize()
    descricao = request.POST.get('descricao')
    usuario = request.POST.get('usuario')
    senha = request.POST.get('senha')

    if not titulo or not senha:
        return HttpResponse('Título e senha são obrigatórios.')

    Senha.objects.create(titulo=titulo, descricao=descricao, usuario=usuario, senha=senha)
    senha = Senha.objects.all()
    return render(request, 'index.html', {'senhas': senha})

def edit(request, id):
    senha = Senha.objects.get(id=id)
    return render(request, 'update.html', {'senhas': senha})

def update(request, id):
    titulo = request.POST.get('titulo').capitalize()
    descricao = request.POST.get('descricao')
    usuario = request.POST.get('usuario')
    vsenha = request.POST.get('senha')

    senha = Senha.objects.get(id=id)
    senha.titulo = titulo   
    senha.descricao = descricao
    senha.usuario = usuario
    senha.senha = vsenha
    senha.save()
    return redirect(home)

def delete(request, id):
    senha = Senha.objects.get(id=id)
    senha.delete()
    return redirect(home)

def docs(request):
    return render(request, 'docs.html')

def structure(request):
    return render(request, 'structure.html')