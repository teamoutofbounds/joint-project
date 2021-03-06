from magatzem.models import Product, SLA, ManifestEntrance, \
    ManifestContainer, ManifestDeparture, ContainerGroup, Room


class ApiManifestCreator(object):

    def __init__(self, producer_id, location):
        self.container_list = []
        self.producer_id = producer_id
        self.toLocation = location

    def _create_product(self, product):
        return Product.objects.get_or_create(product_id=product['name'],
                                             producer_id=self.producer_id)[0]

    @staticmethod
    def _create_sla(product):
        return SLA.objects.get_or_create(limit=product['sla'][:10],
                                         temp_min=product['tempMinDegree'],
                                         temp_max=product['tempMaxDegree'],
                                         hum_min=product['humidMin'],
                                         hum_max=product['humidMax'])[0]

    def _create_manifest_container(self, qty, prod_obj, sla):
        return ManifestContainer.objects.create(quantity=qty,
                                                id_product=prod_obj,
                                                id_SLA=sla,
                                                id_manifest=self.manifest)

    @staticmethod
    def _create_container_group(product, room, prod_obj, sla, state=0):
        return ContainerGroup.objects.create(quantity=product['qty'],
                                             id_room=room,
                                             id_product=prod_obj,
                                             sla=sla,
                                             state=state)  # 1

    def _create_entry_manifest(self, product):
        _product = self._create_product(product)
        sla = ApiManifestCreator._create_sla(product)
        self._create_manifest_container(product['qty'], _product, sla)
        room = Room.objects.get(pk=16)
        ApiManifestCreator._create_container_group(product, room, _product, sla)

    def _create_departure_manifest(self, product):

        _product = Product.objects.get(product_id=product['name'],
                                       producer_id=self.producer_id)
        container_group = \
            ContainerGroup.objects.filter(id_product=_product)\
            .exclude(state=1)\
            .order_by('sla_id', 'quantity')

        if not container_group:
            return []

        self.select_departure_containers(container_group, _product, product['qty'])


    def select_departure_containers(self, container_group, prod_obj, qty):

        for container in container_group:
            if container.state == 1:
                continue
            if container.quantity < qty:
                qty -= container.quantity
                container.state = 1
                container.save()
                self._create_manifest_container(container.quantity,
                                                prod_obj, container.sla)
                self.container_list.append(container)
            elif container.quantity > qty:
                container.quantity -= qty
                container.save()
                new_container = self._create_container_group(qty, container.id_product,
                                                             container.id_room, container.sla, 1)
                self._create_manifest_container(qty, prod_obj, container.sla)
                self.container_list.append(new_container)
            else:
                container.state = 1
                container.save()
                self._create_manifest_container(qty, prod_obj, container.sla)
                self.container_list.append(container)
                break


class ApiManifestEntraceCreator(ApiManifestCreator):
    def __init__(self, ref, producer_id, location):
        ApiManifestCreator.__init__(self, producer_id, location)
        ManifestEntrance.objects.get_or_create(ref=ref, origin=location)
        self.manifest = ManifestEntrance.objects.get(ref=ref)


class ApiManifestDepartureCreator(ApiManifestCreator):
    def __init__(self, ref, producer_id, location):
        ApiManifestCreator.__init__(self, producer_id, location)
        ManifestDeparture.objects.get_or_create(ref=ref, destination=location)
        self.manifest = ManifestDeparture.objects.get(ref=ref)


class CheckProducts:

    def __init__(self, producer_id):
        self.producer_id = producer_id
        self.container_list = []
        self.tmp_containers = []
        self.completed = True

    def check_departure_manifest(self, product):
        _product = Product.objects.get(product_id=product['name'],
                                       producer_id=self.producer_id)
        if not self.completed:
            return

        container_group = \
            ContainerGroup.objects.filter(id_product=_product) \
                .exclude(state=1) \
                .order_by('sla_id', 'quantity')

        self.check_departure_containers(container_group, product['qty'])

    def check_departure_containers(self, container_group, qty):

        for container in container_group:
            if container.state == 1:
                continue
            if container.quantity < qty:
                qty -= container.quantity
                self.add_container(container, container.quantity)
            elif container.quantity > qty:
                container.quantity -= qty
                self.add_container(container, qty)
                qty = 0
            else:
                qty = 0
                self.add_container(container, container.quantity)
                break

        self.check_completed(qty)

    def check_completed(self, qty):
        if qty != 0:
            self.completed = False
            self.container_list = []
        else:
            self.merge_containers()

    def merge_containers(self):
        if not self.tmp_containers:
            return
        new_quantity = 0
        for cont in self.tmp_containers:
            new_quantity += cont[1]

        self.add_regrouped_container(new_quantity)
        self.tmp_containers = []

    def add_container(self, container, quantity):
        self.container_list.append(
            [
                container.id_product.product_id,
                quantity,
                container.sla.temp_min,
                container.sla.temp_max,
                container.sla.hum_min,
                container.sla.hum_max
            ]
        )

    def add_regrouped_container(self, quantity):
        self.container_list.append(
            [
                self.tmp_containers[0][0],
                quantity,
                self.tmp_containers[0][2],
                self.tmp_containers[0][3],
                self.tmp_containers[0][4],
                self.tmp_containers[0][5]
            ]
        )
