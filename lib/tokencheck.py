import requests
import json
def check(token):
	headers = {'authorization': token}
	r = requests.get('https://discordapp.com/api/v7/users/@me', headers=headers)
	if r.status_code == 200:
		return json.loads(r.text)
	else:
		return False
