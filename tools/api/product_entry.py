import json

import urllib.request
from bs4 import BeautifulSoup

class EntryHandler:

	def generate_entry(self):
		# create a password manager
		password_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()

		# Add the username and password.
		top_level_url = "https://ourfarms.herokuapp.com/apiRest/REF/?format=json"
		password_mgr.add_password(None, top_level_url, 'GR1', 'gr1234567890')

		handler = urllib.request.HTTPBasicAuthHandler(password_mgr)

		# create "opener" (OpenerDirector instance)
		opener = urllib.request.build_opener(handler)

		# use the opener to fetch a URL
		with opener.open('https://ourfarms.herokuapp.com/apiRest/REF/?format=json') as u:
		#u = opener.open('https://ourfarms.herokuapp.com/apiRest/REF/?format=json')

			soup = BeautifulSoup(u.read(), 'html.parser')
			list_dic = json.loads(soup.decode('utf-8'))

		return list_dic
