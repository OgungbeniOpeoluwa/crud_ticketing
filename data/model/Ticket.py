from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

from data.repository.DbConnection import engine

Base = declarative_base()

class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    user_email = Column(String, index=True)
    event_name = Column(String)
    qr_code = Column(String)
    valid = Column(Boolean)
    ticket_id =Column(String)

    def to_dict(self):
        return {
            "id": self.id,
            "event_name": self.event_name,
            "email": self.user_email,
            "qr_code": self.qr_code,
            "valid": self.valid,
            "ticket_id": self.ticket_id,
        }

Base.metadata.create_all(bind=engine)


