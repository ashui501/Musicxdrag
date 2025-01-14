import openai
from pyrogram import filters
from pyrogram.enums import ChatAction
from AnonXMusic import app

# Set your OpenAI API key
openai.api_key = "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"

@app.on_message(filters.command(["chatgpt"]))
async def chatgpt_handler(client, message):
    await app.send_chat_action(message.chat.id, ChatAction.TYPING)

    # Handle user input
    if (
        message.text.startswith(f"/chatgpt@{app.username}")
        and len(message.text.split(" ", 1)) > 1
    ):
        user_input = message.text.split(" ", 1)[1]
    elif message.reply_to_message and message.reply_to_message.text:
        user_input = message.reply_to_message.text
    else:
        if len(message.command) > 1:
            user_input = " ".join(message.command[1:])
        else:
            await message.reply_text("Example usage: `/chatgpt How does AI work?`")
            return

    if not user_input:
        await message.reply_text("Please provide a valid input.")
        return

    try:
        # Call the OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Use "gpt-4" for GPT-4 if available
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_input}
            ]
        )
        reply = response["choices"][0]["message"]["content"].strip()
        
@app.on_message(filters.command(["reset"]))
async def reset_handler(client, message):
    user_id = message.from_user.id
    if user_id in user_conversations:
        user_conversations.pop(user_id)
    await message.reply_text("**» Conversation context has been reset.**")

@app.on_message(filters.command(["setrole"]))
async def set_role_handler(client, message):
    user_id = message.from_user.id
    if len(message.command) > 1:
        role_content = " ".join(message.command[1:])
        user_conversations[user_id] = [
            {"role": "system", "content": role_content}
        ]
        await message.reply_text(f"**» System role set to:** `{role_content}`")
    else:
        await message.reply_text("**» Example usage:** `/setrole You are a friendly AI.`")

        await message.reply_text(reply, quote=True)
    except Exception as e:
        await message.reply_text(f"Error: {str(e)}. Please try again later.")
