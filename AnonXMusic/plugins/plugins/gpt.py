import openai
from pyrogram import filters
from pyrogram.enums import ChatAction
from pyrogram.errors import UserNotParticipant
from AnonXMusic import app

# Set your OpenAI API key
openai.api_key = "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"

# The group username
GROUP_USERNAME = "@dragabackup"

@app.on_message(filters.command(["chatgpt"]))
async def chatgpt_handler(client, message):
    await app.send_chat_action(message.chat.id, ChatAction.TYPING)

    # Check if the user is a member of the group
    try:
        # Fetch chat member status
        member = await app.get_chat_member(GROUP_USERNAME, message.from_user.id)
        
        # Check if the user is a member, admin, or creator
        if member.status not in ["member", "administrator", "creator"]:
            await message.reply_text("You need to join the group @dragabackup to use ChatGPT.")
            return
    except UserNotParticipant:
        # If the user is not a participant
        await message.reply_text("You need to join the group @dragabackup to use ChatGPT.")
        return

    # Handle user input for ChatGPT
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

        await message.reply_text(reply, quote=True)
    except Exception as e:
        await message.reply_text(f"Error: {str(e)}. Please try again later.")
