# Mioka Airdrop Bot

This is a Telegram bot for managing an airdrop campaign for the Mioka token.

## Features

- **Multi-language Support:** The bot supports English, Japanese, and French.
- **Airdrop Tasks:** Users must complete a series of tasks to earn tokens.
- **Referral System:** The bot tracks direct and indirect referrals to award extra tokens.
- **Admin Functionality:** The admin can generate an Excel file of all participants.

## How to Deploy on Render

### Step 1: Create a GitHub Repository

1.  Create a new repository on your GitHub account (`Mioka-dev`).
2.  Add all the files (`main.py`, `requirements.txt`, `translations.py`, `Procfile`) to this repository.

### Step 2: Configure Render

1.  Log in to your Render account.
2.  Go to the dashboard and create a new **Web Service**.
3.  Connect your GitHub repository (`mioka-airdrop-bot`).
4.  In the **Environment** section, set the following:
    - **`Build Command`**: `pip install -r requirements.txt`
    - **`Start Command`**: `python main.py`
5.  In the **Environment Variables** section, add your bot token:
    - **Key**: `BOT_TOKEN`
    - **Value**: `8446660847:AAELsOK5Qfr2NzLQwTn-pM3jPlLaAHSyEf8` (Your actual bot token from BotFather)
6.  Click **Create Web Service**. Render will now automatically deploy your bot.

### Step 3: Set the Webhook

1.  After the deployment is complete, Render will provide a public URL for your service (e.g., `https://mioka-airdrop-bot.onrender.com`).
2.  You need to set this URL as your bot's webhook using the Telegram Bot API. You can do this by opening a new tab in your browser and entering the following URL (replace the placeholders):
    `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/setWebhook?url=<YOUR_RENDER_URL>`
    
    **Example:**
    `https://api.telegram.org/bot8446660847:AAELsOK5Qfr2NzLQwTn-pM3jPlLaAHSyEf8/setWebhook?url=https://mioka-airdrop-bot.onrender.com`

Your bot should now be fully functional.