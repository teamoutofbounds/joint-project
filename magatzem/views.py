from django.shortcuts import render

# Create your views here.


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
