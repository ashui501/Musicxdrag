import asyncio
import speedtest
from pyrogram import filters
from pyrogram.types import Message

from AnonXMusic import app
from AnonXMusic.misc import SUDOERS
from AnonXMusic.utils.decorators.language import language


def testspeed(m, _):
    try:
        test = speedtest.Speedtest()
        test.get_best_server()
        m.edit_text(_["server_12"])
        test.download()
        m.edit_text(_["server_13"])
        test.upload()
        test.results.share()
        result = test.results.dict()
        m.edit_text(_["server_14"])
        return result  # Return the result dictionary
    except Exception as e:
        return {"error": str(e)}  # Return an error dictionary


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

    # Check if the result contains an error
    if "error" in result:
        await m.edit_text(f"<code>{result['error']}</code>")
        return

    # Proceed with accessing the result
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
    msg = await message.reply_photo(photo=result["share"], caption=output)
    await m.delete()
