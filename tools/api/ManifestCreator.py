from magatzem.models import Product, SLA, ManifestEntrance, ManifestContainer, ManifestDeparture, Manifest, ContainerGroup, Room
import copy


class ApiManifestCreator(object):

    def __init__(self, ref, producer_id, toLocation):
        if not toLocation: # Cas entrada
            ManifestEntrance.objects.get_or_create(ref=ref, origin=producer_id)
        else:   # Cas sortida
            ManifestDeparture.objects.get_or_create(ref=ref, destination=toLocation)
            self.container_list=[]
        self.manifest = Manifest.objects.get(ref=ref)
        self.producer_id = producer_id
        self.toLocation = toLocation

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

        container_group = ContainerGroup.objects.filter(id_product=_product,
                                                        sla_id=sla).order_by('sla_id', 'quantity')
        qty = product['qty']
        for container in container_group:
            if container.quantity < qty:
                qty -= container.quantity
                self.container_list.append(container)
            elif container.quantity > qty:
                container2 = copy.deepcopy(container)
                container2.quantity = qty
                container.quantity -= qty
                container.save()
                self.container_list.append(container2)
            else:
                qty -= container.quantity
                self.container_list.append(container)
                break

        for container in self.container_list:
            container.state=1
            quantity = container.quantity - product['qty']
            ManifestContainer.objects.create(quantity=container.quantity,
                                             id_product=_product,
                                             id_SLA=sla,
                                             id_manifest=self.manifest)
