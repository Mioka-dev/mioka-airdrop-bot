# Mioka Airdrop Bot

This is a single-language Telegram bot for the Mioka Airdrop campaign.

## Features

-   **Airdrop Participation**: Guides users through missions (joining Telegram, following on Twitter, etc.).
-   **Referral System**: Tracks direct and indirect referrals to calculate user tokens.
-   **Admin Panel**: Allows the administrator to extract a list of all participants in CSV format.
-   **Single Language**: The bot is configured to operate exclusively in English to ensure stable deployment on the Render platform.

## Setup

### Environment Variables

Before deploying, ensure you have set the following environment variables on your platform (e.g., Render):

-   `BOT_TOKEN`: Your Telegram bot token.
-   `WEBHOOK_URL`: The webhook URL provided by your hosting service (e.g., `https://your-app-name.onrender.com/`).

### Deployment

This bot is designed to be deployed on platforms like Render. It requires the following files in the main directory:

1.  `main.py`: The main bot script.
2.  `requirements.txt`: A list of all required Python libraries.
3.  `Procfile`: Specifies the command to run the bot.