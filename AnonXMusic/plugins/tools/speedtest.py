import asyncio
import speedtest  # Keep the speedtest import
from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup

from AnonXMusic import app  # Your bot's app instance
from AnonXMusic.misc import SUDOERS  # Your SUDO users list
from AnonXMusic.utils.decorators.language import language  # Your language decorator


def convert(speed):
    return round(int(speed) / 1048576, 2)


def testspeed(m, _):  # No need for asyncio.get_event_loop here
    try:
        st = speedtest.Speedtest()
        st.get_best_server()  # Keep this for server selection
        m.edit_text(_["speedtest_running"]) # Use language string
        download = st.download()
        m.edit_text(_["speedtest_downloading"]) # Use language string
        upload = st.upload()
        result = st.results.dict()  # Get the results as a dictionary
        return result
    except Exception as e:
        return {"error": str(e)}


@app.on_message(
    filters.command(["speedtest", "spt"], prefixes=["/", "!", "%", ",", "", ".", "@", "#"]) & SUDOERS
)
@language
async def speedtest_function(client, message: Message, _):
    m = await message.reply_text(_["speedtest_starting"])  # Initial message
    result = await asyncio.get_event_loop().run_in_executor(None, testspeed, m, _) # Run in executor

    if "error" in result:
        await m.edit_text(f"<code>{result['error']}</code>")
        return

    # Inline keyboard buttons
    buttons = [
        [
            InlineKeyboardButton(_["speedtest_image_button"], callback_data="speedtest_image"),
            InlineKeyboardButton(_["speedtest_text_button"], callback_data="speedtest_text"),
        ],
    ]
    await m.edit_text(_["speedtest_mode"], reply_markup=InlineKeyboardMarkup(buttons))  # Ask for mode


@app.on_callback_query(filters.regex("speedtest_.*") & SUDOERS)
@language
async def speedtest_callback(client, callback_query, _):
    await callback_query.answer()  # Acknowledge the button press
    try:
        message = callback_query.message
        result = message.reply_to_message.text # Get the result from the original message
        if "SpeedTest Results" not in result:
            await message.edit_text(_["speedtest_noreply"])
            return

        download = float(result.split('Download: ')[1].split('Mb/s')[0])
        upload = float(result.split('Upload: ')[1].split('Mb/s')[0])
        ping = float(result.split('Ping: ')[1])

        if callback_query.data == "speedtest_image":
            # This part needs adaptation. The original code used speedtest.results.share(), which is not available in pyspeedtest.
            # You will likely have to find an alternative library to generate a speed test image.
            await message.edit_text(_["speedtest_noimage"])  # Placeholder message for now.
            return # Exit early

        elif callback_query.data == "speedtest_text":
            output = _["speedtest_results"].format(download, upload, ping) # Use language string
            await message.edit_text(output, parse_mode="markdown")

    except Exception as e:
        await message.edit_text(f"Error processing callback: {e}")
