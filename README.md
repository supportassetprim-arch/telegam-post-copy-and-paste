# 🚀 Telegram Multi-Channel Auto Poster 24/7

This is an advanced Telegram Auto Poster bot that flawlessly copies text and media from one or more "Source Channels" and automatically posts them to your "Destination Channel(s)" based on a predefined schedule. It is built to run 24/7 completely free of charge using Render.com and UptimeRobot.

## ✨ Features

- 🔄 **Multi-Channel Support:** Simultaneously copy from multiple source channels and route them to their respective destination channels.
- 🚫 **Restriction Bypass:** Even if a source channel has "Copy/Forwarding Restricted" enabled, the bot will secretly download the media and upload it to your channel as a completely new post.
- 🔗 **Link & Username Filter:** Automatically removes all website links (http, https, www, t.me) and username tags (`@username`) from the copied source text.
- 🛡️ **Anti-Duplicate System:** Saves the last processed message ID in your Telegram "Saved Messages". If the server restarts, it picks up right where it left off, ensuring a post is never duplicated.
- ⏱️ **Smart Schedule (Daily Limit):** Set your desired number of posts per day, and the script will automatically calculate the delay (e.g., every 2.4 hours) between each post.
- 🚀 **First Run Burst:** Instantly copies and posts 10 messages during its very first run (or when reset) before switching to the daily schedule.
- 🌐 **24/7 Live Web Server:** Features a built-in Flask web server that receives pings from UptimeRobot, preventing the Render server from going to sleep.

---

## 🛠️ Deployment Guide

### 🔑 Pre-Step: How to Generate a Telegram Session String (Using Google Colab)
Since this bot acts on behalf of your user account (to bypass forwarding restrictions), it requires a **Session String**. You can easily generate this securely using Google Colab without needing to install anything on your PC.

1. Go to [Google Colab](https://colab.research.google.com/) and create a "New Notebook".
2. Create a new code cell, paste the following Python code, and click the **Run** (Play) button:

```python
!pip install telethon
from telethon.sync import TelegramClient
from telethon.sessions import StringSession

api_id = int(input("Enter API ID: "))
api_hash = input("Enter API Hash: ")

with TelegramClient(StringSession(), api_id, api_hash) as client:
    print("\n--- YOUR SESSION STRING ---")
    print(client.session.save())
    print("---------------------------\n")
    print("⚠️ DO NOT SHARE THIS WITH ANYONE! KEEP IT SECRET!")

```

3. The script will first ask for your `API ID` and `API Hash` (You can get them from [my.telegram.org](https://my.telegram.org)).
4. Next, it will ask for your Telegram phone number (including country code, e.g., `+88017xxxxxxxx`).
5. You will receive a login code in your Telegram app (from the official Telegram service). Enter it in Colab. *(Note: If you have Two-Step Verification enabled, it will ask for your password).*
6. Finally, copy the long text string generated at the bottom. This is your `SESSION_STRING` which you will use in Step 3.

---

### Step 1: Upload Files to GitHub

Make sure you have the following two files in your GitHub repository:

1. `app.py` (The main bot script)
​2. `requirements.txt` (List of dependencies: telethon, flask, etc.)

### Step 2: Deploy to Render.com

1. Go to **Render.com** and create a new **"Web Service"**.
​2. Connect your GitHub repository.
2. **Build Command:** `pip install -r requirements.txt`
3. **Start Command:** `python app.py`

### Step 3: Set Environment Variables

Go to the **Environment Variables** section of your Render Web Service and add the following keys:

| Key | Value (Example) | Details |
| --- | --- | --- |
| `API_ID` | `1234567` | Your API ID from my.telegram.org. |
| `API_HASH` | `a1b2c3d4e5...` | Your API Hash. |
| `SESSION_STRING` | `1Bjw...` | The String Session generated in the Pre-Step via Colab. |
| `CHANNEL_PAIRS` | `@source1:@dest1, @source2:@dest2` | Source and destination channels separated by a colon, pairs separated by commas. |
| `DAILY_LIMIT` | `10` | The maximum number of posts you want to publish per channel per day. |

### Step 4: UptimeRobot (Keep it alive 24/7)

1. Once deployed, copy your Render web URL (e.g., `https://telegam-post-copy-and-paste.onrender.com`).
​2. Go to **UptimeRobot.com** and create a new **HTTP Monitor**.
2. Paste your Render URL and set a **5-minute interval**.
*(That's it! Your bot will now run continuously in the background).*

---

## 💡 Important Tips

* **Reset First Run:** If you want to force the bot to do a "10-post burst" again, go to your Telegram app's **"Saved Messages"**, delete the messages starting with `AutoPoster_State_...`, and hit **"Manual Deploy"** (Restart) on Render.
* **Large Media Files:** Keep in mind that downloading and uploading very large video files might take a bit longer on Render's free tier. It works perfectly and quickly for photos, text, and normal-sized videos.

---

**Developed with ❤️ using Python (Telethon & Flask)**

```

```
