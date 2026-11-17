import re
from urllib.parse import urlparse

from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from database.users import get_language
from keyboards.keyboard import choose_password, main_menu
from services.qr_generator import (
    generate_number,
    generate_text_link_email,
    generate_wifi_with_out_password,
    generate_wifi_with_password,
)

GET_LINK, GET_TEXT, GET_NUMBER, GET_WIFI_NAME, CHOOSE_PASSWORD, GET_WIFI_PASSWORD, GET_EMAIL = range(1, 8)
MAX_TEXT_LENGTH = 2000

MESSAGES = {
    "fa": {
        "cancelled": "عملیات لغو شد.", "link_prompt": "لینک موردنظرت رو بفرست (با http:// یا https://).",
        "link_invalid": "لینک معتبر نیست. یک آدرس کامل با http:// یا https:// بفرست.",
        "text_prompt": "متن موردنظرت رو بفرست.", "number_prompt": "شماره موبایل ایران رو به شکل 09123456789 بفرست.",
        "number_invalid": "شماره معتبر نیست. نمونه صحیح: 09123456789",
        "wifi_prompt": "نام شبکه Wi-Fi رو بفرست.", "wifi_choose": "این شبکه رمز دارد؟",
        "password_prompt": "رمز Wi-Fi رو بفرست.", "email_prompt": "آدرس ایمیلت رو بفرست.",
        "email_invalid": "ایمیل معتبر نیست. دوباره وارد کن.", "too_long": "متن بیش از حد طولانیه. حداکثر ۲۰۰۰ کاراکتر بفرست.",
        "empty": "ورودی نمی‌تونه خالی باشه. دوباره تلاش کن.", "generated": "QR Code آماده شد! می‌تونی تصویر رو ذخیره کنی. ✅",
        "error": "ساخت QR Code با خطا مواجه شد. لطفاً دوباره تلاش کن.",
    },
    "en": {
        "cancelled": "Operation cancelled.", "link_prompt": "Send the URL (starting with http:// or https://).",
        "link_invalid": "Invalid URL. Send a complete address starting with http:// or https://.",
        "text_prompt": "Send the text you want to encode.", "number_prompt": "Send an Iranian mobile number in this format: 09123456789.",
        "number_invalid": "Invalid number. Example: 09123456789",
        "wifi_prompt": "Send the Wi-Fi network name (SSID).", "wifi_choose": "Is this Wi-Fi network password-protected?",
        "password_prompt": "Send the Wi-Fi password.", "email_prompt": "Send the email address.",
        "email_invalid": "Invalid email address. Please try again.", "too_long": "The input is too long. Maximum length is 2,000 characters.",
        "empty": "Input cannot be empty. Please try again.", "generated": "Your QR code is ready! You can save the image. ✅",
        "error": "Could not generate the QR code. Please try again.",
    },
}


def _lang(update: Update) -> str:
    return get_language(update.effective_user.id) or "fa"


def _t(update: Update, key: str) -> str:
    return MESSAGES[_lang(update)][key]


async def _send_qr(update: Update, payload_buffer):
    try:
        await update.effective_message.reply_photo(photo=payload_buffer, caption=_t(update, "generated"))
    except Exception:
        await update.effective_message.reply_text(_t(update, "error"))
        raise
    finally:
        payload_buffer.close()


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.effective_message.reply_text(_t(update, "cancelled"), reply_markup=main_menu(_lang(update)))
    return ConversationHandler.END


async def get_link_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.message.reply_text(_t(update, "link_prompt"))
    return GET_LINK


async def receive_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    link = (update.effective_message.text or "").strip()
    parsed = urlparse(link)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc or " " in link:
        await update.effective_message.reply_text(_t(update, "link_invalid"))
        return GET_LINK
    if len(link) > MAX_TEXT_LENGTH:
        await update.effective_message.reply_text(_t(update, "too_long"))
        return GET_LINK
    await _send_qr(update, generate_text_link_email(link))
    return ConversationHandler.END


async def get_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.message.reply_text(_t(update, "text_prompt"))
    return GET_TEXT


async def receive_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (update.effective_message.text or "").strip()
    if not text:
        await update.effective_message.reply_text(_t(update, "empty"))
        return GET_TEXT
    if len(text) > MAX_TEXT_LENGTH:
        await update.effective_message.reply_text(_t(update, "too_long"))
        return GET_TEXT
    await _send_qr(update, generate_text_link_email(text))
    return ConversationHandler.END


async def get_phone_number(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.message.reply_text(_t(update, "number_prompt"))
    return GET_NUMBER


async def receive_number(update: Update, context: ContextTypes.DEFAULT_TYPE):
    number = (update.effective_message.text or "").strip()
    if not re.fullmatch(r"09\d{9}", number):
        await update.effective_message.reply_text(_t(update, "number_invalid"))
        return GET_NUMBER
    await _send_qr(update, generate_number(number))
    return ConversationHandler.END


async def get_wifi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.message.reply_text(_t(update, "wifi_prompt"))
    return GET_WIFI_NAME


async def receive_wifi_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = (update.effective_message.text or "").strip()
    if not name:
        await update.effective_message.reply_text(_t(update, "empty"))
        return GET_WIFI_NAME
    if len(name) > 100:
        await update.effective_message.reply_text(_t(update, "too_long"))
        return GET_WIFI_NAME
    context.user_data["wifi_name"] = name
    await update.effective_message.reply_text(_t(update, "wifi_choose"), reply_markup=choose_password(_lang(update)))
    return CHOOSE_PASSWORD


async def choose_wifi_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    name = context.user_data.get("wifi_name")
    if not name:
        await query.message.reply_text(_t(update, "error"))
        return ConversationHandler.END
    if query.data == "wifi_secured":
        await query.message.reply_text(_t(update, "password_prompt"))
        return GET_WIFI_PASSWORD
    await _send_qr(update, generate_wifi_with_out_password(name))
    context.user_data.pop("wifi_name", None)
    return ConversationHandler.END


async def receive_wifi_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    password = (update.effective_message.text or "").strip()
    name = context.user_data.get("wifi_name")
    if name is None:
        await update.effective_message.reply_text(_t(update, "error"))
        return ConversationHandler.END
    if not password:
        await update.effective_message.reply_text(_t(update, "empty"))
        return GET_WIFI_PASSWORD
    if len(password) > 100:
        await update.effective_message.reply_text(_t(update, "too_long"))
        return GET_WIFI_PASSWORD
    await _send_qr(update, generate_wifi_with_password(name, password))
    context.user_data.pop("wifi_name", None)
    return ConversationHandler.END


async def get_email(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.message.reply_text(_t(update, "email_prompt"))
    return GET_EMAIL


async def receive_email(update: Update, context: ContextTypes.DEFAULT_TYPE):
    email = (update.effective_message.text or "").strip()
    if not re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", email):
        await update.effective_message.reply_text(_t(update, "email_invalid"))
        return GET_EMAIL
    if len(email) > 254:
        await update.effective_message.reply_text(_t(update, "too_long"))
        return GET_EMAIL
    await _send_qr(update, generate_text_link_email(f"mailto:{email}"))
    return ConversationHandler.END
