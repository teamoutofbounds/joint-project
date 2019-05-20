from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView
from django.db.models import Q

from magatzem.models.room import Room
from magatzem.models.task_operari import TaskOperari

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group


from tools.algorithms.sala_selector import RoomHandler
from tools.api.product_entry import EntryHandler

from datetime import date

# Check roles function
from users.forms import SignUpForm


def is_allowed(user, roles):
    allowed = False
    belongs_to = user.groups.all()
    for role in belongs_to:
        if role in roles:
            allowed = True
    return allowed


class ContainerSelectionList(ListView, LoginRequiredMixin, UserPassesTestMixin):
    model = Room
    context_object_name = 'container_list'
    slug_field = "room"
    slug_url_kwarg = "room"
    template_name = 'magatzem/select-container.html'
    # permission variable
    roles = ('Gestor',)

    def test_func(self):
        return is_allowed(self.request.user, self.roles)

    def get_queryset(self):
        self.room = get_object_or_404(Room, name=self.kwargs['room'])
        return self.room.get_containers()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Selecció de Contenidors'
        return context


class RoomList(ListView, LoginRequiredMixin, UserPassesTestMixin):
    model = Room
    context_object_name = 'room_list'
    template_name = 'magatzem/room-list.html'
    # permission variable
    roles = ('Gestor', 'CEO',)

    def test_func(self):
        return is_allowed(self.request.user, self.roles)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Sales'
        return context


class RoomDetail(DetailView, LoginRequiredMixin, UserPassesTestMixin):
    model = Room
    template_name = 'magatzem/room-detail.html'
    context_object_name = 'room'
    # permission variable
    roles = ('Gestor',)

    def test_func(self):
        return is_allowed(self.request.user, self.roles)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = TaskOperari.objects.filter(~Q(task_status=4),
                                                      Q(origin_room=context['room']) | Q(destination_room=context['room']))
        context['containers'] = self.object.get_containers()
        context['title'] = context['room'].name
        return context


class NotificationsListView(ListView, LoginRequiredMixin, UserPassesTestMixin):
    model = TaskOperari
    context_object_name = 'task_list'
    template_name = 'magatzem/notification.html'
    new_task = False
    # permission variable
    roles = ('Operari',)

    def test_func(self):
        return is_allowed(self.request.user, self.roles)

    def get_queryset(self):
        queryset = TaskOperari.objects.filter(Q(user=self.request.user), Q(task_status=1) | Q(task_status=2) |
                                              Q(task_status=3))
        if not queryset:
            queryset = TaskOperari.assign_task(self.request.user)
            self.new_task = True

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['new'] = self.new_task
        context['title'] = 'Home'
        return context


class TaskPanelOperaris(ListView, LoginRequiredMixin, UserPassesTestMixin):
    queryset = TaskOperari.objects.filter(date=date.today())
    template_name = 'magatzem/tasks-list.html'
    # permission variable
    roles = ('Gestor', 'CEO')

    def test_func(self):
        return is_allowed(self.request.user, self.roles)

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


class HomeGestor(ListView, LoginRequiredMixin, UserPassesTestMixin):
    model = Room
    context_object_name = 'rooms'
    template_name = 'magatzem/home-gestor.html'
    # permission variable
    roles = ('Gestor',)

    def test_func(self):
        return is_allowed(self.request.user, self.roles)

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
        tasks = TaskOperari.objects.order_by('-date').filter(date=date.today())
        return tasks


class HomeCEO(ListView, LoginRequiredMixin, UserPassesTestMixin):
    """ THIS IS A TEMPORARY IMPLEMENTATION:
        Needed to check if all works properly in the front end,
        until the real implementation could be done.
    """
    model = Room
    context_object_name = 'rooms'
    template_name = 'magatzem/home-ceo.html'
    # permission variable
    roles = ('CEO',)

    def test_func(self):
        return is_allowed(self.request.user, self.roles)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home CEO'
        # get last tasks
        context['last_tasks'] = self.get_last_tasks()
        # get room capacity
        context['capacities'] = {}
        for item in context['object_list']:
            context['capacities'][item.name] = item.quantity * 100 / item.limit

        return context

    def get_last_tasks(self):
        tasks = TaskOperari.objects.order_by('-date').filter(date=date.today())
        return tasks


def home_ceo(request):
    context = {}
    context['title'] = 'Home-CEO'
    return render(request, 'magatzem/home-ceo.html', context)


def home_operari(request):
    context = {}
    context['title'] = 'Home-Operari'
    return render(request, 'magatzem/notification.html', context)


class ConfirmNotification(UpdateView):
    model = TaskOperari
    template_name = 'magatzem/confirm-notification.html'
    fields = {}
    def form_valid(self, form):
        if self.request.POST['confirm'] == "SI":
            form.instance.task_status = 4
            return super().form_valid(form)
        else:
            return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('operaris-notificacions')


