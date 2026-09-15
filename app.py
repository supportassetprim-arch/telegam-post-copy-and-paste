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
    # Eta apnar frontend e dekhabe
    return """
    <html>
        <head><title>Telegram Auto Poster</title></head>
        <body style="font-family: Arial; text-align: center; margin-top: 50px;">
            <h1 style="color: #0088cc;">🚀 Telegram Auto Poster is Running 24/7!</h1>
            <p>UptimeRobot is keeping this service alive.</p>
        </body>
    </html>
    """

def run_flask():
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)


# ==========================================
# 2. TELEGRAM BOT LOGIC
# ==========================================
# Environment Variables theke data nibe (Render e set korte hobe)
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

    # StringSession er fole bot kokhono logout hobe na
    client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)
    await client.start()
    print("✅ Telegram Logged in Successfully!")

    # 24 ghontake limit diye vag kore wait time ber kora (seconds e)
    delay_seconds = 86400 / DAILY_LIMIT
    print(f"📊 Daily Limit: {DAILY_LIMIT} Posts")
    print(f"⏳ Proti post er majhe gap: {delay_seconds / 3600:.2f} Ghonta")

    last_msg_id = 0

    while True:
        try:
            # Source channel theke message fetch kora
            messages = await client.get_messages(SOURCE_CHANNEL, limit=5)
            
            # Notun theke purano ulte (reverse) nibe jate serial thik thake
            for msg in reversed(messages):
                if msg.id > last_msg_id:
                    # Message ti copy kore pathabe (Forwarded tag asbe na)
                    if msg.text or msg.media:
                        await client.send_message(DEST_CHANNEL, msg.text, file=msg.media)
                        print(f"✅ Success: Notun message post hoyeche! (Msg ID: {msg.id})")
                        last_msg_id = msg.id
                        
                        # Ekta post korar por hisab onujayi ghumiye thakbe (Schedule)
                        print(f"💤 Waiting {delay_seconds / 3600:.2f} hours for the next post...")
                        await asyncio.sleep(delay_seconds)
            
            # Jodi copy korar moto notun kichu na thake, 5 minute por abar check korbe
            await asyncio.sleep(300)

        except Exception as e:
            print(f"❌ Error occurred: {e}")
            await asyncio.sleep(60) # Error hole 1 minute wait kore abar try korbe

# ==========================================
# 3. SCRIPT START KORAR LOGIC
# ==========================================
if __name__ == '__main__':
    # 1. Flask server ke background thread e start kora
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    
    # 2. Telegram bot ke main asycnio loop e run kora
    # asyncio.run() use kora hoyeche jate asynchronas kaj gulo thik vabe chole
    try:
        asyncio.run(telegram_bot())
    except KeyboardInterrupt:
        print("Bot stopped by user.")
