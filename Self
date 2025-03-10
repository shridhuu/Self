_A='media'
import requests,random
from telethon import TelegramClient,events,functions
import logging,asyncio
from asyncio import sleep
from telethon import TelegramClient,events
from telethon.tl.functions.users import GetFullUserRequest
from telethon import events
import random,re
from collections import defaultdict
owner_id=int(input('Enter Your Telegram USER ID: '))
api_id=int(input('Enter Your API ID: '))
api_hash=input('Enter Your API Hash: ')
client=TelegramClient('selfmybot',api_id,api_hash)
def is_owner(event):'Check if the command is sent by the owner.';return event.sender_id==owner_id
@client.on(events.NewMessage(pattern='\\.block (.+)'))
async def block_user_handler(event):
	A=event
	if not await is_owner(A):return
	B=A.pattern_match.group(1).strip()
	try:C=await client.get_entity(B);await client(functions.contacts.BlockRequest(C.id));await A.edit(f"🚫 Successfully blocked the user: {B}")
	except Exception as D:await A.edit(f"❌ Failed to block {B}. Error: {str(D)}")
@client.on(events.NewMessage(pattern='\\.unblock (.+)'))
async def unblock_user_handler(event):
	A=event
	if not await is_owner(A):return
	B=A.pattern_match.group(1).strip()
	try:C=await client.get_entity(B);await client(functions.contacts.UnblockRequest(C.id));await A.edit(f"✅ Successfully unblocked the user: {B}")
	except Exception as D:await A.edit(f"❌ Failed to unblock {B}. Error: {str(D)}")
user_email_requests={}
class Reset:
	def __init__(A):C='http://hkkqxzia-rotate:h8kgwqbiwytr@p.webshare.io:80/';B='https';A.url='https://www.instagram.com/api/v1/web/accounts/account_recovery_send_ajax/';A.headers={'authority':'www.instagram.com','method':'POST','path':'/api/v1/web/accounts/account_recovery_send_ajax/','scheme':B,'accept':'*/*','accept-encoding':'gzip, deflate, br','accept-language':'en-US;q=0.8,en;q=0.7','content-type':'application/x-www-form-urlencoded','cookie':'csrftoken=BbJnjd.Jnw20VyXU0qSsHLV; mid=ZpZMygABAAH0176Z6fWvYiNly3y2; ig_did=BBBA0292-07BC-49C8-ACF4-AE242AE19E97; datr=ykyWZhA9CacxerPITDOHV5AE; ig_nrcb=1; dpr=2.75; wd=393x466','origin':'https://www.instagram.com','referer':'https://www.instagram.com/accounts/password/reset/?source=fxcal','sec-ch-ua':'"Not-A.Brand";v="99", "Chromium";v="124"','sec-ch-ua-mobile':'?1','sec-ch-ua-platform':'"Android"','sec-fetch-dest':'empty','sec-fetch-mode':'cors','sec-fetch-site':'same-origin','user-agent':'Mozilla/5.0 (Linux; Android 10; M2101K786) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36','x-asbd-id':'129477','x-csrftoken':'BbJnjd.Jnw20VyXU0qSsHLV','x-ig-app-id':'1217981644879628','x-ig-www-claim':'0','x-instagram-ajax':'1015181662','x-requested-with':'XMLHttpRequest'};A.proxies={'http':C,B:C}
	def send(A,email_or_username):
		B={'email_or_username':email_or_username,'flow':'fxcal'};C=requests.post(A.url,headers=A.headers,data=B)
		try:return C.json()
		except Exception as D:return f"Error occurred: {D}"
reset_handler=Reset()
@client.on(events.NewMessage(pattern='\\.rst'))
async def insta_command_handler(event):
	A=event
	if not await is_owner(A):return
	B=A.raw_text.split(maxsplit=1)
	if len(B)<2:await A.edit('❌ Please provide a username or email.\nExample: `.rst <username/email>`');return
	C=B[1].strip();await A.edit(f"🔄 Processing password reset request for `{C}`...")
	try:D=reset_handler.send(C);await A.edit(f"**✅ Result:**\n```{D}```\n**[SHRIDHAR]**(tg://openmessage?user_id=6432270973)")
	except Exception as E:await A.edit(f"**❌ Error occurred: **```{str(E)}```")
import os,json
COMMANDS_FILE='commands.json'
if os.path.exists(COMMANDS_FILE):os.remove(COMMANDS_FILE);print(f"{COMMANDS_FILE} deleted successfully!")
else:print(f"{COMMANDS_FILE} does not exist.")
def load_commands():
	try:
		with open(COMMANDS_FILE,'r')as A:return json.load(A)
	except(FileNotFoundError,json.JSONDecodeError):return{}
def save_commands():
	with open(COMMANDS_FILE,'w')as A:json.dump(commands,A,indent=4)
commands=load_commands()
async def is_owner(event):return event.sender_id==owner_id
@client.on(events.NewMessage(pattern='^\\.add (\\S+)$'))
async def add_command(event):
	A=event
	if not await is_owner(A):return
	C=A.pattern_match.group(1)
	if A.reply_to_msg_id:
		B=await A.get_reply_message();D={'text':B.text}
		if B.media:E=await client.download_media(B.media,'media_files/');D[_A]=E
		commands[C]=D;save_commands();await A.edit(f"✅ **Command** `.{C}` **saved successfully!**")