def entrada_producte(request):
    if 'ref' in request.GET:
        entry_handler = EntryHandler()
        context = {}
        context['title'] = 'Entrada Productes'
        transports = entry_handler.generate_entry()
        for transport in transports:
            if transport['ref'] == request.GET['ref']:
                context['container'] = transport
    return render(request, 'magatzem/product-entry.html', context)


def manifest_form(request):
    return render(request, 'magatzem/manifest-form.html', {'title': 'Entrada Productes'})


def manifest_sortida_form(request):
    return render(request, 'magatzem/manifest-leave-form.html', {'title': 'Sortida Productes'})


def sortida_producte(request):
    if 'ref' in request.GET:
        entry_handler = EntryHandler()
        context = {}
        context['title'] = 'Sortida Productes'
        transports = entry_handler.generate_entry()
        # mostrar només el que s'ha de treure
        for transport in transports:
            if transport['ref'] == request.GET['ref']:
                context['container'] = transport
    return render(request, 'magatzem/product-leave.html', context)


def manifest_list_mock(request):
    context = {
        'manifestentry': [
            {'reference': '20199110001',
             'productor': 'Empresa Pepito',
             'origin': 'C/ Cannonge Brugulat',
             'date': '25/5/2019'},
            {'reference': '20199110001',
             'productor': 'Empresa Pepito',
             'origin': 'C/ Cannonge Brugulat',
             'date': '25/5/2019'},
            {'reference': '20199110001',
             'productor': 'Empresa Pepito',
             'origin': 'C/ Cannonge Brugulat',
             'date': '25/5/2019'},
            {'reference': '20199110001',
             'productor': 'Empresa Pepito',
             'origin': 'C/ Cannonge Brugulat',
             'date': '25/5/2019'},
        ],
        'manifestexit': [
            {'reference': '20199110001',
             'productor': 'Empresa Pepito',
             'destination': 'C/ Cannonge Brugulat',
             'date': '25/5/2019'},
            {'reference': '20199110001',
             'productor': 'Empresa Pepito',
             'destination': 'C/ Cannonge Brugulat',
             'date': '25/5/2019'},
            {'reference': '20199110001',
             'productor': 'Empresa Pepito',
             'destination': 'C/ Cannonge Brugulat',
             'date': '25/5/2019'},
            {'reference': '20199110001',
             'productor': 'Empresa Pepito',
             'destination': 'C/ Cannonge Brugulat',
             'date': '25/5/2019'},
        ]
    }
    return render(request, 'magatzem/manifest-list.html', context)


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
            },
            {
                'name': 'Sala 5',
                'temp': 0,
                'hum': 0,
                'quantity': 0,
                'limit': 50,
                'room_status': 0
            },
            {
                'name': 'Sala 6',
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


def panel_tecnics_tasks_mock(request):
    context = {
        'todo': [
            {'description': 'Rotura', 'task_type': 1,
             'task_status': 'Pendent', 'room': 'Sala 6',
             'detail': 'Bomba de fred'},
        ],
        'doing': [
            {'description': 'Mantenimiento', 'task_type': 0,
             'task_status': 'Rebuda', 'room': 'Sala 3',
             'detail': 'Motor'},
            {'description': 'Rotura', 'task_type': 1,
             'task_status': 'Rebuda', 'room': 'Sala 3',
             'detail': 'Fan-coil'},
            {'description': 'Ajuste clima', 'task_type': 2,
             'task_status': 'Rebuda', 'room': 'Sala 10',
             'detail': '10º C'},
        ],
        'done': [
            {'description': 'Mantenimiento', 'task_type': 0,
             'task_status': 'Completada', 'room': 'Sala 4',
             'detail': 'Motor'},
            {'description': 'Ajuste clima', 'task_type': 2,
             'task_status': 'Completada', 'room': 'Sala 11',
             'detail': '2º C'},
        ]
    }

    return render(request, 'magatzem/tasks-list-tecnic.html', context)


def list_users(request):
    all_users = User.objects.all()
    return render(request, 'users/list_users-ceo.html', {'all_users': all_users})


def create_user_as_ceo(request):
    gestor = Group.objects.get_or_create(name='Gestor')[0]
    operari = Group.objects.get_or_create(name='Operari')[0]
    tecnic = Group.objects.get_or_create(name='Tecnic')[0]
    ceo = Group.objects.get_or_create(name='Ceo')[0]
    # add permisions to every group here
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            created = authenticate(username=username, password=raw_password)
            user_type = form.cleaned_data.get('user_type')
            if user_type.name == "Gestor":
                created.groups.add(gestor)
                created.save()
            elif user_type.name == "Operari":
                created.groups.add(operari)
                created.save()
            elif user_type.name == "Tecnic":
                created.groups.add(tecnic)
                created.save()
            elif user_type.name == "Ceo":
                created.groups.add(ceo)
                created.save()
            return redirect('list_users')
    else:
        form = SignUpForm()
    return render(request, 'users/usercreate-ceo.html', {'form': form})


def delete_user_as_ceo(request, pk):
    u = User.objects.get(pk=pk)
    u.delete()

    return redirect('list_users')
