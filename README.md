
# Mioka Airdrop Bot

## Setup

1. Create a `.env` file and add:
   BOT_TOKEN=your-telegram-bot-token

2. Install dependencies:
   pip install -r requirements.txt

3. Run locally (for debug):
   python main.py

4. Deploy to Render as a Web Service.
   - Start command: `python main.py`
   - Use webhook URL: `https://your-render-url.com/webhook/YOUR_BOT_TOKEN`
