import requests
import random
from telethon import TelegramClient, events, functions
import logging
import asyncio
from asyncio import sleep
from telethon import TelegramClient, events
from telethon.tl.functions.users import GetFullUserRequest
from telethon import events
import random
import re
from collections import defaultdict
owner_id = int(input('Enter Your Telegram USER ID: '))
api_id = int(input('Enter Your API ID: '))
api_hash = input("Enter Your API Hash: ")
client = TelegramClient('selfmybot', api_id, api_hash)
def is_owner(event):
    """Check if the command is sent by the owner."""
    return event.sender_id == owner_id

# ========== Block Command ==========
@client.on(events.NewMessage(pattern=r'\.block (.+)'))
async def block_user_handler(event):
    if not await is_owner(event):  # Ensure only the owner can use the command
        return
    
    # Extract the username from the command
    username = event.pattern_match.group(1).strip()

    try:
        # Resolve the username to get the user entity
        user_to_block = await client.get_entity(username)
        
        # Block the user
        await client(functions.contacts.BlockRequest(user_to_block.id))
        
        # Confirm the action
        await event.edit(f"🚫 Successfully blocked the user: {username}")
    except Exception as e:
        # Handle errors and inform the user
        await event.edit(f"❌ Failed to block {username}. Error: {str(e)}")
        
# ========== Unblock Command ==========
@client.on(events.NewMessage(pattern=r'\.unblock (.+)'))
async def unblock_user_handler(event):
    if not await is_owner(event):  # Ensure only the owner can use the command
        return
    
    # Extract the username from the command
    username = event.pattern_match.group(1).strip()

    try:
        # Resolve the username to get the user entity
        user_to_unblock = await client.get_entity(username)
        
        # Unblock the user
        await client(functions.contacts.UnblockRequest(user_to_unblock.id))
        
        # Confirm the action
        await event.edit(f"✅ Successfully unblocked the user: {username}")
    except Exception as e:
        # Handle errors and inform the user
        await event.edit(f"❌ Failed to unblock {username}. Error: {str(e)}")    
user_email_requests = {}

class Reset:
    def __init__(self):
        self.url = "https://www.instagram.com/api/v1/web/accounts/account_recovery_send_ajax/"
        self.headers = {
            "authority": "www.instagram.com",
            "method": "POST",
            "path": "/api/v1/web/accounts/account_recovery_send_ajax/",
            "scheme": "https",
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US;q=0.8,en;q=0.7",
            "content-type": "application/x-www-form-urlencoded",
            "cookie": "csrftoken=BbJnjd.Jnw20VyXU0qSsHLV; mid=ZpZMygABAAH0176Z6fWvYiNly3y2; ig_did=BBBA0292-07BC-49C8-ACF4-AE242AE19E97; datr=ykyWZhA9CacxerPITDOHV5AE; ig_nrcb=1; dpr=2.75; wd=393x466",
            "origin": "https://www.instagram.com",
            "referer": "https://www.instagram.com/accounts/password/reset/?source=fxcal",
            "sec-ch-ua": '"Not-A.Brand";v="99", "Chromium";v="124"',
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": '"Android"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Linux; Android 10; M2101K786) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
            "x-asbd-id": "129477",
            "x-csrftoken": "BbJnjd.Jnw20VyXU0qSsHLV",
            "x-ig-app-id": "1217981644879628",
            "x-ig-www-claim": "0",
            "x-instagram-ajax": "1015181662",
            "x-requested-with": "XMLHttpRequest"
        }
        self.proxies = {
            "http": "http://hkkqxzia-rotate:h8kgwqbiwytr@p.webshare.io:80/",
            "https": "http://hkkqxzia-rotate:h8kgwqbiwytr@p.webshare.io:80/"
        }
    
    def send(self, email_or_username):
        data = {
            "email_or_username": email_or_username,
            "flow": "fxcal"
        }
        response = requests.post(self.url, headers=self.headers, data=data)
        try:
            return response.json()
        except Exception as e:
            return f"Error occurred: {e}"


reset_handler = Reset()

