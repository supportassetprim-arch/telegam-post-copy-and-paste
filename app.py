import os
import asyncio
import threading
from flask import Flask
from telethon.sync import TelegramClient
from telethon.sessions import StringSession

# ==========================================
# 1. FLASK WEB SERVER (UptimeRobot er jonno)
# ==========================================
app = Flask(__name__)

@app.route('/')
def home():
    return "🚀 Telegram Auto Poster is Running 24/7!"

def run_flask():
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)

# ==========================================
# 2. TELEGRAM BOT LOGIC
# ==========================================
API_ID = int(os.environ.get('API_ID', 0))
API_HASH = os.environ.get('API_HASH', '')
SESSION_STRING = os.environ.get('SESSION_STRING', '')

SOURCE_CHANNEL = os.environ.get('SOURCE_CHANNEL', '')
DEST_CHANNEL = os.environ.get('DEST_CHANNEL', '')
DAILY_LIMIT = int(os.environ.get('DAILY_LIMIT', 10))

async def telegram_bot():
    if API_ID == 0 or not API_HASH or not SESSION_STRING:
        print("❌ Environment variables thik moto set kora nei!")
        return

    client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)
    await client.start()
    print("✅ Telegram Logged in Successfully!")

    delay_seconds = 86400 / DAILY_LIMIT
    print(f"📊 Daily Limit: {DAILY_LIMIT} Posts")
    print(f"⏳ Normal gap between posts: {delay_seconds / 3600:.2f} Ghonta")

    last_msg_id = 0
    is_first_run = True  # Prothom run check korar jonnno

    while True:
        try:
            # Prothom run e shudhu 2 ta post nibe, pore 5 ta kore check korbe
            limit_count = 2 if is_first_run else 5
            messages = await client.get_messages(SOURCE_CHANNEL, limit=limit_count)
            
            for msg in reversed(messages):
                if msg.id > last_msg_id:
                    
                    if msg.text or msg.media:
                        print(f"🔄 Processing message ID: {msg.id}")
                        
                        # jodi Media thake, tahole download kore upload korbe (Restrict bypass)
                        if msg.media:
                            print("📥 Downloading media (Bypassing restriction)...")
                            file_path = await client.download_media(msg)
                            await client.send_message(DEST_CHANNEL, msg.text or "", file=file_path)
                            os.remove(file_path) # Upload er por delete kore dibe server theke
                        else:
                            # Shudhu text thakle normally text post korbe
                            await client.send_message(DEST_CHANNEL, msg.text)
                            
                        print(f"✅ Success: Message ID {msg.id} posted!")
                        last_msg_id = msg.id
                        
                        # Delay logic
                        if is_first_run:
                            # Prothom bar 2 ta post er majhe 3 second gap dibe
                            await asyncio.sleep(3)
                        else:
                            # Normal routine e ghumiye jabe
                            print(f"💤 Waiting {delay_seconds / 3600:.2f} hours for the next post...")
                            await asyncio.sleep(delay_seconds)
            
            # Prothom run sesh hole, schedule onujayi wait kora shuru korbe
            if is_first_run:
                is_first_run = False
                print("\n🎉 First run complete! 2 ta post hoyeche. Ebar theke schedule onujayi post hobe.\n")
                await asyncio.sleep(delay_seconds)
            else:
                # Kono notun post na thakle 5 min pore abar check korbe
                await asyncio.sleep(300)

        except Exception as e:
            print(f"❌ Error occurred: {e}")
            await asyncio.sleep(60)

# ==========================================
# 3. SCRIPT START
# ==========================================
if __name__ == '__main__':
    threading.Thread(target=run_flask, daemon=True).start()
    try:
        asyncio.run(telegram_bot())
    except KeyboardInterrupt:
        print("Bot stopped.")
