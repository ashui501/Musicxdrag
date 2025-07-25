import time
from pyrogram import filters
from pyrogram.enums import ChatType
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from youtubesearchpython.__future__ import VideosSearch

import config
from AnonXMusic import app
from AnonXMusic.misc import _boot_
from AnonXMusic.plugins.sudo.sudoers import sudoers_list
from AnonXMusic.utils.database import (
    add_served_chat,
    add_served_user,
    blacklisted_chats,
    get_lang,
    is_banned_user,
    is_on_off,
)
from AnonXMusic.utils.formatters import get_readable_time
from AnonXMusic.utils.inline import help_pannel, private_panel, start_panel
from config import BANNED_USERS, LOGGER_ID 
from strings import get_string  # Import get_string at the top

@app.on_message(filters.command(["start"]) & filters.private & ~BANNED_USERS)
async def start_pm(client, message: Message):
    await add_served_user(message.from_user.id)

    language = await get_lang(message.chat.id)  # Get language inside the function
    _ = get_string(language)  # Get the translation object

    if len(message.text.split()) > 1:
        name = message.text.split(None, 1)[1]
        if name[0:4] == "help":
            keyboard = help_pannel(_)
            await message.reply_sticker("CAACAgEAAxkBAAJYdWZLJQqyG4fMdFFHFbTZDZPczqfnAAJUAgACODjZR-6jaMt58aQENQQ")
            return await message.reply_video(
                video="https://files.catbox.moe/l372oy.mp4",
                caption=_["help_1"].format(config.SUPPORT_CHAT),
                reply_markup=keyboard,
            )
        elif name[0:3] == "sud":  # Example: Handling sudo
            await sudoers_list(client=client, message=message, _=_)
            if await is_on_off(2):
                await app.send_message(
                    chat_id=LOGGER_ID,
                    text=f"{message.from_user.mention} ᴊᴜsᴛ sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ʙᴏᴛ ᴛᴏ ᴄʜᴇᴄᴋ <b>sᴜᴅᴏʟɪsᴛ</b>.\n\n<b>ᴜsᴇʀ ɪᴅ :</b> <code>{message.from_user.id}</code>\n<b>ᴜsᴇʀɴᴀᴍᴇ :</b> @{message.from_user.username}",
                    message_thread_id=12327  # Send to the specific thread
                )
            return
        elif name[0:3] == "inf":  # Example: Handling info
            m = await message.reply_text("🔎")
            query = (str(name)).replace("info_", "", 1)
            query = f"https://www.youtube.com/watch?v={query}"
            results = VideosSearch(query, limit=1)
            for result in (await results.next())["result"]:
                title = result["title"]
                duration = result["duration"]
                views = result["viewCount"]["short"]
                thumbnail = result["thumbnails"][0]["url"].split("?")[0]
                channellink = result["channel"]["link"]
                channel = result["channel"]["name"]
                link = result["link"]
                published = result["publishedTime"]
            searched_text = _["start_6"].format(
                title, duration, views, published, channellink, channel, app.mention
            )
            key = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text=_["S_B_8"], url=link),
                        InlineKeyboardButton(text=_["S_B_9"], url=config.SUPPORT_CHAT),
                    ],
                ]
            )
            await m.delete()
            await app.send_photo(
                chat_id=message.chat.id,
                photo=thumbnail,
                caption=searched_text,
                reply_markup=key,
            )
            if await is_on_off(2):
                await app.send_message(
                    chat_id=LOGGER_ID,
                    text=f"{message.from_user.mention} ᴊᴜsᴛ sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ʙᴏᴛ ᴛᴏ ᴄʜᴇᴄᴋ <b>ᴛʀᴀᴄᴋ ɪɴғᴏʀᴍᴀᴛɪᴏɴ</b>.\n\n<b>ᴜsᴇʀ ɪᴅ :</b> <code>{message.from_user.id}</code>\n<b>ᴜsᴇʀɴᴀᴍᴇ :</b> @{message.from_user.username}",
                    message_thread_id=12327  # Send to the specific thread
                )
            return

    else:
        out = private_panel(_)
        await message.reply_sticker("CAACAgEAAxkBAAJYdWZLJQqyG4fMdFFHFbTZDZPczqfnAAJUAgACODjZR-6jaMt58aQENQQ")
        await message.reply_video(
            video="https://telegra.ph/file/d2532972423ce5c4b632e.mp4",
            caption=_["start_2"].format(message.from_user.mention, app.mention),
            reply_markup=InlineKeyboardMarkup(out),
        )
        if await is_on_off(2):
            await app.send_message(
                chat_id=LOGGER_ID,
                text=f"{message.from_user.mention} ᴊᴜsᴛ sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ʙᴏᴛ.\n\n<b>ᴜsᴇʀ ɪᴅ :</b> <code>{message.from_user.id}</code>\n<b>ᴜsᴇʀɴᴀᴍᴇ :</b> @{message.from_user.username}",
                message_thread_id=12327  # Send to the specific thread
            )

