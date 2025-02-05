import asyncio
from pyspeedtest import SpeedTest  # Import SpeedTest from pyspeedtest
from pyrogram import filters
from pyrogram.types import Message

from AnonXMusic import app
from AnonXMusic.misc import SUDOERS
from AnonXMusic.utils.decorators.language import language


def testspeed(m, _):
    try:
        st = SpeedTest()  # Create a SpeedTest object
        st.get_best_server()
        m.edit_text(_["server_12"])
        download = st.download()  # in bits per second
        m.edit_text(_["server_13"])
        upload = st.upload()  # in bits per second
        ping = st.ping()
        # pyspeedtest doesn't directly provide a shareable image.  We'll handle this differently.

        result = {
            "client": {"isp": st.isp},  # Get ISP information if pyspeedtest provides it
            "client": {"country": ""},  # Add a placeholder for country
            "server": {"name": st.best["host"]},
            "server": {"country": ""},  # Add a placeholder for country
            "server": {"cc": ""},      # Add a placeholder for country code
            "server": {"sponsor": ""}, # Add a placeholder for sponsor
            "server": {"latency": ping},
            "download": download,
            "upload": upload,
            "ping": ping,
        }
        return result
    except Exception as e:
        return {"error": str(e)}


@app.on_message(
    filters.command(
        ["speedtest", "spt"], prefixes=["/", "!", "%", ",", "", ".", "@", "#"]
    )
    & SUDOERS
)
@language
async def speedtest_function(client, message: Message, _):
    m = await message.reply_text(_["server_11"])
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, testspeed, m, _)

    if "error" in result:
        await m.edit_text(f"<code>{result['error']}</code>")
        return

    download_mbps = result["download"] / 1000000
    upload_mbps = result["upload"] / 1000000

    output = _["server_15"].format(
        result["client"]["isp"],
        result["client"]["country"], # These will likely be empty with pyspeedtest
        result["server"]["name"],
        result["server"]["country"], # These will likely be empty with pyspeedtest
        result["server"]["cc"],      # These will likely be empty with pyspeedtest
        result["server"]["sponsor"], # These will likely be empty with pyspeedtest
        result["server"]["latency"],
        result["ping"],
    )

    # Since pyspeedtest doesn't provide a shareable image, send a text message with the results
    await m.edit_text(output)  # Edit the original message with the formatted output

    # Optionally, you could add download/upload speeds in Mbps to the output
    await m.edit_text(f"{output}\nDownload: {download_mbps:.2f} Mbps\nUpload: {upload_mbps:.2f} Mbps")
