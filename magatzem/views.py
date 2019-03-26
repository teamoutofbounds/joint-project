from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.views.generic import ListView, DetailView
from django.db.models import Q

from magatzem.models.room import Room
from magatzem.models.task import Task


class RoomList(ListView):
    model = Room
    context_object_name = 'room_list'
    template_name = 'magatzem/room-list.html'


class RoomDetail(DetailView):
    model = Room
    template_name = 'magatzem/room-detail.html'
    context_object_name = 'room'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = Task.objects.filter(~Q(task_status=4),
                                               Q(origin_room=context['room']) | Q(destination_room=context['room']))
        return context


def exemple_mock(request):
    context = {
        'variable': 'Hello World!!',
    }

    return render(request, 'magatzem/exemple.html', context)


def entrada_producte_mock(request):
    context = {'productor_id': '20199110001',
               'producte_id': 'MANZANAS GREENTRANS',
               'limit': '25/02/2019',
               'temp_min': 10,
               'temp_max': 15,
               'hum_min': 35,
               'hum_max': 60,
               'quantitat': 4
               }

    return render(request, 'magatzem/entrada.html', context)


def llista_sales_mock(request):
    context = {}

    return render(request, 'insertar_ruta al html que utilitza el mock', context)


def sala_mock(request):
    context = {}

    return render(request, 'insertar_ruta al html que utilitza el mock', context)


def seleccionar_productes_mock(request):
    context = {}

    return render(request, 'insertar_ruta al html que utilitza el mock', context)


def seleccionar_sala_mock(request):
    context = {}

    return render(request, 'insertar_ruta al html que utilitza el mock', context)


def rebre_notificacio_mock(request):
    context = {}

    return render(request, 'insertar_ruta al html que utilitza el mock', context)
