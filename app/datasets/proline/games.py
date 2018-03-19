from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

class ProlineGames(object):
        __tablename__ = 'proline_games'
        id          = Column(Integer, primary_key=True)
        created_at  = Column(Time,    default=datetime.utcnow)
        updated_at  = Column(Time,    default=datetime.utcnow, onupdate=datetime.utcnow)
        ticket_id   = Column(Integer, nullable=False)
        game_handle = Column(Integer, nullable=False)
        cutoff_date = Column(Time,    nullable=False)
        home        = Column(String,  nullable=False)
        visitor     = Column(String,  nullable=False)
        sport       = Column(String,  nullable=False)
        Column('outcomes',       String),
        Column('v_plus',         Float),
        Column('v',              Float),
        Column('t',              Float),
        Column('h',              Float),
        Column('h_plus',         Float),
        Index('idx_ticket_game_handle', 'ticket_id', 'game_handle', unique=True)