import asyncio as aio
import os
from bot import bot, DB, manga_updater, chapter_creation  # Ensure these imports are correct
import logging

LOGGER = logging.getLogger(__name__)

# Environment variables
PORT = int(os.environ.get("PORT", "8443"))
TOKEN = os.environ.get("TOKEN")
RENDER_EXTERNAL_URL = os.environ.get("RENDER_EXTERNAL_URL")

if not TOKEN or not RENDER_EXTERNAL_URL:
    LOGGER.error("Environment variables TOKEN or RENDER_EXTERNAL_URL are not set")
    exit(1)  # Proper exit if environment variables are missing

# Set the webhook URL
WEBHOOK_URL = f"{RENDER_EXTERNAL_URL}/{TOKEN}"

# Log the values for debugging
LOGGER.info(f"PORT: {PORT}")
LOGGER.info(f"TOKEN: {TOKEN}")
LOGGER.info(f"RENDER_EXTERNAL_URL: {RENDER_EXTERNAL_URL}")
LOGGER.info(f"WEBHOOK_URL: {WEBHOOK_URL}")

# Async main function
async def async_main():
    db = DB()
    await db.connect()
    
    # Start additional tasks like manga updates and chapter creation
    aio.create_task(manga_updater())
    for i in range(10):
        aio.create_task(chapter_creation(i + 1))

# Running the bot with webhook configuration
if __name__ == '__main__':
    # Create event loop
    loop = aio.get_event_loop_policy().get_event_loop()
    
    # Ensure asynchronous tasks are running
    loop.run_until_complete(async_main())
    
    # Set up the webhook
    bot.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=TOKEN,
        webhook_url=WEBHOOK_URL
    )
