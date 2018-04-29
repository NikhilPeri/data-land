from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Index, Integer, Time, String, Float

from datetime import datetime

Base = declarative_base()

class ProlineGames(Base):
    __tablename__ = 'proline_games'

    id          = Column(Integer, primary_key=True)
    created_at  = Column(Time,    default=datetime.utcnow)
    updated_at  = Column(Time,    default=datetime.utcnow, onupdate=datetime.utcnow)
    ticket_id   = Column(Integer, nullable=False)
    handle      = Column(Integer, nullable=False)
    cutoff_date = Column(Time,    nullable=False)
    home        = Column(String,  nullable=False)
    visitor     = Column(String,  nullable=False)
    sport       = Column(String,  nullable=False)
    outcomes    = Column(String)
    v_plus      = Column(Float)
    v           = Column(Float)
    t           = Column(Float)
    h           = Column(Float)
    h_plus      = Column(Float)

    idx_ticket_game_handle = Index('ticket_id', 'game_handle', unique=True)
