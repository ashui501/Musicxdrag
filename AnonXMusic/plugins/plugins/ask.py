from pyrogram import filters
from pyrogram.enums import ChatAction, ParseMode
from AnonXMusic import app
import aiohttp

# Function to fetch data from Akeno API
async def fetch_data_from_akeno(question):
    url = "https://web-3ypd.onrender.com/api/cohere"  # API endpoint
    params = {"query": question}  # Pass query as a parameter
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            data = await response.json()
            return data.get("results", "No response received.")  # Extract the answer

# Command handler for /ask
@app.on_message(filters.command("ask"))
async def ask_command(client, message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    # Indicate typing action
    await app.send_chat_action(chat_id, ChatAction.TYPING)
    
    if len(message.command) < 2:
        await message.reply_text("Exᴀᴍᴘʟᴇ ᴜsᴀɢᴇ: /ask [your question]")
        return
    
    question = " ".join(message.command[1:])  # Get the question from command arguments
    response = await fetch_data_from_akeno(question)
    
    formatted_response = f"<blockquote>{response}</blockquote>"
    
    await message.reply_text(formatted_response, parse_mode=ParseMode.HTML)
