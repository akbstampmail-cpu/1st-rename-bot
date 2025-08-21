from pyrogram import Client, filters
import os 

API_ID = 24856401
API_HASH = "63c6e57119836813a65282cdc685ec40"
BOT_TOKEN = "8358484108:AAGuktgQh2QDWPHxGFriMGP6O67ZlbLj124" 

app = Client("rename-bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN) 

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply("👋 Hello! Mujhe koi file bhejo aur us file par reply karke likho:\n\n`/rename NewFileName.ext`") 

@app.on_message(filters.command("rename"))
async def rename_file(client, message):
    if not message.reply_to_message:
        await message.reply("❌ Pehle kisi file par reply karo!")
        return 

    file_message = message.reply_to_message 

    if not file_message.document:
        await message.reply("❌ Sirf documents supported hain!")
        return 

    # New name extract
    args = message.text.split(" ", 1)
    if len(args) < 2:
        await message.reply("❌ Naya naam bhi likhna padega! Example: /rename newfile.pdf")
        return
    new_name = args[1] 

    # Download aur rename
    file_path = await file_message.download()
    new_path = new_name 

    os.rename(file_path, new_path) 

    # Send renamed file
    await message.reply_document(document=new_path, caption=f"✅ File renamed to: {new_name}") 

    # Local file delete
    os.remove(new_path) 

app.run()