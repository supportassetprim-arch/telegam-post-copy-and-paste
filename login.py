import os
import asyncio
from telethon.sync import TelegramClient
from telethon.sessions import StringSession

# Render-er environment theke API data nibe, na pele input chaibe
env_api_id = os.environ.get('API_ID')
env_api_hash = os.environ.get('API_HASH')

async def main():
    print("\n🚀 === Render Telegram Login System === 🚀\n")
    
    try:
        api_id = int(env_api_id) if env_api_id else int(input("Enter API ID: ").strip())
        api_hash = env_api_hash if env_api_hash else input("Enter API HASH: ").strip()

        print("\n⏳ Telegram er sathe connect kora hochche...")
        client = TelegramClient(StringSession(), api_id, api_hash)
        
        # Ekhane login process shuru hobe (Number ar OTP chaibe)
        await client.start()
        
        print("\n✅ Login Successful! Apnar Notun Session String Niche Deya Holo:\n")
        print("========================================================================")
        print(client.session.save())
        print("========================================================================")
        print("\n👆 Upore deya string-ti copy korun ebong Render-er Environment Variables-e")
        print("'SESSION_STRING' er ghore paste kore Save din.\n")
        
    except Exception as e:
        print(f"\n❌ Ekta somossa hoyeche: {e}")

if __name__ == '__main__':
    asyncio.run(main())