@app.on_message(filters.command(["start"]) & filters.group & ~BANNED_USERS)
async def start_gp(client, message: Message):
    language = await get_lang(message.chat.id)  # Get language inside the function
    _ = get_string(language)  # Get the translation object

    out = start_panel(_)
    uptime = int(time.time() - _boot_)
    await message.reply_video(
        video="https://telegra.ph/file/d2532972423ce5c4b632e.mp4",
        caption=_["start_1"].format(app.mention, get_readable_time(uptime)),
        reply_markup=InlineKeyboardMarkup(out),
    )
    await add_served_chat(message.chat.id)
    if await is_on_off(2):
        await app.send_message(
            chat_id=LOGGER_ID,
            text=f"{message.from_user.mention} ᴊᴜsᴛ sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ʙᴏᴛ ɪɴ ᴀ ɢʀᴏᴜᴘ.\n\n<b>ᴜsᴇʀ ɪᴅ :</b> <code>{message.from_user.id}</code>\n<b>ᴜsᴇʀɴᴀᴍᴇ :</b> @{message.from_user.username}",
            message_thread_id=12327  # Send to the specific thread
        )

@app.on_message(filters.new_chat_members, group=-1)
async def welcome(client, message: Message):
    for member in message.new_chat_members:
        try:
            language = await get_lang(message.chat.id)
            _ = get_string(language)
            if await is_banned_user(member.id):
                await message.chat.ban_member(member.id)
                continue
            if member.id == app.id:
                if message.chat.type != ChatType.SUPERGROUP:
                    await message.reply_text(_["start_4"])
                    return await app.leave_chat(message.chat.id)
                if message.chat.id in await blacklisted_chats():
                    await message.reply_text(
                        _["start_5"].format(
                            app.mention,
                            f"https://t.me/{app.username}?start=sudolist",
                            config.SUPPORT_CHAT,
                        ),
                        disable_web_page_preview=True,
                    )
                    return await app.leave_chat(message.chat.id)

                out = start_panel(_)
                await message.reply_video(
                    video="https://telegra.ph/file/d2532972423ce5c4b632e.mp4",
                    caption=_["start_3"].format(
                        message.from_user.first_name,
                        app.mention,
                        message.chat.title,
                        app.mention,
                    ),
                    reply_markup=InlineKeyboardMarkup(out),
                )
                await add_served_chat(message.chat.id)
                if await is_on_off(2):
                    await app.send_message(
                        chat_id=LOGGER_ID,
                        text=f"{member.mention} ᴊᴜsᴛ ᴊᴏɪɴᴇᴅ ᴛʜᴇ ᴄʜᴀᴛ.\n\n<b>ᴜsᴇʀ ɪᴅ :</b> <code>{member.id}</code>\n<b>ᴜsᴇʀɴᴀᴍᴇ :</b> @{member.username}",
                        message_thread_id=12327  # Send to the specific thread
                    )
                await message.stop_propagation()
        except Exception as ex:
            print(ex)
