# 🚀 Telegram Multi-Channel Auto Poster 24/7

Eta ekta advanced Telegram Auto Poster bot, jeta ek ba ekadhik "Source Channel" theke text ebong media hoboho copy kore apnar "Destination Channel"-e schedule onujayi auto-post kore. Eti Render.com ebong UptimeRobot babohar kore 24 ghonta (24/7) completely free-te cholar jonno toiri kora hoyeche.

## ✨ Features (Ki ki thakche)

* 🔄 **Multi-Channel Support:** Eksathe onek gulo channel theke copy kore onno onno channel-e post korar subidha.
* 🚫 **Restriction Bypass:** Source channel-e "Copy/Forward Restricted" thakleo eti media download kore apnar channel-e completely notun post hisabe upload korbe.
* 🔗 **Link & Username Filter:** Source post theke shob dhoroner website link (http, t.me) ebong username tag (`@username`) automatically muche felbe.
* 🛡️ **Anti-Duplicate System:** Server kono karone restart nileo apnar Telegram-er "Saved Messages"-e ID save thakar karone ekoi post 2 bar kokhonoi hobe na.
* ⏱️ **Smart Schedule (Daily Limit):** Dine koyta post hobe ta set kore dile, script auto time calculate kore (e.g., 2.4 ghonta por por) post korbe.
* 🚀 **First Run Burst:** Prothom bar chalu hole ba reset korle aksathe 10 ti post copy korbe.
* 🌐 **24/7 Live Web Server:** Flask web server deya ache jeta UptimeRobot theke ping receive kore Render ke ghumate dey na.

---

## 🛠️ Deployment Guide (Kivabe Setup Korben)

### Step 1: GitHub-e Files Upload
Apnar GitHub repository-te obosshoi ei duti file thakte hobe:
1. `app.py` (Main bot code)
2. `requirements.txt` (telethon, flask etc. library-r nam)

### Step 2: Render.com e Deploy
1. **Render.com**-e giye notun ekta **"Web Service"** toiri korun.
2. Apnar GitHub repository connect korun.
3. Build Command: `pip install -r requirements.txt`
4. Start Command: `python app.py`

### Step 3: Environment Variables Set Kora
Render-er **Environment Variables** section-e giye nicher Key gulo add korun:

| Key | Value (Example) | Details |
| :--- | :--- | :--- |
| `API_ID` | `1234567` | Apnar my.telegram.org theke pawa API ID. |
| `API_HASH` | `a1b2c3d4e5...` | Apnar API Hash. |
| `SESSION_STRING` | `1Bjw...` | Local PC ba Colab theke generate kora String Session. |
| `CHANNEL_PAIRS` | `@source1:@dest1, @source2:@dest2` | Source ebong target channel-er nam (comma diye ekadhik add kora jabe). |
| `DAILY_LIMIT` | `10` | Proti channel-e dine koyta post hobe tar limit. |

### Step 4: UptimeRobot (24/7 Live)
1. Deploy hoye gele Render theke ekta URL paben (jemon: `https://telegam-post-copy-and-paste.onrender.com`).
2. **UptimeRobot.com** e giye ekta HTTP Monitor toiri korun.
3. Render-er link-ti diye 5 minute-er interval set kore din. 
*(Bas! Apnar bot ekhon theke 24/7 nonstop cholte thakbe)*

---

## 💡 Kichu Zaroori Tips

* **Reset First Run:** Bot jodi abar prothom theke notun kore 10 ta post korate chan, tahole apnar Telegram account-er **"Saved Messages"** e giye `AutoPoster_State_...` lekha message gulo delete kore Render-ti restart (Manual Deploy) din.
* **Large Media Files:** Beshi boro size-er video download/upload hote Render-er free server-e ektu beshi shomoy lagte pare. Normal photo, text ebong choto video-r jonno perfect.

---
**Developed with ❤️ using Python (Telethon & Flask)**
