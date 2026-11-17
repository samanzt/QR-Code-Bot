# QR Code Bot

A bilingual Telegram bot that generates QR codes for URLs, plain text, Iranian mobile numbers, Wi-Fi networks, and email addresses.

## Features

- Persian and English interface
- Language selection on first use
- User language preference saved in SQLite
- Change language at any time using `/language`
- Generate QR codes for:
  - URLs
  - Plain text
  - Iranian mobile numbers
  - Wi-Fi networks (secured or open)
  - Email addresses
- Input validation
- Cancel ongoing operations using `/cancel`

## Project Structure

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

## Requirements

- Python 3.11 or newer
- A Telegram bot token from [@BotFather](https://t.me/BotFather)

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/samanzt/QR-Code-Bot.git
cd QR-Code-Bot
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

**Windows (PowerShell):**

```powershell
.venv\Scripts\Activate.ps1
```

**Linux / macOS:**

```bash
source .venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure environment variables

Create a `.env` file in the project root, using `.env.example` as a template.

Add your Telegram bot token:

```env
BOT_TOKEN=your_bot_token_here
```

### 6. Run the bot

```bash
python main.py
```

## Telegram Commands

| Command | Description |
|---|---|
| `/start` | Start the bot |
| `/language` | Change the interface language |
| `/cancel` | Cancel the current operation |

## Database

- Uses SQLite to store user language preferences.
- The database is created automatically when the bot starts.

## Validation

- Iranian mobile numbers are validated using the `09xxxxxxxxx` format.
- User input is validated before QR code generation.

## Notes

- Never upload your `.env` file, bot tokens, or database files to a public repository.
- This project uses Telegram long polling.
- Only one running instance should use a bot token at a time.

## Links

- **Telegram Bot:** [@QrixoBot](https://t.me/QrixoBot)
- **GitHub Profile:** [samanzt](https://github.com/samanzt)

## Author

Developed by [Saman Ziarati](https://github.com/samanzt).