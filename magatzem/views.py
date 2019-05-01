from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.views.generic.dates import TodayArchiveView
from django.db.models import Q
from magatzem.models.room import Room
from magatzem.models.task import Task
from magatzem.models.container import Container
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

# from .tasks import assign_task
from tools.algorithms.sala_selector import RoomHandler
from tools.api.product_entry import EntryHandler
from datetime import date


# Check if logged in Mixin
class LoginRequiredMixin(object):
    @method_decorator(login_required())
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)


class ContainerSelectionList(ListView, LoginRequiredMixin):
    model = Room
    context_object_name = 'container_list'
    slug_field = "room"
    slug_url_kwarg = "room"
    template_name = 'magatzem/select-container.html'

    def get_queryset(self):
        self.room = get_object_or_404(Container, room=self.kwargs['room'])
        return Container.objects.filter(room=self.room)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Selecció de Contenidors'
        return context


class RoomList(ListView, LoginRequiredMixin):
    model = Room
    context_object_name = 'room_list'
    template_name = 'magatzem/room-list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Sales'
        return context


class RoomDetail(DetailView, LoginRequiredMixin):
    model = Room
    template_name = 'magatzem/room-detail.html'
    context_object_name = 'room'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = Task.objects.filter(~Q(task_status=4),
                                               Q(origin_room=context['room']) | Q(destination_room=context['room']))
        context['containers'] = Container.objects.filter(room=context['room']).defer('room')
        context['title'] = context['room'].name
        return context


class NotificationsListView(ListView, LoginRequiredMixin):
    model = Task
    context_object_name = 'task_list'
    template_name = 'magatzem/notification.html'
    new_task = False

    def get_queryset(self):
        queryset = Task.objects.filter(Q(user=self.request.user), Q(task_status=1) | Q(task_status=2) |
                                       Q(task_status=3))
        if not queryset:
            queryset = Task.assign_task(self.request.user)
            self.new_task = True

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['new'] = self.new_task
        context['title'] = 'Home'
        return context


class TaskPanelOperaris(TodayArchiveView, LoginRequiredMixin):
    queryset = Task.objects.all()
    date_field = 'date'
    # context_object_name = 'task_list'
    template_name = 'magatzem/tasks-list.html'

    def get_context_data(self, **kwargs):
        tasks = super().get_context_data(**kwargs)
        context = {'todo': [], 'doing': [], 'done': []}
        for task in tasks['object_list']:
            if task.task_status == 0 or task.task_status == 1 or task.task_status == 2:
                context['todo'].append(task)  # pendent assignacio
            elif task.task_status == 3:
                context['doing'].append(task)
            else:
                context['done'].append(task)
        context['title'] = 'Tasques Operaris'
        return context


class HomeGestor(ListView):
    model = Room
    context_object_name = 'rooms'
    template_name = 'magatzem/home-gestor.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home Gestor'
        # get last tasks
        context['last_tasks'] = self.get_last_tasks()
        # get room capacity
        context['capacities'] = {}
        for item in context['object_list']:
            context['capacities'][item.name] = item.quantity * 100 / item.limit

        return context

    def get_last_tasks(self):
        tasks = Task.objects.order_by('-date').filter(date=date.today())
        return tasks


def home_gestor(request):
    context = {}
    context['title'] = 'Home-Gestor'
    return render(request, 'magatzem/home-gestor.html', context)


def home_ceo(request):
    context = {}
    context['title'] = 'Home-CEO'
    return render(request, 'magatzem/home-ceo.html', context)


def home_operari(request):
    context = {}
    context['title'] = 'Home-Operari'
    return render(request, 'magatzem/notification.html', context)


def entrada_producte(request):
    entry_handler = EntryHandler()
    container = entry_handler.generate_entry()

    hum = container['hum']
    temp= container['temp']
    rooms = Room.objects.filter(Q(hum__gte=hum), Q(temp__gte=temp))

    optimization_handler = RoomHandler(container, rooms)

    context = optimization_handler.select_containers()

    return render(request, 'magatzem/product-entry.html', context)


