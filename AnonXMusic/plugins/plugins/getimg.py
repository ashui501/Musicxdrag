import requests
from pyrogram import filters
from pyrogram.enums import ChatAction
from AnonXMusic import app

# Getimg API key (replace with your actual key)
GETIMG_API_KEY = "key-ICLT6PNtwcDA5PKI7DmuKMXrueoKcDybWuHrXX1o9V8eszHCAOabBpvq2d7ZWewTa5A50ntiXEkDcMo1ewE5exp6LxuOAAr"
GETIMG_API_URL = "https://api.getimg.ai/v1/generate"

# Function to generate an image using Getimg API
def generate_image(prompt):
    headers = {
        "Authorization": f"Bearer {GETIMG_API_KEY}",
        "Content-Type": "application/json"
    }

    # Request payload to send to Getimg API
    data = {
        "prompt": prompt,
        "style": "artistic",  # You can change the style based on the available options
        "width": 512,
        "height": 512
    }

    # Make the API request
    response = requests.post(GETIMG_API_URL, json=data, headers=headers)

    if response.status_code == 200:
        # Extract image URL from the response
        image_url = response.json().get("image_url")
        return image_url
    else:
        return None

# Command handler to generate an image
@app.on_message(filters.command("generate_image"))
async def generate_image_handler(client, message):
    chat_id = message.chat.id
    await app.send_chat_action(chat_id, ChatAction.TYPING)

    # Get the prompt from the user input
    if len(message.command) > 1:
        prompt = " ".join(message.command[1:])
    else:
        await message.reply_text("Usage: /generate_image <your prompt>")
        return

    try:
        # Call the function to generate the image via Getimg API
        image_url = generate_image(prompt)

        if image_url:
            # Send the generated image URL back to the user
            await message.reply_photo(photo=image_url, caption=f"Generated image for prompt: {prompt}")
        else:
            await message.reply_text("Sorry, I couldn't generate the image. Please try again later.")
    except Exception as e:
        await message.reply_text(f"Error: {str(e)}. Please try again later.")

