import os
import requests
import json
from colorama import init, Fore, Back, Style; init()
import sys

def checkfolders(paths):
	for path in paths:
		if not os.path.exists(os.path.dirname(path)):
			os.makedirs(os.path.dirname(path))

# Make sure output folders exist.
checkfolders([
	'results/friends/',
	'results/chats/users/',
	'results/chats/groupchats/',
	'results/payment-methods/'
])

def getheaders(token):
	headers = {
	"Content-Type":"application/json",
	"Authorization":token
	}
	return headers # Discord Auth Headers

def getfriends(token):
	r = requests.get("https://discordapp.com/api/v6/users/@me/relationships",headers=getheaders(token))
	friends = json.loads(r.text)
	for friend in friends:
		with open('results/friends/' + friend["user"]["username"] + '-' + friend["user"]["id"] + '.txt','w') as o:
			o.write(f'''
Username: {friend["user"]["username"]}
ID: {friend["user"]["id"]}
Nickname: {str(friend["nickname"])}
Avatar: https://cdn.discordapp.com/avatars/{friend["user"]["id"]}/{friend["user"]["avatar"]}.webp
''')
			o.close()
	return len(friends)

def getchats(token):
	r = requests.get("https://discordapp.com/api/v6/users/@me/channels",headers=getheaders(token))
	chats = json.loads(r.text)
	chatcount = len(chats)
	for chatnum in range(len(chats)):
		chat = chats[chatnum]
		sys.stdout.write(f'\r{Style.BRIGHT}{str(int(chatnum + 1))}/{str(len(chats))}{Style.RESET_ALL} Chats Enumerated...')
		sys.stdout.flush()
		if str(chat["type"]) == '1':
			recipient = chat["recipients"][0]
			with open('results/chats/users/' + recipient["username"] + '-' + recipient["id"] + '.txt','w') as o:
				o.write(f'''
Chat Type: Direct Messages
Chat ID: {chat["id"]}

----------------------------------------

Recipient Username: {recipient["username"]}
Recipient ID: {recipient["id"]}
Recipient Avatar: https://cdn.discordapp.com/avatars/{recipient["id"]}/{recipient["avatar"]}.webp

----------------------------------------

--- LAST 10 MESSAGES ---
''')
				for message in json.loads(requests.get(f'https://discord.com/api/v8/channels/{chat["id"]}/messages?limit=10', headers=getheaders(token)).text):
					try:
						if message['attachments'] != []:
							for file in message['attachments']:
								o.write(f'''\n[{message['timestamp']}] {message["author"]["username"]} Sent a File: {file["filename"]} ({file["url"]})''')
						if message['content'] != "":
							o.write(f'''\n[{message['timestamp']}] {message["author"]["username"]}: {message["content"]}''')
					except TypeError:
						pass
				o.write('\n\n--- END OF LAST 10 MESSAGES ---')
				o.close()
		elif str(chat["type"]) == '3':
			recipients = chat["recipients"]
			with open('results/chats/groupchats/' + str(chat["name"]) + '-' + chat["id"] + '.txt','w') as o:
				o.write(f'''
Chat Type: Group Chat
Chat Name: {chat["name"]}
Chat ID: {chat["id"]}
Recpient Count: {str(len(recipients))}

----------------------------------------
''')
				for recipient in recipients:
					o.write(f'''
Recipient Username: {recipient["username"]}
Recipient ID: {recipient["id"]}
Recipient Avatar: https://cdn.discordapp.com/avatars/{recipient["id"]}/{recipient["avatar"]}.webp
''')
				o.write('''\n----------------------------------------\n\n--- LAST 10 MESSAGES ---\n''')
				for message in json.loads(requests.get(f'https://discord.com/api/v8/channels/{chat["id"]}/messages?limit=10', headers=getheaders(token)).text):
					try:
						if message['attachments'] != []:
							for file in message['attachments']:
								o.write(f'''\n[{message['timestamp']}] {message["author"]["username"]} Sent a File: {file["filename"]} ({file["url"]})''')
						if message['content'] != "":
							o.write(f'''\n[{message['timestamp']}] {message["author"]["username"]}: {message["content"]}''')
					except TypeError:
						pass
				o.write('\n\n--- END OF LAST 10 MESSAGES ---')
				o.close()
	return len(chats)

def getpaymentmethods(token):
	r = requests.get('https://discord.com/api/v8/users/@me/billing/payment-sources',headers=getheaders(token))
	paymentmethods = json.loads(r.text)
	for method in paymentmethods:
		if str(method["type"]) == '2': # Paypal
			with open('results/payment-methods/' + method["id"] + '.txt','w') as o:
				o.write(f'''
ID {method["id"]}
Payment Method Type: PayPal

PayPal Email: {method["email"]}

Billing Name: {method["billing_address"]["name"]}
Billing Address: {str(method["billing_address"]["line_1"])}, {str(method["billing_address"]["line_2"])}, {str(method["billing_address"]["postal_code"])}
Billing City: {method["billing_address"]["city"]}
Billing State: {method["billing_address"]["state"]}
Billing Country: {method["billing_address"]["country"]}
''')
				o.close()

		if str(method["invalid"]) != 'false':
			with open('results/payment-methods/' + method["id"] + '.txt','w') as o:
				o.write(f'''
ID: {method["id"]}
Payment Method Type: Card

Card Brand: {method["brand"]}
Last 4 Digits: {method["last_4"]}
Exp. Month: {str(method["expires_month"])}
Exp. Year: {str(method["expires_year"])}

Billing Name: {method["billing_address"]["name"]}
Billing Address: {str(method["billing_address"]["line_1"])}, {str(method["billing_address"]["line_2"])}, {str(method["billing_address"]["postal_code"])}
Billing City: {method["billing_address"]["city"]}
Billing State: {method["billing_address"]["state"]}
Billing Country: {method["billing_address"]["country"]}
''')
				o.close()
	return len(paymentmethods)
