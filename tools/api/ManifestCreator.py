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
                                                        state=0) #1

    def _create_departure_manifest(self, product):
        _product = Product.objects.get(product_id=product['name'],
                                       producer_id=self.producer_id)

        sla = SLA.objects.get(limit=product['sla'][:10],
                              temp_min=product['tempMinDegree'],
                              temp_max=product['tempMaxDegree'],
                              hum_min=product['humidMin'],
                              hum_max=product['humidMax'])

        container_group = ContainerGroup.objects.filter(id_product=_product,
                                                        sla_id=sla)\
                                                        .exclude(state=1)\
                                                        .order_by('sla_id', 'quantity')

        if not container_group:
            return []

        qty = product['qty']
        for container in container_group:
            if container.state == 1:
                continue
            if container.quantity < qty:
                qty -= container.quantity
                container.state = 1
                container.save()
                ManifestContainer.objects.create(quantity=container.quantity,
                                                 id_product=_product,
                                                 id_SLA=sla,
                                                 id_manifest=self.manifest)
                self.container_list.append(container)
            elif container.quantity > qty:
                container.quantity -= qty
                container.save()
                new_container = ContainerGroup.objects.create(
                    quantity=qty,
                    id_product=container.id_product,
                    id_room=container.id_product,
                    sla=container.sla,
                    state=1
                    )
                ManifestContainer.objects.create(quantity=qty,
                                                 id_product=_product,
                                                 id_SLA=sla,
                                                 id_manifest=self.manifest)
                self.container_list.append(new_container)
            else:
                container.state = 1
                container.save()
                ManifestContainer.objects.create(quantity=container.quantity,
                                                 id_product=_product,
                                                 id_SLA=sla,
                                                 id_manifest=self.manifest)
                self.container_list.append(container)
                break
