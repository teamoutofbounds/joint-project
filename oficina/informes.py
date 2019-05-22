from django.core.files import File
from django.contrib.auth.models import User, Group
from datetime import date
from django.db.models import Q

from magatzem.models import TaskOperari, ContainerGroup, SLA, ManifestDeparture, ManifestContainer


def tasques_realitzades(_date):
    file_name = "tasques_operaris" + str(_date) + ".xlsx"
    today_tasks = TaskOperari.objects.filter(date=date.today())
    rol = Group.objects.get(name="Operari")
    operaris = User.objects.filter(group=rol)

    with open('../informes/' + file_name) as f:
        myfile = File(f)
        # Header
        myfile.write("Storage&Go\n")
        myfile.write("Data: " + str(_date) + "\n")
        myfile.write("Tasques Operaris\n\n")

        # Header table
        myfile.write("Operari\t# Tasques Completades\t%\n")
        # Content
        content = {}
        total = len(today_tasks)
        for operari in operaris:
            realitzades = 0
            for task in today_tasks:
                if task.user == operari:
                    realitzades += 1

            myfile.write(str(operari) + "\t"
                         + str(realitzades)
                         + "\t" + str(realitzades/total) + "\n")

        myfile.close()
        f.close()


def productes_amb_slas_proxims(_date):
    file_name = "SLAS" + str(date.today()) + "->" + str(date) + ".xlsx"
    slas = SLA.objects.filter(Q(date__ge=date.today()) & Q(date__le=_date))
    containers = ContainerGroup.objects.filter(sla__in=slas)

    with open('../informes/' + file_name) as f:
        myfile = File(f)
        # Header
        myfile.write("Storage&Go\n")
        myfile.write("Data: " + str(date) + "\n")
        myfile.write("Productes amb SLA pròxim\n\n")

        # Header table
        myfile.write()

        # content
        for container in containers:
            myfile.write(str(container) + "\n")

        myfile.close()
        f.close()


def productes_servits_expirats(i_date, f_date):
    file_name = "Incidencies" + str(date.today()) + ".xlsx"
    slas = SLA.objects.filter(Q(date__ge=f_date))
    manifests = ManifestDeparture.objects.filter(Q(date__le=f_date) & Q(date__ge=i_date))
    containers = ManifestContainer.objects.filter(id_manifest__in=manifests)

    with open('../informes/' + file_name) as f:
        myfile = File(f)
        # Header
        myfile.write("Storage&Go\n")
        myfile.write("Data: " + str(date) + "\n")
        myfile.write("Productes amb SLA pròxim\n\n")

        for container in containers:
            if container.sla in slas:
                myfile.write(str(container) + "\n")

    myfile.close()
    f.close()

