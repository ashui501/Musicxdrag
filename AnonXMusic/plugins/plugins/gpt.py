import openai
from pyrogram import filters
from pyrogram.enums import ChatAction
from AnonXMusic import app

# Set your OpenAI API key
openai.api_key = "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"
# To store conversations (per user basis, using a dictionary for simplicity)
user_conversations = {}

@app.on_message(filters.command(["chatgpt", "gpt", "ask"]))  # Add support for "gpt"
async def ask_handler(client, message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    # Indicate typing action
    await app.send_chat_action(chat_id, ChatAction.TYPING)

    # Retrieve the user's input
    if len(message.command) > 1:
        user_input = " ".join(message.command[1:])
    elif message.reply_to_message and message.reply_to_message.text:
        user_input = message.reply_to_message.text
    else:
        await message.reply_text("Exᴀᴍᴘʟᴇ ᴜsᴀɢᴇ: /ᴄʜᴀᴛɢᴘᴛ Hᴏᴡ ᴅᴏᴇs ʀᴇᴄᴜʀsɪᴏɴ ᴡᴏʀᴋ?")
        return

    # Initialize the conversation history if it's a new user
    if user_id not in user_conversations:
        user_conversations[user_id] = [
            {"role": "system", "content": "You are a helpful assistant who can answer any questions."}
        ]

    # Append the user's input to the conversation
    user_conversations[user_id].append({"role": "user", "content": user_input})

    try:
        # Call the OpenAI API with the full conversation history
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Use "gpt-4" if needed
            messages=user_conversations[user_id]
        )

        # Get the assistant's response
        assistant_response = response["choices"][0]["message"]["content"].strip()

        # Append the assistant's response to the conversation history
        user_conversations[user_id].append({"role": "assistant", "content": assistant_response})

        # Send the assistant's response to the user
        await message.reply_text(assistant_response, quote=True)

    except Exception as e:
        await message.reply_text(f"**» Error:** {str(e)}. Please try again later.")

@app.on_message(filters.command(["reset"]))
async def reset_handler(client, message):
    user_id = message.from_user.id
    if user_id in user_conversations:
        user_conversations.pop(user_id)
    await message.reply_text("Cᴏɴᴠᴇʀsᴀᴛɪᴏɴ ᴄᴏɴᴛᴇxᴛ ʜᴀs ʙᴇᴇɴ ʀᴇsᴇᴛ.")

@app.on_message(filters.command(["setrole"]))
async def set_role_handler(client, message):
    user_id = message.from_user.id
    if len(message.command) > 1:
        role_content = " ".join(message.command[1:])
        user_conversations[user_id] = [
            {"role": "system", "content": role_content}
        ]
        await message.reply_text(f"Sʏsᴛᴇᴍ ʀᴏʟᴇ sᴇᴛ ᴛᴏ: {role_content}")
    else:
        await message.reply_text("Exᴀᴍᴘʟᴇ ᴜsᴀɢᴇ: /sᴇᴛʀᴏʟᴇ Yᴏᴜ ᴀʀᴇ ᴀ ғʀɪᴇɴᴅʟʏ AI.")

@app.on_message(filters.command(["generate_image", "image"]))
async def generate_image_handler(client, message):
    chat_id = message.chat.id

    # Indicate typing action
    await app.send_chat_action(chat_id, ChatAction.UPLOAD_PHOTO)

    # Retrieve the user's input
    if len(message.command) > 1:
        prompt = " ".join(message.command[1:])
    else:
        await message.reply_text("Exᴀᴍᴘʟᴇ ᴜsᴀɢᴇ: /ɢᴇɴᴇʀᴀᴛᴇ_ɪᴍᴀɢᴇ A ғʟᴏᴀᴛɪɴɢ ᴄɪᴛʏ ɪɴ ᴛʜᴇ ᴄʟᴏᴜᴅs.")
        return

    try:
        # Call the OpenAI API to generate the image
        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size="1024x1024"
        )

        # Get the image URL
        image_url = response["data"][0]["url"]

        # Send the image URL as a message
        await message.reply_photo(photo=image_url, caption=f"Image Prompt: {prompt}")

    except Exception as e:
        await message.reply_text(f"» Error: {str(e)}. Please try again later.")
