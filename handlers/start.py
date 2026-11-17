from telegram import Update
from telegram.ext import ContextTypes

from database.users import get_language, set_language
from keyboards.keyboard import language_keyboard, main_menu

TEXTS = {
    "fa": {
        "welcome": "سلام! 👋\nبه ربات ساخت QR Code خوش اومدی.\nچه نوع QR Code می‌خوای بسازی؟",
        "choose": "لطفاً زبان موردنظرت رو انتخاب کن:",
        "saved": "زبان با موفقیت تغییر کرد. ✅",
        "language_prompt": "زبان موردنظرت رو انتخاب کن:",
        "unknown": "برای شروع، لطفاً زبان ربات رو انتخاب کن.",
    },
    "en": {
        "welcome": "Hello! 👋\nWelcome to the QR Code Generator Bot.\nWhat type of QR code would you like to create?",
        "choose": "Please select your preferred language:",
        "saved": "Your language has been updated. ✅",
        "language_prompt": "Choose your preferred language:",
        "unknown": "Please select a language to get started.",
    },
}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    selected_language = get_language(user_id)
    if not selected_language:
        await update.effective_message.reply_text(
            "سلام! خوش اومدی 👋\nPlease select your language / لطفاً زبانت رو انتخاب کن:",
            reply_markup=language_keyboard(),
        )
        return
    await update.effective_message.reply_text(
        TEXTS[selected_language]["welcome"],
        reply_markup=main_menu(selected_language),
    )


async def language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    current = get_language(update.effective_user.id)
    prompt = TEXTS.get(current or "fa", TEXTS["fa"])["language_prompt"]
    await update.effective_message.reply_text(prompt, reply_markup=language_keyboard())


async def change_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    current = get_language(update.effective_user.id) or "fa"
    prompt = TEXTS[current]["language_prompt"]
    await query.message.reply_text(prompt, reply_markup=language_keyboard())


async def select_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    selected_language = query.data.removeprefix("lang_")
    set_language(update.effective_user.id, selected_language)
    await query.edit_message_text(
        TEXTS[selected_language]["saved"] + "\n\n" + TEXTS[selected_language]["welcome"],
        reply_markup=main_menu(selected_language),
    )
