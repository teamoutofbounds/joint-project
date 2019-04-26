'''
import base64
import json
from pip._vendor import requests


class EntryHandler:

	def generate_entry(self):
		response = requests.get(
			'https://ourfarms.herokuapp.com/apiRest/product/?format=json',
			auth=('GR1', 'gr1234567890')
		)

		if response.status_code != 200:
			return -1

		dic = json.loads(response.content)
		return self._create_dict(dic)

	def _create_dict(self, dic):
		container = dict()
		container['name'] = dic['name']
		container['quantity'] = dic['quantity']
		container['temp_max'] = dic['tempMaxDegree']
		container['temp_min'] = dic['tempMinDegree']
		container['hum_max'] = dic['humidMax']
		container['hum_min'] = dic['humidMin']
		container['date'] = dic['sla']
		return container
'''