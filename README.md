# 🚀 Telegram Multi-Channel Auto Poster 24/7

This is an advanced Telegram Auto Poster bot that flawlessly copies text and media from one or more "Source Channels" and automatically posts them to your "Destination Channel(s)" based on a predefined schedule. It is built to run 24/7 completely free of charge using Render.com and UptimeRobot.

## ✨ Features

* 🔄 **Multi-Channel Support:** Simultaneously copy from multiple source channels and route them to their respective destination channels.
* 🚫 **Restriction Bypass:** Even if a source channel has "Copy/Forwarding Restricted" enabled, the bot will secretly download the media and upload it to your channel as a completely new post.
* 🔗 **Link & Username Filter:** Automatically removes all website links (http, https, www, t.me) and username tags (`@username`) from the copied source text.
* 🛡️ **Anti-Duplicate System:** Saves the last processed message ID in your Telegram "Saved Messages". If the server restarts, it picks up right where it left off, ensuring a post is never duplicated.
* ⏱️ **Smart Schedule (Daily Limit):** Set your desired number of posts per day, and the script will automatically calculate the delay (e.g., every 2.4 hours) between each post.
* 🚀 **First Run Burst:** Instantly copies and posts 10 messages during its very first run (or when reset) before switching to the daily schedule.
* 🌐 **24/7 Live Web Server:** Features a built-in Flask web server that receives pings from UptimeRobot, preventing the Render server from going to sleep.

---

## 🛠️ Deployment Guide

### Step 1: Upload Files to GitHub
Make sure you have the following two files in your GitHub repository:
1. `app.py` (The main bot script)
2. `requirements.txt` (List of dependencies: telethon, flask, etc.)

### Step 2: Deploy to Render.com
1. Go to **Render.com** and create a new **"Web Service"**.
2. Connect your GitHub repository.
3. **Build Command:** `pip install -r requirements.txt`
4. **Start Command:** `python app.py`

### Step 3: Set Environment Variables
Go to the **Environment Variables** section of your Render Web Service and add the following keys:

| Key | Value (Example) | Details |
| :--- | :--- | :--- |
| `API_ID` | `1234567` | Your API ID from my.telegram.org. |
| `API_HASH` | `a1b2c3d4e5...` | Your API Hash. |
| `SESSION_STRING` | `1Bjw...` | The String Session generated locally or on Colab. |
| `CHANNEL_PAIRS` | `@source1:@dest1, @source2:@dest2` | Source and destination channels separated by a colon, pairs separated by commas. |
| `DAILY_LIMIT` | `10` | The maximum number of posts you want to publish per channel per day. |

### Step 4: UptimeRobot (Keep it alive 24/7)
1. Once deployed, copy your Render web URL (e.g., `https://telegam-post-copy-and-paste.onrender.com`).
2. Go to **UptimeRobot.com** and create a new **HTTP Monitor**.
3. Paste your Render URL and set a **5-minute interval**. 
*(That's it! Your bot will now run continuously in the background).*

---

## 💡 Important Tips

* **Reset First Run:** If you want to force the bot to do a "10-post burst" again, go to your Telegram app's **"Saved Messages"**, delete the messages starting with `AutoPoster_State_...`, and hit **"Manual Deploy"** (Restart) on Render.
* **Large Media Files:** Keep in mind that downloading and uploading very large video files might take a bit longer on Render's free tier. It works perfectly and quickly for photos, text, and normal-sized videos.

---
**Developed with ❤️ using Python (Telethon & Flask)**
