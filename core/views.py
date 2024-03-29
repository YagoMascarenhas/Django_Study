from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from core.models import Evento
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from datetime import datetime, timedelta
from django.http.response import Http404, JsonResponse

# Create your views here.

# def index(request):
#     return redirect("/agenda/")


def login_user(request):
    return render(request, "login.html")


def logout_user(request):
    logout(request)
    return redirect("/")


def submit_login(request):
    if request.POST:
        username = request.POST.get("username")
        password = request.POST.get("password")
        usuario = authenticate(username=username, password=password)
        if usuario is not None:
            login(request, usuario)
            return redirect("/")
        else:
            messages.error(request, "Usuario ou senha inválido")
    return redirect("/")


@login_required(login_url="/login/")
def lista_eventos(request):
    usuario = request.user
    # __gt apresenta eventos após uma data, __lt apresenta eventos antes de uma data
    evento = Evento.objects.filter(usuario=usuario, data_evento__gt=datetime.now())
    dados = {"eventos": evento}
    return render(request, "agenda.html", dados)


@login_required(login_url="/login/")
def evento(request):
    id_evento = request.GET.get("id")
    usuario = request.user
    dados = {}
    if id_evento:
        dados["evento"] = Evento.objects.get(id=id_evento)
    if usuario != dados["evento"].usuario:
        raise Http404
    return render(request, "evento.html", dados)


def submit_evento(request):
    if request.POST:
        titulo = request.POST.get("titulo")
        data_evento = request.POST.get("data_evento")
        local = request.POST.get("local")
        descricao = request.POST.get("descricao")
        id_evento = request.POST.get("id_evento")
        usuario = request.user

        if id_evento:
            evento = Evento.objects.get(id=id_evento)
            if evento.usuario == usuario:
                evento.id = id_evento
                evento.titulo = titulo
                evento.data_evento = data_evento
                evento.local = local
                evento.descricao = descricao
                evento.save()
            # Evento.objects.filter(id_evento=id_evento).update(titulo=titulo,
            #                                                   data_evento=data_evento,
            #                                                   local=local,
            #                                                   descricao=descricao)
            else:
                raise Http404
        else:
            Evento.objects.create(titulo=titulo,
                                  data_evento=data_evento,
                                  local=local,
                                  descricao=descricao,
                                  usuario=usuario)
    return redirect("/")


@login_required(login_url="/login/")
def delete_evento(request, id_evento):
    usuario = request.user
    try:
        evento = Evento.objects.get(id=id_evento)
    except Exception:
        raise Http404()
    if usuario == evento.usuario:
        evento.delete()
    else:
        raise Http404()
    return redirect("/")


@login_required(login_url="/login/")
def historico(request):
    usuario = request.user
    # __gt apresenta eventos após uma data, __lt apresenta eventos antes de uma data
    evento = Evento.objects.filter(usuario=usuario, data_evento__lt=datetime.now())
    dados = {"eventos": evento}
    return render(request, "historico.html", dados)


def json_lista_evento(request, id_usuario):
    usuario = User.objects.get(id=id_usuario)
    evento = Evento.objects.filter(usuario=usuario).values("id", "titulo")
    return JsonResponse(list(evento), safe=False)
