import os
import asyncio
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

# Load environment variables from .env file
load_dotenv()

# Get bot token from environment variable
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Validate token exists
if not TOKEN:
    print("❌ ERROR: TELEGRAM_BOT_TOKEN not found in environment variables!")
    print("Please create a .env file with: TELEGRAM_BOT_TOKEN=your_token_here")
    exit(1)

# Store chat IDs of subscribed users/groups
subscribed_chats = set()

# ============================================
# COMMAND HANDLERS
# ============================================

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command - Subscribe user to ads"""
    chat_id = update.effective_chat.id
    chat_name = update.effective_chat.title or update.effective_user.first_name
    
    if chat_id not in subscribed_chats:
        subscribed_chats.add(chat_id)
        print(f"✅ New subscription: {chat_name} (ID: {chat_id})")
    
    await update.message.reply_text(
        "✅ *You are now subscribed!*\n\n"
        "You will receive advertisement messages every 60 minutes.\n\n"
        "Commands:\n"
        "• `/stop` - Unsubscribe from ads\n"
        "• `/stats` - View bot statistics",
        parse_mode="Markdown"
    )


async def stop_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /stop command - Unsubscribe user from ads"""
    chat_id = update.effective_chat.id
    chat_name = update.effective_chat.title or update.effective_user.first_name
    
    if chat_id in subscribed_chats:
        subscribed_chats.remove(chat_id)
        print(f"❌ Unsubscribed: {chat_name} (ID: {chat_id})")
    
    await update.message.reply_text(
        "❌ *You have been unsubscribed.*\n\n"
        "You will no longer receive advertisement messages.\n\n"
        "Send `/start` anytime to resubscribe.",
        parse_mode="Markdown"
    )


async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /stats command - Show bot statistics"""
    await update.message.reply_text(
        f"📊 *Bot Statistics*\n\n"
        f"Active Subscribers: *{len(subscribed_chats)}*\n"
        f"Ad Interval: *60 minutes*\n"
        f"Status: *✅ Running*",
        parse_mode="Markdown"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command - Show available commands"""
    await update.message.reply_text(
        "🤖 *Telegram Advertisement Bot*\n\n"
        "*Available Commands:*\n"
        "• `/start` - Subscribe to ads\n"
        "• `/stop` - Unsubscribe from ads\n"
        "• `/stats` - View statistics\n"
        "• `/help` - Show this message\n\n"
        "*How it works:*\n"
        "1. Send `/start` to subscribe\n"
        "2. Receive ads every 60 minutes\n"
        "3. Send `/stop` to unsubscribe anytime",
        parse_mode="Markdown"
    )


# ============================================
# MESSAGE HANDLER
# ============================================

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Auto-subscribe any user who sends a message"""
    chat_id = update.effective_chat.id
    chat_name = update.effective_chat.title or update.effective_user.first_name
    
    if chat_id not in subscribed_chats:
        subscribed_chats.add(chat_id)
        print(f"✅ Auto-subscribed: {chat_name} (ID: {chat_id})")
        
        await update.message.reply_text(
            "✅ Welcome! You've been auto-subscribed to our advertisement service.\n\n"
            "Send `/stop` to unsubscribe anytime.",
            parse_mode="Markdown"
        )


# ============================================
# ADVERTISEMENT TASK
# ============================================

async def send_advertisements(app):
    """Send advertisement messages to all subscribed chats every 60 minutes"""
    ad_message = """
🚀 *SOCIAL MEDIA SERVICES* 🔥

📸 *Instagram*
• Unbann / Ban
• Shielding
• Lookups
• Gen & Non-Gen Claims

📘 *Facebook*
• Unbann / Ban
• Shielding
• Lookups
• Gen & Non-Gen Claims

🎵 *TikTok* — Unbann / Ban
👻 *Snapchat* — Unbann / Ban
🟢 *WhatsApp* — Unbann / Ban

💼 *Business Manager Services*

🔒 Trusted • ⚡ Fast

🤝 *MM:* @mrgod @laugh @Cold @thon

📩 *DM:* @The_Legend_1568
"""
    
    while True:
        try:
            await asyncio.sleep(3600)  # Wait 60 minutes before sending ads
            
            if len(subscribed_chats) == 0:
                print("⏰ Ad time - No subscribed chats")
                continue
            
            print(f"📢 Sending ads to {len(subscribed_chats)} chats...")
            
            # Create a copy to avoid issues if set changes during iteration
            chats_to_send = subscribed_chats.copy()
            
            for chat_id in chats_to_send:
                try:
                    await app.bot.send_message(
                        chat_id=chat_id,
                        text=ad_message,
                        parse_mode="Markdown"
                    )
                except Exception as e:
                    # Remove chat if there's an error (likely user blocked or deleted)
                    if chat_id in subscribed_chats:
                        subscribed_chats.remove(chat_id)
                    print(f"⚠️ Error sending to {chat_id}: {str(e)[:50]}")
            
            print(f"✅ Ads sent successfully to {len(chats_to_send)} chats")
            
        except Exception as e:
            print(f"❌ Advertisement loop error: {str(e)}")
            await asyncio.sleep(10)  # Wait before retrying


# ============================================
# MAIN FUNCTION
# ============================================

async def main():
    """Initialize and run the bot"""
    print("==================================================")
    print("🤖 TELEGRAM ADVERTISEMENT BOT")
    print("==================================================")
    
    # Create the Application
    print("✅ Bot token loaded successfully")
    print("🚀 Starting Telegram Bot...")
    
    app = ApplicationBuilder().token(TOKEN).build()
    
    # Add command handlers
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("stop", stop_command))
    app.add_handler(CommandHandler("stats", stats_command))
    app.add_handler(CommandHandler("help", help_command))
    
    # Add message handler (auto-subscribe)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("✅ Bot initialized successfully!")
    
    # Start the advertisement task
    asyncio.create_task(send_advertisements(app))
    print("📢 Advertisement scheduler started (60 minute interval)")
    
    # Start polling for updates
    print("📢 Listening for messages...\n")
    await app.run_polling()


# ============================================
# ENTRY POINT
# ============================================

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 Bot stopped by user")
    except Exception as e:
        print(f"\n❌ Bot error: {e}")
