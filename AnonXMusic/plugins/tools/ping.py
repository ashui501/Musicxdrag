from datetime import datetime
import httpx  # For making HTTP requests
from pyrogram import Client, filters
from pyrogram.types import Message

from AnonXMusic import app
from AnonXMusic.core.call import Anony
from AnonXMusic.utils import bot_sys_stats
from AnonXMusic.utils.decorators.language import language
from AnonXMusic.utils.inline import supp_markup
from config import BANNED_USERS, PING_IMG_URL

# Replace with your actual API URL and Bot Token
API_URL = "https://karma-api2.vercel.app/instadl"
DOWNLOADING_STICKER_ID = (
    "CAACAgUAAxkBAAEVtNxnbAfkXOWkvCJSkfjJab2fml0AAbkAAhESAAKKWGlXKi6QQO-bOTM2BA"
)

@app.on_message(filters.command(["ping", "alive"]) & ~BANNED_USERS)
@language
async def ping_com(client, message: Message, _):
    start = datetime.now()
    response = await message.reply_photo(
        photo=PING_IMG_URL,
        caption=_["ping_1"].format(app.mention),
    )
    pytgping = await Anony.ping()
    UP, CPU, RAM, DISK = await bot_sys_stats()
    resp = (datetime.now() - start).microseconds / 1000
    await response.edit_text(
        _["ping_2"].format(resp, app.mention, UP, RAM, CPU, DISK, pytgping),
        reply_markup=supp_markup(_),
    )

# Instagram download command handler
@app.on_message(filters.command(["ig", "instagram", "insta", "instadl"]) & ~BANNED_USERS)
@language
async def instadl_command_handler(client, message: Message, _):
    if len(message.command) < 2:
        await message.reply_text("Usage: /instadl [Instagram URL]")
        return

    link = message.command[1]
    downloading_sticker = None  # Initialize the variable

    try:
        # Send the downloading sticker
        downloading_sticker = await message.reply_sticker(DOWNLOADING_STICKER_ID)

        # Make an asynchronous GET request to the API using httpx
        async with httpx.AsyncClient() as client:
            response = await client.get(API_URL, params={"url": link})
            data = response.json()

        # Check if the API request was successful
        if "content_url" in data:
            content_url = data["content_url"]

            # Determine content type from the URL
            content_type = "video" if "video" in content_url else "photo"

            # Reply with either photo or video
            if content_type == "photo":
                await message.reply_photo(content_url)
            elif content_type == "video":
                await message.reply_video(content_url)
            else:
                await message.reply_text("Unsupported content type.")
        else:
            await message.reply_text(
                "Unable to fetch content. Please check the Instagram URL or try with another Instagram link."
            )

    except Exception as e:
        print(e)
        await message.reply_text("An error occurred while processing the request.")

    finally:
        # Only delete the sticker if it was successfully sent
        if downloading_sticker:
            await downloading_sticker.delete()

# Start the Pyrogram bot
if __name__ == "__main__":
    app.run()
