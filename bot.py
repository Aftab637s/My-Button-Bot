from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
import re

# Aapki API Details
api_id = 31492116
api_hash = "be3f66039951f8eebc4c609c66fb17a5"  
bot_token = "8030942691:AAHFe6sZX4-fqjeyuwKvkv7iNvxpd_QIX7Q"  

app = Client("button_adder_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

@app.on_message(filters.command("start"))
async def start(client, message):
    # 1. Pehle "Starting......" bhejega
    msg = await message.reply_text("Starting......")
    await asyncio.sleep(1)  
    
    # 2. Fir emoji bhejega
    await msg.edit_text("✨")
    await asyncio.sleep(1)  
    
    # 3. Final English Menu
    welcome_text = (
        "✨ **Welcome to the Button Adder Bot!** ✨\n\n"
        "I can send messages with stylish inline buttons to your channels.\n\n"
        "**How to use:**\n"
        "`/post @YourChannel Write your message here [Button Name | https://link.com]`\n\n"
        "*(Note: Make sure to promote me as an Admin in your channel!)*"
    )
    await msg.edit_text(welcome_text)

@app.on_message(filters.command("post"))
async def post_message(client, message):
    try:
        # Check if the format is correct
        if len(message.command) < 3:
            await message.reply_text("❌ **Invalid format. Please use:**\n`/post @ChannelUsername Your text [Button Name | https://link.com]`")
            return
            
        # Extract the raw message without '/post' and '@channel'
        raw_text = message.text.split(" ", 2)[2]
        channel_username = message.command[1]
        
        # Regex pattern to find [Button | Link] format
        pattern = r'\[(.*?)\]'
        button_matches = re.findall(pattern, raw_text)
        
        # Remove the button brackets from the text to make it clean
        clean_text = re.sub(pattern, '', raw_text).strip()
        
        # Create Inline Buttons
        keyboard = []
        for match in button_matches:
            if "|" in match:
                btn_name, btn_link = match.split("|", 1)
                keyboard.append([InlineKeyboardButton(btn_name.strip(), url=btn_link.strip())])
                
        reply_markup = InlineKeyboardMarkup(keyboard) if keyboard else None
        
        # Send to the channel
        await client.send_message(
            chat_id=channel_username,
            text=clean_text,
            reply_markup=reply_markup
        )
        await message.reply_text("✅ **Message successfully posted to the channel!**")
        
    except Exception as e:
        await message.reply_text(f"❌ **An error occurred:**\n`{e}`\n\n*(Make sure the bot is an Admin in the channel!)*")

print("Button Adder Bot is running! ✨")
app.run()
