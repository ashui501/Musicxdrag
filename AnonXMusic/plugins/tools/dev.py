import os
import re
import subprocess
import sys
import traceback
from inspect import getfullargspec
from io import StringIO
from time import time

from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery

from AnonXMusic import app
from config import OWNER_ID


async def aexec(code, client, message):
    exec(
        "async def __aexec(client, message): "
        + "".join(f"\n {a}" for a in code.split("\n"))
    )
    return await locals()["__aexec"](client, message)


async def edit_or_reply(msg: Message, **kwargs):
    func = msg.edit_text if msg.from_user.is_self else msg.reply
    await func(**kwargs)


@app.on_message(filters.text & filters.user(OWNER_ID) & ~filters.forwarded & ~filters.via_bot)
async def executor(client: app, message: Message):
    """Executes Python or shell commands based on plain text input."""
    if not message.text:
        return  # Prevent errors when message.text is None

    if message.text.startswith("eval"):
        if len(message.text.split()) < 2:
            return await edit_or_reply(message, text="<b>ᴡʜᴀᴛ ʏᴏᴜ ᴡᴀɴɴᴀ ᴇxᴇᴄᴜᴛᴇ ʙᴀʙʏ ?</b>")
        
        cmd = message.text.split(" ", maxsplit=1)[1]
        t1 = time()
        old_stderr, old_stdout = sys.stderr, sys.stdout
        redirected_output = sys.stdout = StringIO()
        redirected_error = sys.stderr = StringIO()
        stdout, stderr, exc = None, None, None
        
        try:
            await aexec(cmd, client, message)
        except Exception:
            exc = traceback.format_exc()
        
        stdout, stderr = redirected_output.getvalue(), redirected_error.getvalue()
        sys.stdout, sys.stderr = old_stdout, old_stderr
        
        evaluation = exc or stderr or stdout or "Success"
        final_output = f"<b>⥤ ʀᴇsᴜʟᴛ :</b>\n<pre language='python'>{evaluation}</pre>"
        
        t2 = time()
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(f"Runtime: {round(t2-t1, 3)}s", callback_data=f"runtime {round(t2-t1, 3)}"),
                    InlineKeyboardButton(" Close", callback_data=f"close|{message.from_user.id}"),
                ]
            ]
        )

        await edit_or_reply(message, text=final_output, reply_markup=keyboard)

    elif message.text.startswith("sh"):
        """Executes shell commands."""
        if len(message.text.split()) < 2:
            return await edit_or_reply(message, text="<b>ᴇxᴀᴍᴩʟᴇ :</b>\nsh git pull")
        
        text = message.text.split(None, 1)[1]
        shell = re.split(r""" (?=(?:[^'"]|'[^']*'|"[^"]*")*$)""", text)
        
        try:
            t1 = time()  # Ensure t1 is defined before usage
            process = subprocess.Popen(shell, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output = process.stdout.read().decode("utf-8").strip() or "None"
        except Exception as err:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            errors = traceback.format_exception(etype=exc_type, value=exc_obj, tb=exc_tb)
            return await edit_or_reply(message, text=f"<b>ERROR :</b>\n<pre>{''.join(errors)}</pre>")
        
        t2 = time()
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(f"Runtime: {round(t2-t1, 3)}s", callback_data=f"runtime {round(t2-t1, 3)}"),
                    InlineKeyboardButton(" Close", callback_data=f"close|{message.from_user.id}"),
                ]
            ]
        )

        await edit_or_reply(message, text=f"<b>OUTPUT :</b>\n<pre>{output}</pre>", reply_markup=keyboard)

    await message.stop_propagation()


@app.on_callback_query(filters.regex(r"runtime"))
async def runtime_func_cq(_, cq):
    runtime = cq.data.split(None, 1)[1]
    await cq.answer(runtime, show_alert=True)


@app.on_callback_query(filters.regex(r"close\|"))
async def close_command(_, CallbackQuery: CallbackQuery):
    user_id = int(CallbackQuery.data.split("|")[1])
    if CallbackQuery.from_user.id != user_id:
        return await CallbackQuery.answer(" You can't close this!", show_alert=True)
    
    await CallbackQuery.message.delete()
    await CallbackQuery.answer()
