# <============================================== IMPORTS =========================================================>
import speedtest
from pyrogram import Client, filters
from pyrogram.enums import ChatAction
from pyrogram.errors import UserNotParticipant

from AnonXMusic import app
from AnonXMusic.plugins.helper_funcs.chat_status import check_admin

# <=======================================================================================================>


# <================================================ FUNCTION =======================================================>
def convert(speed):
    return round(int(speed) / 1048576, 2)


# Handle the /speedtest command
@app.on_message(filters.command("speedtest"))
async def speedtestxyz(client, message):
    # Start the speedtest
    await app.send_chat_action(message.chat.id, ChatAction.TYPING)
    msg = await message.reply_text("Running SpeedTest...")

    # Perform SpeedTest
    speed = speedtest.Speedtest()
    speed.get_best_server()
    speed.download()
    speed.upload()

    replymsg = "SpeedTest Results:"

    # Send result as image or text based on user preference
    if message.text == "/speedtest image":
        speedtest_image = speed.results.share()
        await message.reply_photo(photo=speedtest_image, caption=replymsg)
    elif message.text == "/speedtest text":
        result = speed.results.dict()
        replymsg += f"\nDownload: `{convert(result['download'])}Mb/s`\nUpload: `{convert(result['upload'])}Mb/s`\nPing: `{result['ping']}`"
        await message.reply_text(replymsg, parse_mode="Markdown")

    # Delete the initial "Running SpeedTest..." message
    await msg.delete()


# <================================================ HANDLER =======================================================>
SPEED_TEST_HANDLER = filters.command("speedtest")
app.add_handler(SPEED_TEST_HANDLER, speedtestxyz)

# <================================================ END =======================================================>
