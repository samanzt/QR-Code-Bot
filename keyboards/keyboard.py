from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def language_keyboard():
    return InlineKeyboardMarkup(
        [[
            InlineKeyboardButton("🇮🇷 فارسی", callback_data="lang_fa"),
            InlineKeyboardButton("🇬🇧 English", callback_data="lang_en"),
        ]]
    )


def main_menu(language="fa"):
    if language == "en":
        rows = [
            [InlineKeyboardButton("🔗 Link", callback_data="qr_link"), InlineKeyboardButton("📝 Text", callback_data="qr_text")],
            [InlineKeyboardButton("📞 Phone number", callback_data="qr_phone"), InlineKeyboardButton("📶 Wi-Fi", callback_data="qr_wifi")],
            [InlineKeyboardButton("✉️ Email", callback_data="qr_email")],
            [InlineKeyboardButton("🌐 Change language", callback_data="change_language")],
        ]
    else:
        rows = [
            [InlineKeyboardButton("🔗 لینک", callback_data="qr_link"), InlineKeyboardButton("📝 متن", callback_data="qr_text")],
            [InlineKeyboardButton("📞 شماره تماس", callback_data="qr_phone"), InlineKeyboardButton("📶 اتصال به وای‌فای", callback_data="qr_wifi")],
            [InlineKeyboardButton("✉️ ایمیل", callback_data="qr_email")],
            [InlineKeyboardButton("🌐 تغییر زبان", callback_data="change_language")],
        ]
    return InlineKeyboardMarkup(rows)


def choose_password(language="fa"):
    if language == "en":
        rows = [
            [InlineKeyboardButton("🔒 Password protected", callback_data="wifi_secured")],
            [InlineKeyboardButton("🔓 No password", callback_data="wifi_open")],
        ]
    else:
        rows = [
            [InlineKeyboardButton("🔒 وای‌فای رمزدار", callback_data="wifi_secured")],
            [InlineKeyboardButton("🔓 وای‌فای بدون رمز", callback_data="wifi_open")],
        ]
    return InlineKeyboardMarkup(rows)
