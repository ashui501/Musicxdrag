import asyncio
from pyspeedtest import SpeedTest
from pyrogram import filters
from pyrogram.types import Message

from AnonXMusic import app  # Make sure this import is correct
from AnonXMusic.misc import SUDOERS  # Make sure this import is correct
from AnonXMusic.utils.decorators.language import language  # Make sure this import is correct


def testspeed(m, _):
    try:
        st = SpeedTest()
        m.edit_text(_["server_12"])  # Indicate starting download test
        download = st.download()  # in bits per second
        m.edit_text(_["server_13"])  # Indicate starting upload test
        upload = st.upload()      # in bits per second
        ping = st.ping()

        result = {
            "client": {"isp": st.isp if hasattr(st, 'isp') else "N/A"},  # ISP information (if available)
            "client": {"country": "N/A"},  # Placeholder for country
            "server": {"name": "N/A"},  # Placeholder for server name
            "server": {"country": "N/A"},  # Placeholder for country
            "server": {"cc": "N/A"},      # Placeholder for country code
            "server": {"sponsor": "N/A"}, # Placeholder for sponsor
            "server": {"latency": ping},
            "download": download,
            "upload": upload,
            "ping": ping,
        }
        return result

    except Exception as e:
        error_message = f"Error during speed test: {e}"  # More descriptive error
        print(error_message)  # Print to console for debugging
        return {"error": error_message}  # Return error dictionary


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

    download_mbps = result.get("download", 0) / 1000000  # Use .get() with default
    upload_mbps = result.get("upload", 0) / 1000000  # Use .get() with default
    ping = result.get("ping", 0)

    output = _["server_15"].format(  # Format output string.  Make sure your _["server_15"] key exists in your language file.
        result["client"].get("isp", "N/A"),  # Use .get() with default
        result["client"].get("country", "N/A"),
        result["server"].get("name", "N/A"),
        result["server"].get("country", "N/A"),
        result["server"].get("cc", "N/A"),
        result["server"].get("sponsor", "N/A"),
        ping,  # Use ping directly
    )

    await m.edit_text(output)
    await m.edit_text(f"{output}\nDownload: {download_mbps:.2f} Mbps\nUpload: {upload_mbps:.2f} Mbps")
