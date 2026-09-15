import os
import asyncio
import threading
import re  # Notun library add kora hoyeche text clean korar jonno
from flask import Flask
from telethon.sync import TelegramClient
from telethon.sessions import StringSession

# ==========================================
# 1. FLASK WEB SERVER
# ==========================================
app = Flask(__name__)

@app.route('/')
def home():
    return "🚀 Telegram Multi-Channel Auto Poster is Running 24/7 (Link Filter Enabled)!"

def run_flask():
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)

# ==========================================
# 2. TEXT CLEANER FUNCTION
# ==========================================
def clean_message_text(text):
    if not text:
        return ""
    # 1. Shob dhoroner Link/URL muche felbe (http, https, www, t.me)
    text = re.sub(r'https?://\S+|www\.\S+|t\.me/\S+', '', text)
    # 2. @ diye shuru howa username muche felbe
    text = re.sub(r'@\w+', '', text)
    # 3. Faka line ba extra space gulo thik korbe
    text = re.sub(r'\n\s*\n', '\n', text).strip()
    return text

# ==========================================
# 3. TELEGRAM BOT LOGIC
# ==========================================
API_ID = int(os.environ.get('API_ID', 0))
API_HASH = os.environ.get('API_HASH', '')
SESSION_STRING = os.environ.get('SESSION_STRING', '')
CHANNEL_PAIRS = os.environ.get('CHANNEL_PAIRS', '')
DAILY_LIMIT = int(os.environ.get('DAILY_LIMIT', 10))

async def channel_worker(client, source, dest, delay_seconds, state_msg_id, last_msg_id):
    is_first_run = (last_msg_id == 0)
    await asyncio.sleep(2) 

    while True:
        try:
            limit_count = 10 if is_first_run else 5
            messages = await client.get_messages(source, limit=limit_count)
            
            for msg in reversed(messages):
                if msg.id > last_msg_id:
                    
                    if msg.text or msg.media:
                        print(f"[{source} ➡️ {dest}] 🔄 Processing MSG ID: {msg.id}")
                        
                        # Text filter kora hochche (Link o Username bad deya)
                        cleaned_text = clean_message_text(msg.text)
                        
                        # Jodi shob link katar por text ektuo na thake, kintu chobi/video thake
                        if msg.media:
                            print(f"[{source}] 📥 Downloading media...")
                            file_path = await client.download_media(msg)
                            await client.send_message(dest, cleaned_text, file=file_path)
                            os.remove(file_path)
                            print(f"[{source} ➡️ {dest}] ✅ Success: Media Posted!")
                        else:
                            # Shudhu text thakle obossoi text thakte hobe (empty message pathano jay na)
                            if cleaned_text:
                                await client.send_message(dest, cleaned_text)
                                print(f"[{source} ➡️ {dest}] ✅ Success: Text Posted!")
                            else:
                                print(f"[{source} ➡️ {dest}] ⚠️ Skipped: Link/Username katar por kono text chilo na.")
                        
                        last_msg_id = msg.id
                        
                        state_text = f"AutoPoster_State_{source}: {last_msg_id}"
                        if state_msg_id:
                            await client.edit_message('me', state_msg_id, state_text)
                        else:
                            state_msg = await client.send_message('me', state_text)
                            state_msg_id = state_msg.id
                        
                        if is_first_run:
                            await asyncio.sleep(3)
                        else:
                            print(f"[{source}] 💤 Waiting {delay_seconds / 3600:.2f} hours for next post...")
                            await asyncio.sleep(delay_seconds)
            
            if is_first_run:
                is_first_run = False
                print(f"\n🎉 [{source}] First run complete!\n")
                await asyncio.sleep(delay_seconds)
            else:
                await asyncio.sleep(300)

        except Exception as e:
            print(f"❌ [{source}] Error: {e}")
            await asyncio.sleep(60)

async def telegram_bot():
    if API_ID == 0 or not API_HASH or not SESSION_STRING or not CHANNEL_PAIRS:
        print("❌ Environment variables thik moto set kora nei!")
        return

    client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)
    await client.start()
    print("✅ Telegram Logged in Successfully!")

    pairs = []
    for pair in CHANNEL_PAIRS.split(','):
        if ':' in pair:
            src, dst = pair.split(':', 1)
            pairs.append((src.strip(), dst.strip()))
            
    if not pairs:
        print("❌ Kono valid CHANNEL_PAIRS paowa jayni!")
        return

    delay_seconds = 86400 / DAILY_LIMIT
    print(f"📊 Daily Limit: {DAILY_LIMIT} Posts per channel")

    print("🔍 Checking Saved Messages for last states...")
    saved_states = {}
    async for msg in client.iter_messages('me', search='AutoPoster_State_'):
        try:
            parts = msg.text.split(':')
            if len(parts) == 2:
                header = parts[0].strip()
                src_name = header.replace('AutoPoster_State_', '')
                l_id = int(parts[1].strip())
                saved_states[src_name] = {'last_id': l_id, 'msg_id': msg.id}
        except:
            pass

    tasks = []
    for source, dest in pairs:
        state = saved_states.get(source, {'last_id': 0, 'msg_id': None})
        task = asyncio.create_task(
            channel_worker(client, source, dest, delay_seconds, state['msg_id'], state['last_id'])
        )
        tasks.append(task)
    
    await asyncio.gather(*tasks)

# ==========================================
# 4. SCRIPT START
# ==========================================
if __name__ == '__main__':
    threading.Thread(target=run_flask, daemon=True).start()
    try:
        asyncio.run(telegram_bot())
    except KeyboardInterrupt:
        print("Bot stopped.")
