import requests
from pyrogram import Client, filters
import time
import asyncio 
import os
from telegram import Message, Update
from telegram.ext import ContextTypes, CallbackContext
from AnonXMusic import app
from pyrogram.types import Message
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup

async def upload_to_anonfiles(file_path):
    url = "https://api.anonfiles.com/upload"
    with open(file_path, "rb") as file:
        files = {"file": file}
        response = requests.post(url, files=files)
    
    if response.status_code == 200:
        result = response.json()
        return result["data"]["file"]["url"]["full"]
    else:
        raise Exception(f"Failed to upload file: {response.status_code} - {response.text}")

    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Failed to upload file: {response.status_code} - {response.text}")

async def handle_media(client: Client, message: Message):
    try:
        if message.photo:
            file = await client.download_media(message.photo.file_id)
            downloaded_file = file

            catbox_url = await upload_to_catbox(downloaded_file)
            inline_button = InlineKeyboardButton("ʟɪɴᴋ", url=catbox_url)
            await message.reply(
                "ᴍᴇᴅɪᴀ ᴜᴘʟᴏᴀᴅᴇᴅ ᴛᴏ ᴄᴀᴛʙᴏx.",
                reply_markup=InlineKeyboardMarkup([[inline_button]])
            )
            os.remove(downloaded_file)

        elif message.video:
            video = message.video
            file = await client.download_media(video.file_id)
            downloaded_file = file

            catbox_url = await upload_to_catbox(downloaded_file)
            inline_button = InlineKeyboardButton("ʟɪɴᴋ", url=catbox_url)
            await message.reply(
                "ᴍᴇᴅɪᴀ ᴜᴘᴏᴀᴅᴇᴅ ᴛᴏ ᴄᴀᴛʙᴏx.",
                reply_markup=InlineKeyboardMarkup([[inline_button]])
            )
            os.remove(downloaded_file)

        elif message.document:
            document = message.document
            file = await client.download_media(document.file_id)
            downloaded_file = file

            catbox_url = await upload_to_catbox(downloaded_file)
            inline_button = InlineKeyboardButton("ʟɪɴᴋ", url=catbox_url)
            await message.reply(
                "ᴍᴇᴅɪᴀ ᴜᴘᴏᴀᴅᴇᴅ ᴛᴏ ᴄᴀᴛʙᴏx.",
                reply_markup=InlineKeyboardMarkup([[inline_button]])
            )
            os.remove(downloaded_file)

    except Exception as e:
        await message.reply(f"Failed to upload file: {e}")

@app.on_message(filters.command(["stgm"]))
async def upload_command(client, message):
    if message.from_user.is_bot:
        return
  
    target_message = message.reply_to_message if message.reply_to_message else message
    media = target_message.photo or target_message.video or target_message.document

    if media:
        await handle_media(client, target_message)
    else:
        await message.reply("sᴇɴᴅ ᴏʀ ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴘʜᴏᴛᴏ ᴏʀ ᴠɪᴅᴇᴏ ғᴏʀ ᴜᴘʟᴏᴀᴅ.")
