from datetime import date

from django.contrib.auth import authenticate
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User, Group
from django.shortcuts import render, redirect
from django.views.generic import ListView, TemplateView, DetailView
from django.db.models import Q

from magatzem.models import SLA, ContainerGroup, Room, TaskOperari, ManifestEntrance, ManifestDeparture, Manifest, \
    ManifestContainer
from magatzem.views import is_allowed
from users.forms import SignUpForm

# Create your views here.

#TODO
# Funciona els SLA que expiren avui, però s'hauria de mostrar el nom del producte i productor en comptes
# del pk que hi ha. També se pot treure la temperatura i humitat i tal, no ens interessa saber-ho aqui
# Nomes PRODUCTE I PRODUCTOR. I fer la finestra mes gran
class HomeCEO(TemplateView, LoginRequiredMixin, UserPassesTestMixin):
    """ THIS IS A TEMPORARY IMPLEMENTATION:
        Needed to check if all works properly in the front end,
        until the real implementation could be done.
    """
    template_name = 'oficina/home-ceo.html'
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
        context['rooms']= Room.objects.all()
        for item in context['rooms']:
            context['capacities'][item.name] = item.quantity * 100 / item.limit
        today = date.today()
        context['slas']= SLA.objects.filter(limit=str(today))

        return context

    def get_last_tasks(self):
        tasks = TaskOperari.objects.order_by('-date').filter(date=date.today())
        return tasks


#TODO
# Hauria de mostrar coses i no ho fa
# Ha de ser una class
def controlSla(request):
    context ={}
    context['title'] = 'Sla Control'
    context['sla'] = getContainersExpiringSLA(date.today())
    return render(request, 'oficina/sla-control.html', context)

def getContainersExpiringSLA(date):

    # get all possible slas
    slas = SLA.objects.filter(limit=date)
    containers = []
    for sla in slas:
        queryset = ContainerGroup.objects.filter(sla=sla)
        for container in queryset:
            if container not in containers:
                containers.append(container)
    return containers

#TODO
# Canviar a classe PERO FUNCIONA
# Hauria d'haver doble check al botó borrar
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
#TODO
# Arreglar el bugaso dels de sortida
# Separar en dos templates o fer que apretant un botó te surtin els d'entrada i un altre els de sortida
class ManifestList(TemplateView, LoginRequiredMixin, UserPassesTestMixin):

    template_name = 'oficina/manifest-list.html'
    # permission variable
    roles = ('CEO',)

    def get_context_data(self, **kwargs):
        context = super(ManifestList, self).get_context_data(**kwargs)
        context['manifestentry'] = ManifestEntrance.objects.all()
        context['manifestexit'] = ManifestDeparture.objects.all()
        return context


#TODO
# Fer que el producte surti com a entrada nova a la taula i afegir el nom del productor
# que ara surt l'altre producte a la dreta de la taula
class ManifestDetail(DetailView, LoginRequiredMixin, UserPassesTestMixin):
    model = Manifest
    template_name = 'oficina/manifest-detail.html'
    context_object_name = 'manifest'
    # permission variable
    roles = ('CEO',)

    def test_func(self):
        return is_allowed(self.request.user, self.roles)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['manifestcontainers'] = ManifestContainer.objects.filter(~Q(id_manifest=context['manifest']))
        return context


