from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import re

# Aapki API Details
api_id = 31492116
api_hash = "be3f66039951f8eebc4c609c66fb17a5"  
bot_token = "8030942691:AAHFe6sZX4-fqjeyuwKvkv7iNvxpd_QIX7Q"  

app = Client("button_adder_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text(
        "✨ **Button Adder Bot mein aapka swagat hai!** ✨\n\n"
        "Main aapke channels mein stylish buttons wale messages bhej sakta hoon.\n\n"
        "**Use karne ka tarika:**\n"
        "`/post @AapkaChannel Pura message yahan likhein [Button Name | https://link.com]`\n\n"
        "*(Note: Mujhe apne channel mein Admin zaroor banayein!)*"
    )

@app.on_message(filters.command("post"))
async def post_message(client, message):
    try:
        if len(message.command) < 3:
            await message.reply_text("❌ **Sahi format use karein:**\n`/post @ChannelUsername Aapka text [Button Name | https://link.com]`")
            return
            
        raw_text = message.text.split(" ", 2)[2]
        channel_username = message.command[1]
        
        pattern = r'\[(.*?)\]'
        button_matches = re.findall(pattern, raw_text)
        
        clean_text = re.sub(pattern, '', raw_text).strip()
        
        keyboard = []
        for match in button_matches:
            if "|" in match:
                btn_name, btn_link = match.split("|", 1)
                keyboard.append([InlineKeyboardButton(btn_name.strip(), url=btn_link.strip())])
                
        reply_markup = InlineKeyboardMarkup(keyboard) if keyboard else None
        
        await client.send_message(
            chat_id=channel_username,
            text=clean_text,
            reply_markup=reply_markup
        )
        await message.reply_text("✅ **Message successfully channel mein bhej diya gaya hai!**")
        
    except Exception as e:
        await message.reply_text(f"❌ **Error aa gaya:**\n`{e}`\n\n*(Dhyan rahe ki bot aapke channel mein Admin hona chahiye!)*")

print("Button Adder Bot is running! ✨")
app.run()