@client.on(events.NewMessage(pattern=r'\.rst'))
async def insta_command_handler(event):
    if not await is_owner(event):  # Only the owner can use this command
        return

    command_parts = event.raw_text.split(maxsplit=1)
    if len(command_parts) < 2:
        await event.edit("❌ Please provide a username or email.\nExample: `.rst <username/email>`")
        return

    email_or_username = command_parts[1].strip()
    await event.edit(f"🔄 Processing password reset request for `{email_or_username}`...")

    try:
        result = reset_handler.send(email_or_username)
        await event.edit(f"**✅ Result:**\n```{result}```\n**[SHRIDHAR]**(tg://openmessage?user_id=6432270973)")
    except Exception as e:
        await event.edit(f"**❌ Error occurred: **```{str(e)}```")
    
import os,json
COMMANDS_FILE = "commands.json"  # This is where commands will be stored

# Delete the file if it exists (to reset the file)
if os.path.exists(COMMANDS_FILE):
    os.remove(COMMANDS_FILE)
    print(f"{COMMANDS_FILE} deleted successfully!")
else:
    print(f"{COMMANDS_FILE} does not exist.")

# Commands load/save functions
def load_commands():
    try:
        # Trying to load the commands file
        with open(COMMANDS_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # If file not found or JSON is invalid, return empty dictionary
        return {}

def save_commands():
    with open(COMMANDS_FILE, "w") as f:
        json.dump(commands, f, indent=4)

commands = load_commands()

# Owner check function
async def is_owner(event):
    return event.sender_id == owner_id

# Add command (saving the reply message or media path)
@client.on(events.NewMessage(pattern=r'^\.add (\S+)$'))
async def add_command(event):
    if not await is_owner(event):
        return

    command_name = event.pattern_match.group(1)

    if event.reply_to_msg_id:
        reply_msg = await event.get_reply_message()

        # Saving text and file path (if media is present)
        message_data = {"text": reply_msg.text}
        
        if reply_msg.media:
            file_path = await client.download_media(reply_msg.media, "media_files/")
            message_data["media"] = file_path  # Saving file path, not the media object

        commands[command_name] = message_data
        save_commands()

        await event.edit(f"✅ **Command** `.{command_name}` **saved successfully!**")

# Remove command
@client.on(events.NewMessage(pattern=r'^\.remove (\S+)$'))
async def remove_command(event):
    if not await is_owner(event):
        return

    command_name = event.pattern_match.group(1)

    if command_name in commands:
        # Remove the command from the dictionary
        del commands[command_name]
        save_commands()

        await event.edit(f"**Command** `.{command_name}` **removed successfully!!**")

        # Remove the corresponding media file if it exists
        if "media" in commands.get(command_name, {}):
            media_path = commands[command_name]["media"]
            if os.path.exists(media_path):
                os.remove(media_path)
                print(f"Media file {media_path} removed successfully!")
    else:
        await event.edit(f"**Command** `.{command_name}` **does not exist!!**")

# Show all saved commands
@client.on(events.NewMessage(pattern=r'^\.show$'))
async def show_commands(event):
    if not await is_owner(event):
        return

    # Show list of all saved commands
    if commands:
        command_list = "\n".join([f".{command}" for command in commands])
        await event.edit(f"**Available commands:s:**\n\n`{command_list}`")
    else:
        await event.edit("**🚫 No commands saved yet.**")

# Command execution (retrieving the saved message or media)
@client.on(events.NewMessage(pattern=r'^\.([a-zA-Z0-9_]+)$'))
async def handle_command(event):
    if not await is_owner(event):
        return
    command = event.pattern_match.group(1)

    if command in commands:
        file_data = commands[command]
        text = file_data.get("text", "")
        media_path = file_data.get("media", None)

        await event.delete()  # Delete the command message
        if media_path:
            await client.send_file(event.chat_id, media_path, caption=text)
        else:
            await client.send_message(event.chat_id, text)
    # No reply for unknown command (do nothing)
    else:
        return


@client.on(events.NewMessage(pattern=r"\.dm (.+)"))
async def dm_user_handler(event):
    """Send a DM to the mentioned user or replied user when '.dm <text>' is used."""
    if not await is_owner(event):
        return

    # Check if the owner has replied to a message or mentioned a user
    replied_user = event.reply_to_msg_id
    if replied_user:
        # If owner replied to someone, use that user's ID
        message = await event.get_reply_message()
        user = message.sender
    else:
        # If owner mentions a user, extract the username or ID
        mentioned_user = event.pattern_match.group(1)  # Get the text after .dm
        if mentioned_user:
            try:
                # Check if mentioned_user is a username or ID and resolve accordingly
                if mentioned_user.startswith('@'):
                    user = await client.get_entity(mentioned_user)  # Resolve by username
                else:
                    user = await client.get_entity(int(mentioned_user))  # Resolve by ID
            except Exception as e:
                logging.error(f"Error resolving user: {str(e)}")
                await event.edit(f"**❌ Error: Could not resolve `{mentioned_user}`. Please check the user ID or username.**")
                return
        else:
            await event.edit("**❌ Mention a user or reply to a user's message.**")
            return

    # Get the DM message text from the command
    dm_text = event.pattern_match.group(1)

    try:
        # Send the message to the user's DM
        await client.send_message(user, dm_text)
        await event.edit(f"**✅ The message has been sent to `@{user.username or f'User {user.id}'}` in DM.**\n **[SHRIDHAR]**(tg://openmessage?user_id=6432270973)")
    except Exception as e:
        logging.error(f"Error sending DM: {str(e)}")
        await event.edit("❌ Error: Could not send the message to the user's DM.")


@client.on(events.NewMessage(pattern=r'^\.info(?: (.+))?'))
async def user_info(event):
    if not await is_owner(event):  # Ensure only the owner can use the command
        return
    try:
        # Check if the command includes a username or if it's a reply
        if event.pattern_match.group(1):
            # Get username from the command
            username = event.pattern_match.group(1).strip()
            user_full = await client(GetFullUserRequest(username))
        elif event.is_reply:
            # Get user info from the replied message
            reply = await event.get_reply_message()
            user_full = await client(GetFullUserRequest(reply.sender_id))
        else:
            await event.edit("❌ Reply to a user or provide a username.")
            return

        # Extract user details
        user_info = user_full.users[0] if hasattr(user_full, 'users') else user_full.user
        result = f"**╭───⌯【 🔍 𝗨𝘀𝗲𝗿 𝗜𝗻𝗳𝗼 】⌯───╮**\n"
        result += f"👤 **𝗡𝗮𝗺𝗲:** `{user_info.first_name or 'N/A'} {user_info.last_name or ''}`\n"
        result += f"🌷 **𝗨𝘀𝗲𝗿𝗻𝗮𝗺𝗲:** @{user_info.username or 'N/A'}\n"
        result += f"🆔 **𝗨𝘀𝗲𝗿 𝗜𝗗:** `{user_info.id}`\n"
        result += f"🔗 **𝗜𝗗 𝗟𝗶𝗻𝗸:** [Permanent Link](tg://openmessage?user_id={user_info.id})\n"
        result += f"📞 **𝗣𝗵𝗼𝗻𝗲:** `{user_info.phone or 'N/A'}`\n"
        result += f"👥 **𝗜𝘀 𝗕𝗼𝘁:** {'Yes' if user_info.bot else 'No'}\n"
        result += f"🗓️ **𝗟𝗮𝘀𝘁 𝗦𝗲𝗲𝗻:** {user_info.status.__class__.__name__ if user_info.status else 'Hidden'}\n**[SHRIDHAR]**(tg://openmessage?user_id=6432270973)"
        result += f"\n**╰──────────────────╯**"

        await event.edit(result)

    except Exception as e:
        await event.edit(f"❌ Error: {str(e)}")


@client.on(events.NewMessage(pattern=r'\.cmds'))
async def cmds_handler(event):
    """List all available commands with dots."""
    if not await is_owner(event):
        return  # Only the owner can use this command
    
    commands = [
    "`.rst <@>` : **Reset Insta Password**",
    "`.info` : **Get The Info of Someone on Telegram**",
    "`.block` : **Block a User**",
    "`.unblock` : **Unblock a User**",
    "`.dm <text>` : **Send Direct Msg from Group**",
    "`.show` : **Show All Custom Commands**",
    "`.add` : **Add a New Command**",
    "`.remove` : **Remove an Added Command**",
    ]
    await event.edit("📜 **Available Commands**:\n\n" + "\n".join(commands)+'\n **[SHRIDHAR]**(tg://openmessage?user_id=6432270973)')

# ========== Start the Client ==========
client.start()
client.run_until_disconnected()
