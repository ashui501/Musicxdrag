import requests
from pyrogram import Client, filters
import time
import os
from telegram import Message, Update
from telegram.ext import ContextTypes, CallbackContext
from AnonXMusic import app
from pyrogram.types import Message
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup

async def upload_to_envssh(file_path):
    url = "https://envs.sh/"
    try:
        with open(file_path, "rb") as file:
            files = {"file": file}
            response = requests.post(url, files=files)
        
        if response.status_code == 200:
            result = response.json()
            # Assuming the response contains a URL to the uploaded file
            return result["url"]
        else:
            raise Exception(f"Failed to upload file: {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Error uploading file: {e}")

async def handle_media(client: Client, message: Message):
    try:
        if message.photo:
            file = await client.download_media(message.photo.file_id)
            downloaded_file = file

            catbox_url = await upload_to_envssh(downloaded_file)  # Updated to use envs.sh
            inline_button = InlineKeyboardButton("ʟɪɴᴋ", url=catbox_url)
            await message.reply(
                "ᴍᴇᴅɪᴀ ᴜᴘʟᴏᴀᴅᴇᴅ ᴛᴏ ᴇɴᴠs.ᴄᴏᴍ.",
                reply_markup=InlineKeyboardMarkup([[inline_button]])
            )
            os.remove(downloaded_file)

        elif message.video:
            video = message.video
            file = await client.download_media(video.file_id)
            downloaded_file = file

            catbox_url = await upload_to_envssh(downloaded_file)  # Updated to use envs.sh
            inline_button = InlineKeyboardButton("ʟɪɴᴋ", url=catbox_url)
            await message.reply(
                "ᴍᴇᴅɪᴀ ᴜᴘʟᴏᴀᴅᴇᴅ ᴛᴏ ᴇɴᴠs.ᴄᴏᴍ.",
                reply_markup=InlineKeyboardMarkup([[inline_button]])
            )
            os.remove(downloaded_file)

        elif message.document:
            document = message.document
            file = await client.download_media(document.file_id)
            downloaded_file = file

            catbox_url = await upload_to_envssh(downloaded_file)  # Updated to use envs.sh
            inline_button = InlineKeyboardButton("ʟɪɴᴋ", url=catbox_url)
            await message.reply(
                "ᴍᴇᴅɪᴀ ᴜᴘʟᴏᴀᴅᴇᴅ ᴛᴏ ᴇɴᴠs.ᴄᴏᴍ.",
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
