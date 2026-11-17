from io import BytesIO

import qrcode


def _to_png_buffer(payload: str) -> BytesIO:
    image = qrcode.make(payload)
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0)
    buffer.name = "qr-code.png"
    return buffer


def generate_text_link_email(data: str) -> BytesIO:
    return _to_png_buffer(data)


def _escape_wifi(value: str) -> str:
    """Escape special characters according to the Wi-Fi QR payload format."""
    return "".join("\\" + char if char in r'\\;,:"' else char for char in value)


def generate_wifi_with_password(name: str, password: str, security: str = "WPA") -> BytesIO:
    payload = f"WIFI:T:{security};S:{_escape_wifi(name)};P:{_escape_wifi(password)};;"
    return _to_png_buffer(payload)


def generate_wifi_with_out_password(name: str) -> BytesIO:
    payload = f"WIFI:T:nopass;S:{_escape_wifi(name)};;"
    return _to_png_buffer(payload)


def generate_number(number: str) -> BytesIO:
    normalized = number.strip().replace(" ", "").replace("-", "")
    if normalized.startswith("09") and len(normalized) == 11 and normalized.isdigit():
        normalized = "+98" + normalized[1:]
    return _to_png_buffer(f"tel:{normalized}")
