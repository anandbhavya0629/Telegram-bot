# Telegram Advertisement Bot 🤖

A simple yet powerful Telegram bot that automatically sends advertisement messages to all subscribed users and groups.

## Features ✨

- **Auto-Subscribe**: Users automatically subscribe by sending `/start`
- **Scheduled Ads**: Sends ads every 60 minutes
- **Easy Control**: `/stop` to unsubscribe, `/stats` for information
- **Error Handling**: Automatically removes inactive chats
- **Secure**: Uses environment variables for bot tokens
- **Production Ready**: Deployable on Render, Heroku, or any server

## Bot Commands 📋

| Command | Description |
|---------|-------------|
| `/start` | Subscribe to advertisement messages |
| `/stop` | Unsubscribe from ads |
| `/stats` | View bot statistics |

## Setup Instructions 🚀

### Prerequisites
- Python 3.8+
- Telegram Bot Token (from @BotFather)
- Git

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/anandbhavya0629/Telegram-bot.git
   cd Telegram-bot
   ```

2. **Create virtual environment**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # Mac/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create .env file** (copy from .env.example)
   ```bash
   cp .env.example .env
   ```

5. **Add your bot token to .env**
   ```
   TELEGRAM_BOT_TOKEN=your_token_here
   ```

6. **Run the bot**
   ```bash
   python bot.py
   ```

### Deployment on Render

1. Push code to GitHub (ensure `.env` is NOT committed)
2. Go to [render.com](https://render.com) and sign up
3. Click **"New +"** → **"Web Service"**
4. Connect your GitHub repository
5. Configure:
   - **Name**: `telegram-bot`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python bot.py`
6. Add environment variable:
   - **Key**: `TELEGRAM_BOT_TOKEN`
   - **Value**: Your bot token
7. Click **Deploy**

## Project Structure 📁

```
Telegram-bot/
├── bot.py                 # Main bot code
├── requirements.txt       # Python dependencies
├── .env                   # Local secrets (not committed)
├── .env.example           # Example env variables
├── .gitignore             # Prevent committing secrets
└── README.md              # This file
```

## How It Works 🔧

1. Bot starts and waits for messages
2. When user sends `/start` → User is subscribed
3. Every 60 minutes → Bot sends ads to all subscribed users
4. If user sends `/stop` → User is unsubscribed
5. If chat is blocked/deleted → Automatically removed from list

## Error Handling 🛡️

- Invalid tokens are detected at startup
- Blocked users are automatically removed
- Network errors are logged and retried
- Graceful shutdown on `Ctrl+C`

## Security Notes 🔒

✅ **What's Done Right:**
- Bot token in `.env` (not in code)
- `.env` is in `.gitignore` (never committed)
- `.env.example` provided for reference
- Proper error handling

❌ **Never Do:**
- Hardcode tokens in Python files
- Commit `.env` to GitHub
- Share your bot token publicly

## Troubleshooting 🐛

| Issue | Solution |
|-------|----------|
| `TELEGRAM_BOT_TOKEN not found` | Create `.env` file with your token |
| Bot won't start | Check Python 3.8+ is installed |
| Render deployment fails | Ensure `requirements.txt` is committed |
| No ads sent | Check if users sent `/start` first |
| Import errors | Run `pip install -r requirements.txt` |

## Support 📞

- [Telegram Bot API Docs](https://core.telegram.org/bots)
- [python-telegram-bot Docs](https://docs.python-telegram-bot.org/)
- [BotFather Setup](https://core.telegram.org/bots#botfather)

## License 📄

MIT License - Feel free to use and modify

---

**Made with ❤️ by anandbhavya0629**