def entrada_producte_mock(request):
    context = {'productes': [
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
    return render(request, 'magatzem/product-entry.html', context)


def llista_sales_mock(request):
    context = {
        'room_list': [
            {
                'name': 'Sala 1',
                'temp': 5,
                'hum': 35,
                'quantity': 25,
                'limit': 50,
                'room_status': 1
            },
            {
                'name': 'Sala 2',
                'temp': 25,
                'hum': 35,
                'quantity': 50,
                'limit': 50,
                'room_status': 1
            },
            {
                'name': 'Sala 3',
                'temp': 50,
                'hum': 35,
                'quantity': 10,
                'limit': 50,
                'room_status': 1
            },
            {
                'name': 'Sala 4',
                'temp': 0,
                'hum': 0,
                'quantity': 0,
                'limit': 50,
                'room_status': 0
            }
        ]

    }

    return render(request, 'magatzem/room-list.html', context)


def sala_mock(request):
    context = {
        'room': {
            'name': 'Sala 1',
            'temp': 5,
            'hum': 35,
            'quantity': 25,
            'limit': 50,
            'room_status': 1
        },
        'tasks': [
            {
                'description': 'Traslladar',
                'containers': {
                    'producer_id': '20199110001',
                    'product_id': 'PERA CONFERENCE',
                    'limit': '08/08/2019',
                    'temp_min': 5,
                    'temp_max': 15,
                    'hum_min': 45,
                    'hum_max': 70,
                    'quantity': 8
                },
                'origin_room': {
                    'name': 'Sala 1',
                    'temp': 5,
                    'hum': 35,
                    'quantity': 25,
                    'limit': 50,
                    'room_status': 1
                },
                'destination_room': {
                    'name': 'Sala 3',
                    'temp': 50,
                    'hum': 35,
                    'quantity': 10,
                    'limit': 50,
                    'room_status': 1
                },
                'task_type': 1,
                'task_status': 1,
            }
        ],
        'containers': [
            {'producer_id': '20199110001',
             'product_id': 'PERA CONFERENCE',
             'limit': '08/08/2019',
             'temp_min': 5,
             'temp_max': 15,
             'hum_min': 45,
             'hum_max': 70,
             'quantity': 8
             },
            {'producer_id': '20199110001',
             'product_id': 'TABLONES CAOBA 7x25',
             'limit': '25/02/2022',
             'temp_min': -5,
             'temp_max': 50,
             'hum_min': 0,
             'hum_max': 40,
             'quantity': 16
             },
            {'producer_id': '20199110001',
             'product_id': 'TABLONES EBANO 7x25',
             'limit': '25/02/2022',
             'temp_min': -5,
             'temp_max': 50,
             'hum_min': 0,
             'hum_max': 40,
             'quantity': 12}
        ],
        'title': 'Sala 1'
    }

    return render(request, 'magatzem/room-detail.html', context)


def seleccionar_productes_mock(request):
    context = {'productes': [
        {'producer_id': '20199110001',
         'product_id': 'MANZANAS GREENTRANS',
         'limit': '25/05/2019',
         'temp_min': 10,
         'temp_max': 15,
         'hum_min': 35,
         'hum_max': 60,
         'quantity': 4,
         'room': {
             'name': 'Sala 1',
             'temp': 5,
             'hum': 35,
             'quantity': 25,
             'limit': 50,
             'room_status': 1
         }
         },
        {'producer_id': '20199110001',
         'product_id': 'MANZANAS GOLDEN',
         'limit': '29/06/2019',
         'temp_min': 10,
         'temp_max': 15,
         'hum_min': 35,
         'hum_max': 60,
         'quantity': 10},
        {'producer_id': '20199110001',
         'product_id': 'PERA CONFERENCE',
         'limit': '08/08/2019',
         'temp_min': 5,
         'temp_max': 15,
         'hum_min': 45,
         'hum_max': 70,
         'quantity': 8},
        {'producer_id': '20199110001',
         'product_id': 'TABLONES CAOBA 7x25',
         'limit': '25/02/2022',
         'temp_min': -5,
         'temp_max': 50,
         'hum_min': 0,
         'hum_max': 40,
         'quantity': 16},
        {'producer_id': '20199110001',
         'product_id': 'TABLONES EBANO 7x25',
         'limit': '25/02/2022',
         'temp_min': -5,
         'temp_max': 50,
         'hum_min': 0,
         'hum_max': 40,
         'quantity': 12}]
    }
    return render(request, 'magatzem/select-container.html', context)


def seleccionar_sala_mock(request):
    context = {
        'productes':
            {'productor_id': '20199110001',
             'producte_id': 'MANZANAS GREENTRANS',
             'limit': '25/05/2019',
             'temp_min': 10,
             'temp_max': 15,
             'hum_min': 35,
             'hum_max': 60,
             'quantitat': 4},
        'room_list': [
            {
                'name': 'Sala 1',
                'temp': 5,
                'hum': 35,
                'quantity': 25,
                'limit': 50,
                'room_status': 1
            },
            {
                'name': 'Sala 2',
                'temp': 25,
                'hum': 35,
                'quantity': 50,
                'limit': 50,
                'room_status': 1
            },
            {
                'name': 'Sala 3',
                'temp': 50,
                'hum': 35,
                'quantity': 10,
                'limit': 50,
                'room_status': 1
            },
            {
                'name': 'Sala 4',
                'temp': 0,
                'hum': 0,
                'quantity': 0,
                'limit': 50,
                'room_status': 0
            }
        ],
        'title': 'seleccio de sala'
    }

    return render(request, 'magatzem/room-selector.html', context)


def rebre_notificacio_mock(request):
    context = {
        'tasks': [
            {
                'description': 'Traslladar',
                'containers':
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
                ,
                'origin_room':
                    {
                        'name': 'Sala 1',
                        'temp': 5,
                        'hum': 35,
                        'quantity': 25,
                        'limit': 50,
                        'room_status': 1
                    }
                ,
                'destination_room':
                    {
                        'name': 'Sala 3',
                        'temp': 50,
                        'hum': 35,
                        'quantity': 10,
                        'limit': 50,
                        'room_status': 1
                    }
                ,
                'task_type': 1,
                'task_status': 2
            },
            {
                'description': 'Traslladar',
                'containers':
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
                ,
                'origin_room':
                    {
                        'name': 'Sala 1',
                        'temp': 5,
                        'hum': 35,
                        'quantity': 25,
                        'limit': 50,
                        'room_status': 1
                    }
                ,
                'destination_room':
                    {
                        'name': 'Sala 3',
                        'temp': 50,
                        'hum': 35,
                        'quantity': 10,
                        'limit': 50,
                        'room_status': 1
                    }
                ,
                'task_type': 1,
                'task_status': 3
            }
        ],
        'title': 'Notificacions'
    }

    return render(request, 'magatzem/notification.html', context)


def panel_tasks_mock(request):
    context = {
        'todo': [
            {'description': 'Transportar manzanas', 'task_type': 0, 'task_status': 'Assignada automaticament',
             'origin_room': 'Moll de càrrega', 'destination_room': 'Sala 3', 'containers': 10},
            {'description': 'Transportar papel baño', 'task_type': 2, 'task_status': 'Assignada manualment',
             'origin_room': 'Sala 2',
             'destination_room': 'Moll de càrrega', 'containers': 5},
            {'description': 'Transportar cervezas', 'task_type': 1, 'task_status': 'Pendent', 'origin_room': 'Sala 3',
             'destination_room': 'Sala 1', 'containers': 3},
        ],
        'doing': [
            {'description': 'Transportar aceite', 'task_type': 1, 'task_status': 'Rebuda', 'origin_room': 'Sala 3',
             'destination_room': 'Sala 1', 'containers': 22},
            {'description': 'Transportar merluza', 'task_type': 1, 'task_status': 'Rebuda', 'origin_room': 'Sala 3',
             'destination_room': 'Sala 4', 'containers': 30},
            {'description': 'Transportar gallo (pescado)', 'task_type': 0, 'task_status': 'Rebuda',
             'origin_room': 'Moll de càrrega',
             'destination_room': 'Sala 3', 'containers': 17},
            {'description': 'Transportar Fairy', 'task_type': 2, 'task_status': 'Rebuda', 'origin_room': 'Sala 2',
             'destination_room': 'Moll de càrrega', 'containers': 8},
        ],
        'done': [
            {'description': 'Transportar café', 'task_type': 0, 'task_status': 'Completada',
             'origin_room': 'Moll de càrrega',
             'destination_room': 'Sala 3', 'containers': 17},
            {'description': 'Transportar jamón', 'task_type': 2, 'task_status': 'Completada', 'origin_room': 'Sala 2',
             'destination_room': 'Moll de càrrega', 'containers': 21},
        ]
    }
    '''
        task_type 0 Entrada | 1 Intern | 2 Sortida
        task_status 0 Pendent | 1 Assignada automaticament | 
                    2 Assignada manualment | 3 Rebuda | 4 Completada
        origin_room
        destination_room
        containers
    '''
    return render(request, 'magatzem/tasks-list.html', context)



