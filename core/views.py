from django.shortcuts import render, HttpResponse
from core.models import Evento

# Create your views here.

def titulo_evento(request, titulo_evento):
    evento = Evento.objects.get(titulo=titulo_evento)
    return HttpResponse("<h1>O evento {} acontecerá em {}</h1>".format(evento.titulo, evento.data_evento))
