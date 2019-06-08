from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, TemplateView
from django.db.models import Q

from magatzem.models import TaskTecnic, ContainerGroup, Manifest, ManifestContainer, ManifestEntrance

from magatzem.models.room import Room
from magatzem.models.task_operari import TaskOperari

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import render

from tools.algorithms.sala_selector import RoomHandler
from tools.api.ManifestCreator import \
    ApiManifestEntraceCreator, \
    ApiManifestDepartureCreator
from tools.api.product_entry import EntryHandler

from datetime import date


# Security related functions
##############################################################################


def is_allowed(user, roles):
    return user.groups.filter(name__in=roles).exists()


def error_403(request, exception):
    return render(request, 'magatzem/403.html')


# Rooms related functions
##############################################################################

class RoomList(LoginRequiredMixin, UserPassesTestMixin, ListView):
    # permission variable
    roles = ('Gestor', 'CEO',)
    raise_exception = True

    model = Room
    context_object_name = 'room_list'
    template_name = 'magatzem/room-list.html'

    def test_func(self):
        self.queryset = self.get_queryset()
        return is_allowed(self.request.user, self.roles)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Sales'
        return context


class RoomDetail(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Room
    template_name = 'magatzem/room-detail.html'
    context_object_name = 'room'
    # permission variable
    roles = ('Gestor',)
    raise_exception = True

    def test_func(self):
        self.object = self.get_object()
        return is_allowed(self.request.user, self.roles)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = TaskOperari.objects.filter(~Q(task_status=4),
                                                      Q(origin_room=context['room'])
                                                      | Q(destination_room=context['room']))
        context['containers'] = self.object.get_containers()
        context['title'] = "sala " + context['room'].name
        return context


class UpdateClimaRoom(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Room
    fields = ['hum', 'temp']
    template_name = 'magatzem/task-tecnic-clima-room.html'
    context_object_name = 'room'
    # permission variable
    roles = ('Gestor',)
    raise_exception = True

    def test_func(self):
        self.object = self.get_object()
        return is_allowed(self.request.user, self.roles)

    def form_valid(self, form):
        TaskTecnic.objects.create(room=self.object,
                                  description="Ajuste clima",
                                  task_status=1,
                                  task_type=2,
                                  detail='Humitat: ' + str(form.instance.hum) + ', Temperatura: ' + str(form.instance.temp))
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('list-room')


class OpenRoom(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Room
    fields = ['room_status', 'hum', 'temp']
    template_name = 'magatzem/task-tecnic-open.html'
    context_object_name = 'room'
    # permission variable
    roles = ('Gestor',)
    raise_exception = True

    def test_func(self):
        self.object = self.get_object()
        return is_allowed(self.request.user, self.roles)

    def form_valid(self, form):
        TaskTecnic.objects.create(room=self.object,
                                  description="Obrir Sala",
                                  task_status=1,
                                  task_type=2,
                                  detail='Obrir la sala amb : Humitat: ' + str(form.instance.hum) + ', Temperatura: ' + str(form.instance.temp))
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('list-room')

# Notification related functions
##############################################################################


class NotificationsOperarisListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = TaskOperari
    context_object_name = 'task_list'
    template_name = 'magatzem/notification-operari.html'
    new_task = False
    # permission variable
    roles = ('Operari',)
    raise_exception = True

    def test_func(self):
        self.queryset = self.get_queryset()
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


class NotificationsTecnicsListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = TaskTecnic
    context_object_name = 'task_list'
    template_name = 'magatzem/notification-tecnic.html'
    # permission variable
    roles = ('Tecnic',)
    raise_exception = True

    def test_func(self):
        self.queryset = self.get_queryset()
        return is_allowed(self.request.user, self.roles)

    def get_queryset(self):
        queryset = TaskTecnic.objects.filter(Q(task_status=1) | Q(task_status=2) |
                                             Q(task_status=3))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home'
        return context


class ConfirmNotification(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = TaskOperari
    template_name = 'magatzem/confirm-notification.html'
    fields = {}
    # permission variable
    roles = ('Operari',)
    raise_exception = True

    def test_func(self):
        self.object = self.get_object()
        return is_allowed(self.request.user, self.roles)

    def form_valid(self, form):
        if self.request.POST['confirm'] == "SI":
            form.instance.task_status = 4
            self.update_rooms()
            return super().form_valid(form)
        else:
            return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('operaris-notificacions')

    def update_rooms(self):
        dest_room = self.object.destination_room
        container_group = self.object.containers
        origin_room = self.object.origin_room

        update_container_group(container_group, dest_room)
        update_rooms(dest_room, origin_room, container_group.quantity)


def update_container_group(container_group, dest_room):
    container_group.id_room = dest_room
    container_group.save()


def update_rooms(dest_room, origin_room, quantity):
    dest_room.quantity = dest_room.quantity + quantity
    origin_room.quantity = origin_room.quantity - quantity
    dest_room.save()
    origin_room.save()


class ConfirmNotificationTecnics(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = TaskTecnic
    template_name = 'magatzem/confirm-notification-tecnics.html'
    fields = {}
    # permission variable
    roles = ('Tecnic',)
    raise_exception = True

    def test_func(self):
        self.object = self.get_object()
        return is_allowed(self.request.user, self.roles)

    def form_valid(self, form):
        if self.request.POST['confirm'] == "SI":
            form.instance.task_status = 4
            return super().form_valid(form)
        else:
            return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('tecnics-notificacions')


# Task Panels related functions
##############################################################################


class TaskPanelOperaris(LoginRequiredMixin, UserPassesTestMixin, ListView):
    queryset = TaskOperari.objects.filter(date=date.today())
    template_name = 'magatzem/tasks-list-operari.html'
    # permission variable
    roles = ('Gestor', 'CEO')
    raise_exception = True

    def test_func(self):
        self.queryset = self.get_queryset()
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


class TaskPanelTecnics(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'magatzem/tasks-list-tecnic.html'
    # permission variable
    roles = ('Gestor', 'CEO')
    raise_exception = True

    def test_func(self):
        return is_allowed(self.request.user, self.roles)

    def get_context_data(self, **kwargs):
        context = {'todo': TaskTecnic.objects.filter(Q(task_status=0)
                                                     | Q(task_status=1)
                                                     | Q(task_status=2)),
                   'doing': TaskTecnic.objects.filter(task_status=3),
                   'done': TaskTecnic.objects.filter(task_status=4,
                                                     date=date.today()),
                   'title': 'Tasques Tecnics'}
        return context



class EditTecnicTask(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = TaskTecnic
    fields = ['task_type', 'room', 'detail']
    template_name = 'magatzem/task-tecnic-edit.html'

    # permission variable
    roles = ('Gestor',)
    raise_exception = True

    def test_func(self):
        self.object = self.get_object()
        return is_allowed(self.request.user, self.roles)

    def get_task_info(self):
        return self.object



class EditOperariTask(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = TaskTecnic
    fields = ['user']
    template_name = 'magatzem/task-operari-edit.html'
    success_url = reverse_lazy('panel-tecnics')

    # permission variable
    roles = ('Gestor',)
    raise_exception = True

    def test_func(self):
        self.object = self.get_object()
        return is_allowed(self.request.user, self.roles)

    def get_task_info(self):
        return self.object


class DeleteTecnicTask(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = TaskTecnic
    template_name = 'magatzem/task-tecnic-confirm-delete.html'
    success_url = reverse_lazy('panel-tecnics')

    # permission variable
    roles = ('Gestor',)
    raise_exception = True

    def test_func(self):
        self.object = self.get_object()
        return is_allowed(self.request.user, self.roles)


# Home Gestor
##############################################################################

class HomeGestor(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Room
    context_object_name = 'rooms'
    template_name = 'magatzem/home-gestor.html'
    # permission variable
    roles = ('Gestor',)
    raise_exception = True

    def test_func(self):
        self.queryset = self.get_queryset()
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


# Container Movement functions
##############################################################################

class ContainerSelectionList(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Room
    context_object_name = 'container_list'
    slug_field = "room"
    slug_url_kwarg = "room"
    template_name = 'magatzem/select-container.html'
    # permission variable
    roles = ('Gestor',)
    raise_exception = True

    def test_func(self):
        self.queryset = self.get_queryset()
        return is_allowed(self.request.user, self.roles)

    def get_queryset(self):
        self.room = get_object_or_404(Room, name=self.kwargs['room'])
        return self.room.get_containers()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Selecció de Contenidors'
        return context


# Entry/Exit Manifesto functions
##############################################################################

def manifest_form(request):
    return render(request, 'magatzem/manifest-form.html', {'title': 'Entrada Productes', 'entrada': True})


def manifest_sortida_form(request):
    return render(request, 'magatzem/manifest-form.html', {'title': 'Sortida Productes', 'entrada': False})


class EntradaProducte(TemplateView):
    roles = ('Gestor', 'CEO')
    template_name = 'magatzem/product-entry.html'

    def get(self, request, *args, **kwargs):
        context = {}
        context['title'] = 'Entrada Productes'

        entry_handler = EntryHandler()
        transports = entry_handler.generate_entry()

        for transport in transports:
            if transport['ref'] == request.GET['ref']:
                if _check_already_in_system_manifest(transport):
                    context['ref'] = transport['ref']
                    context['entrada'] = True
                    return render(request, 'magatzem/product-entry-existent.html', context)
                context['container'] = transport
        return render(request, 'magatzem/product-entry.html', context)

    def post(self, request, *args, **kwargs):
        context = {}
        context['title'] = 'Entrada Productes'

        entry_handler = EntryHandler()
        transports = entry_handler.generate_entry()

        for transport in transports:
            if transport['ref'] == request.POST['ref']:
                if _check_already_in_system_manifest(transport):
                    context['ref'] = transport['ref']
                    context['entrada'] = True
                    return render(request, 'magatzem/product-entry-existent.html', context)
                _generar_manifest_entrada(transport)
                context['container'] = transport
        return redirect('automated-tasks', request.POST['ref'])


def _check_already_in_system_manifest(transport):
    if Manifest.objects.filter(ref=transport['ref']):
        return True
    return False


def _generar_manifest_entrada(transport):
    # for transport in transports:
    # creator = ApiManifestCreator(transport['ref'], transport['fromLocation'], None)
    creator = ApiManifestEntraceCreator(transport['ref'], transport['fromLocation'], transport['toLocation'])
    for product in transport['Products']:
        creator._create_entry_manifest(product)


def _generar_manifest_sortida(transport):
    # for transport in transports:
    # creator = ApiManifestCreator(transport['ref'], transport['fromLocation'], transport['toLocation'])
    creator = ApiManifestDepartureCreator(transport['ref'], transport['toLocation'], transport['toLocation'])
    for product in transport['Products']:
        creator._create_departure_manifest(product)
    return creator.container_list


def _check_for_manifest_sortida(transport):
    from tools.api.ManifestCreator import CheckProducts
    checker = CheckProducts(transport['toLocation'])
    for product in transport['Products']:
        checker.check_departure_manifest(product)
    return checker.container_list


def sortida_producte(request):
    if 'ref' in request.POST:
        entry_handler = EntryHandler()
        context = {}
        context['title'] = 'Sortida Productes'
        context['is_valid_ref'] = False
        transports = entry_handler.generate_entry()
        # mostrar només el que s'ha de treure
        for transport in transports:
            if transport['ref'] == request.POST['ref']:
                if _check_already_in_system_manifest(transport):
                    context['ref'] = transport['ref']
                    context['entrada'] = False
                    return render(request, 'magatzem/product-entry-existent.html', context)
                context['is_valid_ref'] = True
                containers = _generar_manifest_sortida(transport)
                context['containers'] = containers
                context['ref'] = transport['ref']
                context['toLocation'] = transport['toLocation']
        return render(request, 'magatzem/product-leave.html', context)


class SortidaProducte(TemplateView):
    roles = ('Gestor', 'CEO')
    template_name = 'magatzem/product-leave.html'

    def get(self, request, *args, **kwargs):
        context = {}
        context['title'] = 'Sortida Productes'
        context['is_valid_ref'] = False

        entry_handler = EntryHandler()
        transports = entry_handler.generate_entry()

        for transport in transports:
            if transport['ref'] == request.GET['ref']:
                if _check_already_in_system_manifest(transport):
                    context['ref'] = transport['ref']
                    context['entrada'] = False
                    return render(request, 'magatzem/product-entry-existent.html', context)
                context['container'] = transport
                context['is_valid_ref'] = True
                containers = _check_for_manifest_sortida(transport)
                context['containers'] = containers
        return render(request, 'magatzem/product-leave.html', context)

    def post(self, request, *args, **kwargs):
        context = {}
        context['title'] = 'Sortida Productes'
        context['is_valid_ref'] = False

        entry_handler = EntryHandler()
        transports = entry_handler.generate_entry()

        for transport in transports:
            if transport['ref'] == request.POST['ref']:
                if _check_already_in_system_manifest(transport):
                    context['ref'] = transport['ref']
                    context['entrada'] = False
                    return render(request, 'magatzem/product-entry-existent.html', context)
                context['container'] = transport
                context['is_valid_ref'] = True
                containers = _generar_manifest_sortida(transport)
                context['containers'] = containers
        return render(request, 'magatzem/product-leave.html', context)


# Generar tasques
##############################################################################
class CreateAutomatedTasks(DetailView):
    roles = ('Gestor', 'CEO')
    template_name = 'magatzem/automated-tasks.html'
    model = ManifestEntrance
    context_object_name = 'manifest'
    # permission variable
    raise_exception = True

    def get_object(self):
        object = get_object_or_404(Manifest, ref=self.kwargs['pk'])
        return object

    def get_context_data(self, **kwargs):
        ####################################################
        # Obtains the containers from the manifest
        ###################################################
        context = super().get_context_data()
        m_containers = ManifestContainer.objects.filter(id_manifest=self.object)
        moll = Room.objects.get(name='Moll')

        container_groups_list = []
        for m_container in m_containers:
            container_groups_list.append(ContainerGroup.objects.get(sla_id=m_container.id_SLA,
                                                                    id_product=m_container.id_product,
                                                                    id_room=moll))
        #####################################################
        # Generate variables for the optimizer
        #####################################################
        rooms = Room.objects.all()
        optimizer_rooms = []
        container = {}
        for c_group in container_groups_list:
            container = {'qty': c_group.quantity,
                         'id_product': c_group.id_product}
            for room in rooms:
                if _room_is_able(room, c_group.sla):
                    able_room = {'name': room.name,
                                 'left_stock': room.limit - room.quantity,
                                 'new_containers': 0}
                    optimizer_rooms.append(able_room)
            optime_task_handler = RoomHandler(container, optimizer_rooms)
            productes_assignats = optime_task_handler.select_containers()

            for prod in productes_assignats:
                TaskOperari.objects.create(description="Traslladar",
                                           task_status=0,
                                           task_type=0,
                                           origin_room=moll,
                                           destination_room=Room.objects.get(name=prod['name']),
                                           containers=c_group)
            if productes_assignats:
                context['tasks'] = True
            return context


def _room_is_able(room, sla):
    return sla.temp_min <= room.temp <= sla.temp_max \
           and sla.hum_min <= room.hum <= sla.hum_max \
           and room.room_status == 1 \
           and room.name != "Moll"


# Mock functions
##############################################################################

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
