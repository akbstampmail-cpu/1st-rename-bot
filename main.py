import os
import threading
import asyncio
from flask import Flask
from pyrogram import Client, filters

# ---------- Config from Environment ----------
API_ID = int(os.getenv("API_ID", "0"))
API_HASH = os.getenv("API_HASH", "")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")

# ---------- Flask (dummy web) ----------
web = Flask(__name__)

@web.route("/")
def home():
    return "✅ Telegram Rename Bot is running."

def run_flask():
    port = int(os.getenv("PORT", "5000"))  # Render provides PORT env
    web.run(host="0.0.0.0", port=port)

# ---------- Pyrogram Bot ----------
bot = Client(
    "rename-bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

@bot.on_message(filters.command("start"))
async def start_cmd(client, message):
    await message.reply(
        "👋 Hello!\n\nMujhe koi **document** bhejo aur us file par reply karke likho:\n"
        "`/rename NewFileName.ext`"
    )

@bot.on_message(filters.command("rename"))
async def rename_file(client, message):
    # Must reply to a document
    if not message.reply_to_message:
        await message.reply("❌ Pehle kisi document par reply karo!")
        return

    file_msg = message.reply_to_message
    if not file_msg.document:
        await message.reply("❌ Abhi sirf documents supported hain.")
        return

    # Get new name
    parts = message.text.split(" ", 1)
    if len(parts) < 2 or not parts[1].strip():
        await message.reply("❌ Example: `/rename newfile.pdf`")
        return
    new_name = parts[1].strip()

    # Download → rename → send → cleanup
    try:
        temp_path = await file_msg.download()                   # e.g. /opt/render/project/src/...
        new_path = os.path.join(os.getcwd(), new_name)          # put in current dir
        os.rename(temp_path, new_path)

        await message.reply_document(new_path, caption=f"✅ Renamed to **{new_name}**")

        await asyncio.sleep(2)  # give time to send
        if os.path.exists(new_path):
            os.remove(new_path)
    except Exception as e:
        await message.reply(f"⚠️ Error: `{e}`")

def run_bot():
    bot.run()

if __name__ == "__main__":
    # Flask (for Render free Web Service) + Bot parallel
    threading.Thread(target=run_flask, daemon=True).start()
    run_bot()