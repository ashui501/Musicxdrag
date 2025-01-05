import asyncio
import speedtest_cli as speedtest  # Updated import
from pyrogram import filters
from pyrogram.types import Message

from AnonXMusic import app
from AnonXMusic.misc import SUDOERS
from AnonXMusic.utils.decorators.language import language

# Function to run the speed test
def testspeed(m, _):
    try:
        test = speedtest.Speedtest()
        test.get_best_server()
        m = m.edit_text(_["server_12"])
        test.download()
        m = m.edit_text(_["server_13"])
        test.upload()
        test.results.share()
        result = test.results.dict()
        m = m.edit_text(_["server_14"])
    except Exception as e:
        return m.edit_text(f"<code>{e}</code>")
    return result

# Command handler for /speedtest
@app.on_message(filters.command(["speedtest", "spt"]) & SUDOERS)
@language
async def speedtest_function(client, message: Message, _):
    # Notify the user that the speed test is in progress
    m = await message.reply_text(_["server_11"])
    
    # Run the speed test asynchronously
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, testspeed, m, _)
    
    # Format the output message with the results
    output = _["server_15"].format(
        result["client"]["isp"],
        result["client"]["country"],
        result["server"]["name"],
        result["server"]["country"],
        result["server"]["cc"],
        result["server"]["sponsor"],
        result["server"]["latency"],
        result["ping"],
    )
    
    # Send the speed test result as an image with the caption containing the details
    msg = await message.reply_photo(photo=result["share"], caption=output)
    
    # Clean up and delete the waiting message
    await m.delete()
