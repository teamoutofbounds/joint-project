from django.http import Http404
from django.shortcuts import redirect
'''
from django.contrib.auth.models import User
from users.forms import SignUpForm
from django.contrib.auth.models import Group
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
'''
# Create your views here.


def redirect_view(request):
    if request.user.groups.filter(name='Gestor').exists():
        response = redirect('gestor-home')
    elif request.user.groups.filter(name='Operari').exists():
        response = redirect('operaris-home')
    elif request.user.groups.filter(name='Tecnic').exists():
        response = redirect('tecnics-home')
    elif request.user.groups.filter(name='Ceo').exists():
        response = redirect('oficina/ceo/')
    else:
        raise Http404
    return response


'''
def signup(request): #afegim els usuaris en grups segons el seu registre
    gestor = Group.objects.get_or_create(name='Gestor')[0]
    operari = Group.objects.get_or_create(name='Operari')[0]
    tecnic = Group.objects.get_or_create(name='Tecnic')[0]
    ceo = Group.objects.get_or_create(name='Ceo')[0]
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            type_profile = form.cleaned_data.get('user_type')
            if type_profile.name == "Gestor":
                user.groups.add(gestor)
                user.save()
            elif type_profile.name == "Operari":
                user.groups.add(operari)
                user.save()
            elif type_profile.name == "Tecnic":
                user.groups.add(tecnic)
                user.save()
            elif type_profile.name == "Ceo":
                user.groups.add(ceo)
                user.save()
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'users/register.html', {'form': form})
'''
