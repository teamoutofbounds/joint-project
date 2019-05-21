from magatzem.models import Product, SLA, ManifestEntrance, ManifestContainer, ManifestDeparture, Manifest, ContainerGroup, Room


class ApiManifestCreator(object):

    def __init__(self, ref, producer_id):
        Manifest.objects.get_or_create(ref=ref)
        self.manifest = Manifest.objects.get(ref=ref)
        self.producer_id = producer_id

    def _create_entry_manifest(self, product):
        _product = Product.objects.get_or_create(product_id=product['name'],
                                                producer_id=self.producer_id)
        sla = SLA.objects.get_or_create(limit=product['sla'][:10],
                                        temp_min=product['tempMinDegree'],
                                        temp_max=product['tempMaxDegree'],
                                        hum_min=product['humidMin'],
                                        hum_max=product['humidMax'])
        _product = Product.objects.get(product_id=product['name'])
        sla = SLA.objects.get(limit=product['sla'][:10],
                                        temp_min=product['tempMinDegree'],
                                        temp_max=product['tempMaxDegree'],
                                        hum_min=product['humidMin'],
                                        hum_max=product['humidMax'])
        manifest_container = ManifestContainer.objects.create(quantity=product['qty'],
                                                                id_product=_product,
                                                                id_SLA=sla,
                                                                id_manifest=self.manifest)
        room = Room.objects.get(pk=16)
        container_group = ContainerGroup.objects.create(quantity=product['qty'],
                                                        id_room=room,
                                                        id_product=_product,
                                                        sla=sla,
                                                        state=1)

    def _create_departure_manifest(self, product):
        _product = Product.objects.get(product_id=product['name'],
                                        producer_id=self.producer_id)
        sla = SLA.objects.get(limit=product['sla'][:10],
                                temp_min=product['tempMinDegree'],
                                temp_max=product['tempMaxDegree'],
                                hum_min=product['humidMin'],
                                hum_max=product['humidMax'])
        _product = Product.objects.get(product_id=product['name'])
        sla = SLA.objects.get(limit=product['sla'][:10],
                                        temp_min=product['tempMinDegree'],
                                        temp_max=product['tempMaxDegree'],
                                        hum_min=product['humidMin'],
                                        hum_max=product['humidMax'])
        manifest_container = ManifestContainer.objects.create(quantity=product['qty'],
                                                                id_product=_product,
                                                                id_SLA=sla,
                                                                id_manifest=self.manifest)














    """
    def __init__(self, product, transports):
        self.limit = product['sla']
        self.temp_min = product['tempMinDegree']
        self.temp_max = product['tempMaxDegree']
        self.hum_min = product['humidMin']
        self.hum_max = product['humidMax']
        self.quantity = product['qty']
        self.name = product['name']
        self.id_product = Product.objects.get(self.name)
        self.id_SLA =
        self.ref = transports['ref']
        self.producer_id = transports['fromLocation']
        self.id_manifest = ManifestEntrance.objects.get(self.ref)
        self.destination = transports['toLocation']
        self.date = transports['creationDate']


    def _create_manifest_container_dependencies(self):
        self._create_product()
        self._create_sla()

    def _create_product(self):
        Product.objects.save(product_id=self.name,
                             producer_id=self.producer_id)

    def _create_sla(self):
        SLA.objects.save(limit=self.limit,
                         temp_min=self.temp_min,
                         temp_max=self.temp_max,
                         hum_min=self.hum_min,
                         hum_max=self.hum_max)

    def _create_manifest_container(self):
        self._create_manifest_container_dependencies()
        ManifestContainer.objects.save(quantity=self.quantity,
                                       id_product=self.id_product,
                                       id_SLA=self.id_SLA,
                                       id_manifest=self.id_manifest)

    def _create_manifest_departure(self):
        ManifestDeparture.objects.save(ref=self.ref,
                                       destination=self.destination,
                                       date=self.creationDate)

    def create_entry(self):
        self._create_manifest_container()

    def create_departure(self):
        self._create_manifest_departure()
        #TODO CREAR ALGORITME PER BUSCAR ELS MILLOR SLA I CREAR NOUS GRUP CONTAINERS I TAL

        """
