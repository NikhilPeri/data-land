from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Index, Integer, Time, String, Float

from datetime import datetime

Base = declarative_base()

class ProlineTicket(Base):
    __tablename__ = 'proline_tickets'

    id         = Column(Integer, primary_key=True)
    created_at = Column(Time,    default=datetime.utcnow)
    updated_at = Column(Time,    default=datetime.utcnow, onupdate=datetime.utcnow)
    handle     = Column(Integer, nullable=False)
    date       = Column(Time,    nullable=False)

    idx_handle_date = Index('handle', 'date', unique=True)
