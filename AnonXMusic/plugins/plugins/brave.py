import requests
from pyrogram import filters
from pyrogram.enums import ChatAction
from AnonXMusic import app

# Add your Brave Search API key (if required)
BRAVE_SEARCH_API_KEY = "your_brave_api_key"  # Leave empty if no key is needed

@app.on_message(filters.command(["search", "brave"]))
async def brave_search_handler(client, message):
    chat_id = message.chat.id

    # Indicate typing action
    await app.send_chat_action(chat_id, ChatAction.TYPING)

    # Retrieve the search query from the message
    if len(message.command) > 1:
        search_query = " ".join(message.command[1:])
    else:
        await message.reply_text("Exᴀᴍᴘʟᴇ ᴜsᴀɢᴇ: /sᴇᴀʀᴄʜ Qᴜᴇsᴛɪᴏɴ ᴏʀ Tᴏᴘɪᴄ.")
        return

    try:
        # Brave Search API Endpoint
        search_url = f"https://search.brave.com/api/v1/search?q={search_query}&source=web"
        
        # Make the request to Brave's API
        response = requests.get(search_url, headers={"Authorization": f"Bearer {BRAVE_SEARCH_API_KEY}"})
        response.raise_for_status()
        results = response.json()

        # Extract and format the results
        if "web" in results and len(results["web"]["results"]) > 0:
            reply_text = "**Top Search Results:**\n"
            for index, result in enumerate(results["web"]["results"][:5], 1):  # Limit to 5 results
                reply_text += f"{index}. [{result['title']}]({result['url']})\n"
            await message.reply_text(reply_text, disable_web_page_preview=True)
        else:
            await message.reply_text("No results found for your query. Please try with a different keyword.")

    except Exception as e:
        await message.reply_text(f"» Error: {str(e)}. Please try again later.")
