import logging
import os

from dotenv import load_dotenv
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)

from database.users import init_db
from handlers.start import change_language, language, select_language, start
from handlers.qr_handler import (
    CHOOSE_PASSWORD,
    GET_EMAIL,
    GET_LINK,
    GET_NUMBER,
    GET_TEXT,
    GET_WIFI_NAME,
    GET_WIFI_PASSWORD,
    cancel,
    choose_wifi_password,
    get_email,
    get_link_button,
    get_phone_number,
    get_text,
    get_wifi,
    receive_email,
    receive_link,
    receive_number,
    receive_text,
    receive_wifi_name,
    receive_wifi_password,
)

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN", "").strip()
if not TOKEN:
    raise RuntimeError("BOT_TOKEN is missing. Add it to the .env file.")

logging.basicConfig(
    format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
    level=logging.INFO,
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


async def post_init(application: Application) -> None:
    init_db()
    logger.info("QR Code Bot initialized")


app = Application.builder().token(TOKEN).post_init(post_init).build()

conversation = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(get_link_button, pattern=r"^qr_link$"),
        CallbackQueryHandler(get_text, pattern=r"^qr_text$"),
        CallbackQueryHandler(get_phone_number, pattern=r"^qr_phone$"),
        CallbackQueryHandler(get_wifi, pattern=r"^qr_wifi$"),
        CallbackQueryHandler(get_email, pattern=r"^qr_email$"),
    ],
    states={
        GET_LINK: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_link)],
        GET_TEXT: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_text)],
        GET_NUMBER: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_number)],
        GET_WIFI_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_wifi_name)],
        CHOOSE_PASSWORD: [CallbackQueryHandler(choose_wifi_password, pattern=r"^wifi_(secured|open)$")],
        GET_WIFI_PASSWORD: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_wifi_password)],
        GET_EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_email)],
    },
    fallbacks=[
        CommandHandler("cancel", cancel),
        CommandHandler("language", language),
        CallbackQueryHandler(select_language, pattern=r"^lang_(fa|en)$"),
    ],
    allow_reentry=True,
)

# The language callback is also available when no conversation is active.
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("language", language))
app.add_handler(CallbackQueryHandler(select_language, pattern=r"^lang_(fa|en)$"))
app.add_handler(CallbackQueryHandler(change_language, pattern=r"^change_language$"))
app.add_handler(conversation)

if __name__ == "__main__":
    logger.info("Starting QR Code Bot")
    app.run_polling(allowed_updates=None)
