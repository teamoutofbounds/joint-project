from django.shortcuts import render

# Create your views here.

def exemple_mock(request):
    context = {
        'variable': 'Hello World!!',
    }

    return render(request, 'magatzem/exemple.html', context)

def entrada_producte_mock(request):
    context = {}

    return render(request, 'insertar_ruta al html que utilitza el mock', context)


def llista_sales_mock(request):
    context = {}

    return render(request, 'insertar_ruta al html que utilitza el mock', context)


def sala_mock(request):
    context = {}

    return render(request, 'insertar_ruta al html que utilitza el mock', context)


def selccionar_productes_mock(request):
    context = {}

    return render(request, 'insertar_ruta al html que utilitza el mock', context)


def selccionar_sala_mock(request):
    context = {}

    return render(request, 'insertar_ruta al html que utilitza el mock', context)


def rebre_notificacio_mock(request):
    context = {}

    return render(request, 'insertar_ruta al html que utilitza el mock', context)
