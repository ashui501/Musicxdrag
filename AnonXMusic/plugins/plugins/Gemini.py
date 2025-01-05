import requests
from pyrogram import filters
from pyrogram.enums import ChatAction
from AnonXMusic import app

# Google API configuration (if using Google Places API)
GOOGLE_API_KEY = "AIzaSyAMKqLzfOYUOjOA-vma74H_skVPYJWuzZI"
GOOGLE_API_URL = "https://maps.googleapis.com/maps/api/place/textsearch/json"

# Gemini API configuration (if using Gemini cryptocurrency API)
GEMINI_API_URL = "https://api.gemini.com/v1/marketdata"
GEMINI_API_KEY = "your_gemini_api_key_here"  # Replace with your Gemini API key

@app.on_message(filters.command(["gemini"]))
async def gemini_handler(client, message):
    await app.send_chat_action(message.chat.id, ChatAction.TYPING)

    # Handle user input
    if message.text.startswith(f"/gemini@{app.username}") and len(message.text.split(" ", 1)) > 1:
        user_input = message.text.split(" ", 1)[1]
    elif message.reply_to_message and message.reply_to_message.text:
        user_input = message.reply_to_message.text
    else:
        if len(message.command) > 1:
            user_input = " ".join(message.command[1:])
        else:
            await message.reply_text("ᴇxᴀᴍᴘʟᴇ :- `/gemini restaurants in New York`")
            return

    if not user_input:
        await message.reply_text("Please provide a valid input.")
        return

    try:
        # Try Google Places API first
        params = {
            "query": user_input,
            "key": GOOGLE_API_KEY,
        }

        response = requests.get(GOOGLE_API_URL, params=params)
        response_data = response.json()
        
        if response_data.get("status") == "REQUEST_DENIED":
            await message.reply_text("Error: Google API access denied. Please check API key permissions.")
            return

        # Check if results are returned from Google API
        if "results" in response_data:
            results = response_data["results"]
            if results:
                result_message = "\n\n".join([f"{place['name']} - {place['formatted_address']}" for place in results[:5]])
                await message.reply_text(result_message, quote=True)
            else:
                await message.reply_text("No results found from Google API.")
        
        # Now try Gemini API if needed
        response = requests.get(GEMINI_API_URL, headers={"Authorization": f"Bearer {GEMINI_API_KEY}"})
        gemini_data = response.json()

        if "error" in gemini_data:
            await message.reply_text("Error: Invalid response from Gemini API.")
        else:
            await message.reply_text("Gemini API data: {}".format(gemini_data))  # Customize based on response

    except requests.exceptions.RequestException as e:
        await message.reply_text(f"Error: {str(e)}. Please try again later.")