@client.on(events.NewMessage(pattern='^\\.remove (\\S+)$'))
async def remove_command(event):
	B=event
	if not await is_owner(B):return
	A=B.pattern_match.group(1)
	if A in commands:
		del commands[A];save_commands();await B.edit(f"**Command** `.{A}` **removed successfully!!**")
		if _A in commands.get(A,{}):
			C=commands[A][_A]
			if os.path.exists(C):os.remove(C);print(f"Media file {C} removed successfully!")
	else:await B.edit(f"**Command** `.{A}` **does not exist!!**")
@client.on(events.NewMessage(pattern='^\\.show$'))
async def show_commands(event):
	A=event
	if not await is_owner(A):return
	if commands:B='\n'.join([f".{A}"for A in commands]);await A.edit(f"**Available commands:s:**\n\n`{B}`")
	else:await A.edit('**🚫 No commands saved yet.**')
@client.on(events.NewMessage(pattern='^\\.([a-zA-Z0-9_]+)$'))
async def handle_command(event):
	A=event
	if not await is_owner(A):return
	B=A.pattern_match.group(1)
	if B in commands:
		C=commands[B];D=C.get('text','');E=C.get(_A,None);await A.delete()
		if E:await client.send_file(A.chat_id,E,caption=D)
		else:await client.send_message(A.chat_id,D)
	else:return
@client.on(events.NewMessage(pattern='\\.dm (.+)'))
async def dm_user_handler(event):
	"Send a DM to the mentioned user or replied user when '.dm <text>' is used.";A=event
	if not await is_owner(A):return
	E=A.reply_to_msg_id
	if E:F=await A.get_reply_message();B=F.sender
	else:
		C=A.pattern_match.group(1)
		if C:
			try:
				if C.startswith('@'):B=await client.get_entity(C)
				else:B=await client.get_entity(int(C))
			except Exception as D:logging.error(f"Error resolving user: {str(D)}");await A.edit(f"**❌ Error: Could not resolve `{C}`. Please check the user ID or username.**");return
		else:await A.edit("**❌ Mention a user or reply to a user's message.**");return
	G=A.pattern_match.group(1)
	try:await client.send_message(B,G);await A.edit(f"**✅ The message has been sent to `@{B.username or f"User {B.id}"}` in DM.**\n **[SHRIDHAR]**(tg://openmessage?user_id=6432270973)")
	except Exception as D:logging.error(f"Error sending DM: {str(D)}");await A.edit("❌ Error: Could not send the message to the user's DM.")
@client.on(events.NewMessage(pattern='^\\.info(?: (.+))?'))
async def user_info(event):
	E='N/A';C=event
	if not await is_owner(C):return
	try:
		if C.pattern_match.group(1):F=C.pattern_match.group(1).strip();D=await client(GetFullUserRequest(F))
		elif C.is_reply:G=await C.get_reply_message();D=await client(GetFullUserRequest(G.sender_id))
		else:await C.edit('❌ Reply to a user or provide a username.');return
		A=D.users[0]if hasattr(D,'users')else D.user;B=f"**╭───⌯【 🔍 𝗨𝘀𝗲𝗿 𝗜𝗻𝗳𝗼 】⌯───╮**\n";B+=f"👤 **𝗡𝗮𝗺𝗲:** `{A.first_name or E} {A.last_name or""}`\n";B+=f"🌷 **𝗨𝘀𝗲𝗿𝗻𝗮𝗺𝗲:** @{A.username or E}\n";B+=f"🆔 **𝗨𝘀𝗲𝗿 𝗜𝗗:** `{A.id}`\n";B+=f"🔗 **𝗜𝗗 𝗟𝗶𝗻𝗸:** [Permanent Link](tg://openmessage?user_id={A.id})\n";B+=f"📞 **𝗣𝗵𝗼𝗻𝗲:** `{A.phone or E}`\n";B+=f"👥 **𝗜𝘀 𝗕𝗼𝘁:** {"Yes"if A.bot else"No"}\n";B+=f"🗓️ **𝗟𝗮𝘀𝘁 𝗦𝗲𝗲𝗻:** {A.status.__class__.__name__ if A.status else"Hidden"}\n**[SHRIDHAR]**(tg://openmessage?user_id=6432270973)";B+=f"\n**╰──────────────────╯**";await C.edit(B)
	except Exception as H:await C.edit(f"❌ Error: {str(H)}")
@client.on(events.NewMessage(pattern='\\.cmds'))
async def cmds_handler(event):
	'List all available commands with dots.';A=event
	if not await is_owner(A):return
	B=['`.rst <@>` : **Reset Insta Password**','`.info` : **Get The Info of Someone on Telegram**','`.block` : **Block a User**','`.unblock` : **Unblock a User**','`.dm <text>` : **Send Direct Msg from Group**','`.show` : **Show All Custom Commands**','`.add` : **Add a New Command**','`.remove` : **Remove an Added Command**'];await A.edit('📜 **Available Commands**:\n\n'+'\n'.join(B)+'\n **[SHRIDHAR]**(tg://openmessage?user_id=6432270973)')
client.start()
client.run_until_disconnected()
