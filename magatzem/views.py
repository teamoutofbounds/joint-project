from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.db.models import Q

from magatzem.models.room import Room
from magatzem.models.task import Task
from magatzem.models.container import Container


class RoomList(ListView):
    model = Room
    context_object_name = 'room_list'
    template_name = 'magatzem/room-list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Sales'


class RoomDetail(DetailView):
    model = Room
    template_name = 'magatzem/room-detail.html'
    context_object_name = 'room'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = Task.objects.filter(~Q(task_status=4),
                                               Q(origin_room=context['room']) | Q(destination_room=context['room']))
        context['containers'] = Container.objects.filter(room=context['room']).defer('room')
        context['title'] = context['room'].title
        return context


def exemple_mock(request):
    context = {
        'variable': 'Hello World!!',
    }

    return render(request, 'magatzem/exemple.html', context)


def entrada_producte_mock(request):
    context = {'productes' : [
        {'productor_id': '20199110001',
         'producte_id': 'MANZANAS GREENTRANS',
         'limit': '25/05/2019',
         'temp_min': 10,
         'temp_max': 15,
         'hum_min': 35,
         'hum_max': 60,
         'quantitat': 4},
        {'productor_id': '20199110001',
         'producte_id': 'MANZANAS GOLDEN',
         'limit': '29/06/2019',
         'temp_min': 10,
         'temp_max': 15,
         'hum_min': 35,
         'hum_max': 60,
         'quantitat': 10},
        {'productor_id': '20199110001',
         'producte_id': 'PERA CONFERENCE',
         'limit': '08/08/2019',
         'temp_min': 5,
         'temp_max': 15,
         'hum_min': 45,
         'hum_max': 70,
         'quantitat': 8},
        {'productor_id': '20199110001',
         'producte_id': 'TABLONES CAOBA 7x25',
         'limit': '25/02/2022',
         'temp_min': -5,
         'temp_max': 50,
         'hum_min': 0,
         'hum_max': 40,
         'quantitat': 16},
        {'productor_id': '20199110001',
         'producte_id': 'TABLONES EBANO 7x25',
         'limit': '25/02/2022',
         'temp_min': -5,
         'temp_max': 50,
         'hum_min': 0,
         'hum_max': 40,
         'quantitat': 12}]
    }
    return render(request, 'magatzem/entrada.html', context)


def llista_sales_mock(request):
    context = {
        'room_list': [
            {
                'name': 'Sala 1',
                'temp_min': 0,
                'temp_max': 5,
                'hum_min': 15,
                'hum_max': 35,
                'quantity': 25,
                'limit': 50,
                'room_status': 1
            },
            {
                'name': 'Sala 2',
                'temp_min': 12,
                'temp_max': 25,
                'hum_min': 25,
                'hum_max': 35,
                'quantity': 50,
                'limit': 50,
                'room_status': 1
            },
            {
                'name': 'Sala 3',
                'temp_min': -5,
                'temp_max': 50,
                'hum_min': 15,
                'hum_max': 35,
                'quantity': 10,
                'limit': 50,
                'room_status': 1
            },
            {
                'name': 'Sala 4',
                'temp_min': 0,
                'temp_max': 0,
                'hum_min': 0,
                'hum_max': 0,
                'quantity': 0,
                'limit': 50,
                'room_status': 0
            }
        ]

    }

    return render(request, 'insertar_ruta al html que utilitza el mock', context)


def sala_mock(request):
    context = {
        'room': {
            'name': 'Sala 1',
            'temp_min': 0,
            'temp_max': 5,
            'hum_min': 15,
            'hum_max': 35,
            'quantity': 25,
            'limit': 50,
            'room_status': 1
        },
        'tasks': {
            'description': 'Traslladar',
            'containers': [
                {
                    'productor_id': '20199110001',
                    'producte_id': 'PERA CONFERENCE',
                    'limit': '08/08/2019',
                    'temp_min': 5,
                    'temp_max': 15,
                    'hum_min': 45,
                    'hum_max': 70,
                    'quantitat': 8
                }
            ],
            'origin_room': {
                'name': 'Sala 1',
                'temp_min': 0,
                'temp_max': 5,
                'hum_min': 15,
                'hum_max': 35,
                'quantity': 25,
                'limit': 50,
                'room_status': 1
            },
            'destination_room': {
                'name': 'Sala 3',
                'temp_min': -5,
                'temp_max': 50,
                'hum_min': 15,
                'hum_max': 35,
                'quantity': 10,
                'limit': 50,
                'room_status': 1
            },
            'task_type': 1,
            'task_status': 1,
        },
        'contenidors': [
            {'productor_id': '20199110001',
             'producte_id': 'PERA CONFERENCE',
             'limit': '08/08/2019',
             'temp_min': 5,
             'temp_max': 15,
             'hum_min': 45,
             'hum_max': 70,
             'quantitat': 8
             },
            {'productor_id': '20199110001',
             'producte_id': 'TABLONES CAOBA 7x25',
             'limit': '25/02/2022',
             'temp_min': -5,
             'temp_max': 50,
             'hum_min': 0,
             'hum_max': 40,
             'quantitat': 16
             },
            {'productor_id': '20199110001',
             'producte_id': 'TABLONES EBANO 7x25',
             'limit': '25/02/2022',
             'temp_min': -5,
             'temp_max': 50,
             'hum_min': 0,
             'hum_max': 40,
             'quantitat': 12}
        ],
        'title': 'Sala 1'
    }

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
