import base64
import io
import os

from fastapi_mail import ConnectionConfig, MessageSchema, FastMail
from starlette.datastructures import UploadFile

conf = ConnectionConfig(
    MAIL_USERNAME=os.environ.get("MAIL_USERNAME"),
    MAIL_PASSWORD=os.environ.get("MAIL_PASSWORD"),  # Use an App Password (not your regular password)
    MAIL_FROM= os.environ.get("MAIL_USERNAME"),
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=True,   # Replaces MAIL_TLS
    MAIL_SSL_TLS=False,   # Replaces MAIL_SSL
    USE_CREDENTIALS=True
)


async def send_qr_email(to_email: str, qr_code_base64: str):
    qr_code_data = base64.b64decode(qr_code_base64)

    qr_code_file = io.BytesIO(qr_code_data)
    qr_upload_file = UploadFile(filename="qrcode.png", file=qr_code_file)

    message = MessageSchema(
        subject="Your Ticket Purchase",
        recipients=[to_email],
        body="<h3>Your Ticket</h3><p>Thank you for purchasing a ticket! The QR code is attached.</p>",
        subtype="html",
        attachments=[qr_upload_file],  # ✅ Use UploadFile instead of tuple
    )

    fm = FastMail(conf)
    await fm.send_message(message)
