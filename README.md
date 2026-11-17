# QR Code Bot | ربات ساخت QR Code

A bilingual Telegram bot that generates QR codes for URLs, plain text, Iranian mobile numbers, Wi-Fi networks, and email addresses.

یک ربات تلگرام دوزبانه برای ساخت QR Code از لینک، متن، شماره موبایل ایران، شبکه Wi-Fi و آدرس ایمیل.

## Features | امکانات

- Persian and English interface (language is selected on first use and saved in SQLite)
- Change language at any time using `/language`
- Generate QR codes for URLs, text, Iranian mobile numbers, Wi-Fi (secured/open), and email
- Input validation and `/cancel` command
- Per-user language persistence
- رابط فارسی و انگلیسی با انتخاب زبان در اولین ورود
- ذخیره زبان کاربر در دیتابیس SQLite
- امکان تغییر زبان با دستور `/language`
- ساخت QR برای لینک، متن، شماره موبایل ایران، وای‌فای رمزدار و بدون رمز و ایمیل
- اعتبارسنجی ورودی‌ها و لغو عملیات با `/cancel`

## Project Structure | ساختار پروژه

```text
qr_code_bot/
├── database/
│   └── users.py
├── handlers/
│   ├── start.py
│   └── qr_handler.py
├── keyboards/
│   └── keyboard.py
├── services/
│   └── qr_generator.py
├── main.py
├── requirements.txt
├── .env.example
└── .gitignore
```

## Setup | راه‌اندازی

Python 3.11 or newer is recommended. Python 3.11 is a safe choice for the hosting environment.

### 1. Create a virtual environment

```bash
python -m venv .venv
```

### 2. Activate the environment

```powershell
# Windows PowerShell
.venv\Scripts\Activate.ps1
```

```bash
# Linux / macOS
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file beside `main.py` based on `.env.example` and add your own Telegram BotFather token:

```env
BOT_TOKEN=your_bot_token_here
```

### 5. Run the bot

```bash
python main.py
```

## Telegram Commands | دستورات

- `/start` — Start the bot / شروع ربات
- `/language` — Change language / تغییر زبان
- `/cancel` — Cancel the current operation / لغو عملیات جاری

## Notes | نکات

- Never upload `.env`, bot tokens, or database files to a public repository.
- The SQLite database is created automatically on startup.
- Iranian mobile numbers are validated using the `09xxxxxxxxx` format.
- This project uses Telegram long polling. Only one running instance should use a bot token at a time.

## Links | لینک‌ها

- Telegram Bot: [QR Code Bot](https://t.me/YOUR_BOT_USERNAME)
- GitHub: [Saman Ziarati](https://github.com/samanzt)

