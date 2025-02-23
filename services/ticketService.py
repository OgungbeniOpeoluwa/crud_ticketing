import asyncio
import base64
import random
import string
import threading
from io import BytesIO

import qrcode
from flask import jsonify
from sqlalchemy.orm import Session

from data.model.Ticket import Ticket
from data.repository.DbConnection import get_db
from services.emailService import send_qr_email

db: Session = get_db()

def buy_ticket(email:str,eventName:str):
    ticket_id = generate_ticket_id(5)
    response = {
        "ticket_id": ticket_id,
        "validity":True,
    }
    qr_data = f"Ticket for {eventName} {response}"
    qr = qrcode.make(qr_data)
    buffered = BytesIO()
    qr.save(buffered, format="PNG")
    qr_code_base64 = base64.b64encode(buffered.getvalue()).decode()


    ticket = Ticket(user_email=email, event_name=eventName, qr_code=qr_code_base64,valid=True,ticket_id=ticket_id)
    db.add(ticket)
    db.commit()
    db.refresh(ticket)

    threading.Thread(target=asyncio.run, args=(send_qr_email(email, qr_code_base64),)).start()

    return ticket_id


def get_ticket():
    tickets = db.query(Ticket).all()
    return jsonify([ticket.to_dict() for ticket in tickets])



def generate_ticket_id(length=8):
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choices(characters, k=length))

