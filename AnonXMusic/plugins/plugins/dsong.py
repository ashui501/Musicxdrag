import os
from datetime import timedelta

import wget
from pyrogram import Client
from pyrogram import filters
from pyrogram.types import Message
from yt_dlp import YoutubeDL
from youtubesearchpython import VideosSearch
from AnonXMusic import app


@app.on_message(filters.command(["vsong"]))
async def vsong_cmd(client, message):
    """Command to download and send a YouTube video."""
    if len(message.command) < 2:
        return await message.reply_text(
            "❌ <b>Video not found,</b>\nPlease enter the correct video title.",
        )
    infomsg = await message.reply_text("<b>🔍 Searching...</b>", quote=False)
    try:
        search = VideosSearch(message.text.split(None, 1)[1], limit=1).result()["result"][0]
        link = f"https://youtu.be/{search['id']}"
    except Exception as error:
        return await infomsg.edit(f"<b>🔍 Searching...\n\n{error}</b>")

    ydl_opts = {
        "format": "bestvideo+bestaudio",
        "outtmpl": "%(title)s.%(ext)s",
        "merge_output_format": "mp4",
        "cookiefile": "cookies.txt",
    }

    try:
        await infomsg.edit("<b>Downloading video...</b>")
        with YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=True)
            file_name = ydl.prepare_filename(info_dict)
            title = info_dict.get("title", "Unknown")
            duration = info_dict.get("duration", 0)
            views = info_dict.get("view_count", 0)
            channel = info_dict.get("uploader", "Unknown")
            thumb = info_dict.get("thumbnail", None)
    except Exception as error:
        return await infomsg.edit(f"<blockquote><b>Downloading video...\n\n{error}</blockquote></b>")

    thumbnail_path = None
    try:
        if thumb:
            thumbnail_path = wget.download(thumb)
        await client.send_video(
            message.chat.id,
            video=file_name,
            thumb=thumbnail_path,
            file_name=title,
            duration=duration,
            supports_streaming=True,
            caption=(
                f"<b>💡 Information {title}</b>\n\n"
                f"<b>🏷 Name:</b> {title}\n"
                f"<b>🧭 Duration:</b> {timedelta(seconds=duration)}\n"
                f"<b>👀 Views:</b> {views:,}\n"
                f"<b>📢 Channel:</b> {channel}\n"
                f"<b>🔗 Link:</b> <a href='{link}'>YouTube</a>\n\n"
                f"<b>⚡ Powered by:</b> {channel}"
            ),
            reply_to_message_id=message.id,
        )
    finally:
        if thumbnail_path and os.path.isfile(thumbnail_path):
            os.remove(thumbnail_path)
        if file_name and os.path.isfile(file_name):
            os.remove(file_name)
    await infomsg.delete()


@app.on_message(filters.command(["song"]))
async def song_cmd(client, message):
    """Command to download and send a YouTube audio file."""
    if len(message.command) < 2:
        return await message.reply_text(
            "❌ <b>Audio not found,</b>\nPlease enter the correct audio title.",
        )
    infomsg = await message.reply_text("<b>🔍 Searching...</b>", quote=False)
    try:
        search = VideosSearch(message.text.split(None, 1)[1], limit=1).result()["result"][0]
        link = f"https://youtu.be/{search['id']}"
    except Exception as error:
        return await infomsg.edit(f"<b>🔍 Searching...\n\n{error}</b>")

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": "%(title)s.%(ext)s",
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
        "cookiefile": "cookies.txt",
    }

    try:
        await infomsg.edit("<b>Downloading audio...</b>")
        with YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=True)
            file_name = ydl.prepare_filename(info_dict).replace(".webm", ".mp3")
            title = info_dict.get("title", "Unknown")
            duration = info_dict.get("duration", 0)
            views = info_dict.get("view_count", 0)
            channel = info_dict.get("uploader", "Unknown")
            thumb = info_dict.get("thumbnail", None)
    except Exception as error:
        return await infomsg.edit(f"<blockquote><b>Downloading audio...\n\n{error}</b></blockquote>")

    thumbnail_path = None
    try:
        if thumb:
            thumbnail_path = wget.download(thumb)
        await client.send_audio(
            message.chat.id,
            audio=file_name,
            thumb=thumbnail_path,
            file_name=title,
            performer=channel,
            duration=duration,
            caption=(
                f"<b>💡 Information {title}</b>\n\n"
                f"<b>🏷 Name:</b> {title}\n"
                f"<b>🧭 Duration:</b> {timedelta(seconds=duration)}\n"
                f"<b>👀 Views:</b> {views:,}\n"
                f"<b>📢 Channel:</b> {channel}\n"
                f"<b>🔗 Link:</b> <a href='{link}'>YouTube</a>\n\n"
                f"<b>⚡ Powered by:</b> {channel}"
            ),
            reply_to_message_id=message.id,
        )
    finally:
        if thumbnail_path and os.path.isfile(thumbnail_path):
            os.remove(thumbnail_path)
        if file_name and os.path.isfile(file_name):
            os.remove(file_name)
    await infomsg.delete()
