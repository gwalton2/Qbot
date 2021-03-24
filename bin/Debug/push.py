import requests
import csv
from threading import Thread
import time

BASE_URI = 'https://pushmeapi.jagcesar.se'

clients = {}

def update():
	global clients
	csvfile = open('hq_clients.csv', 'r', encoding = 'UTF-8')
	data = list(csv.reader(csvfile))

	for user in data[1:]:
		task = user[4]
		identifier = user[3]

		if 'add' in task:
			clients[identifier] = user[0]

		if 'remove' in task:
			remove(identifier)

		if 'confirm' in task:
			confirm(identifier, user[2])
			clients[identifier] = user[0]

def remove(identifier):
	message = 'Your subscription with ScottBot has expired. Thank you so much for joining us. To get more ScottBot select this message in the PushMe app to visit us on Ebay.'
	url = 'https://www.ebay.com/itm/HQ-Triva-Bot/302758151611'
	send(message, identifier, url=url)

def confirm(identifier, date):
	message1 = 'You are confirmed with ScottBot!'
	message2 = f'Your subscription is set to expire on {date}'

	send(message1, identifier)
	time.sleep(2)
	send(message2, identifier)

def push(message):
	for user in clients:
		process = Thread(target = send, args = [message, user])
		process.start()

def send(message, identifier, url=None):
	r = requests.post(BASE_URI, data={'identifier': identifier, 'title': message, 'url': url})

	if r.status_code != 200:
		r = requests.post(BASE_URI, data={'identifier': identifier, 'title': message, 'url': url})

		if r.status_code != 200:
			print(f'Error with client: {clients[identifier]}')

	