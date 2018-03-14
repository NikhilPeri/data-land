from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Index, Integer, String, Float, Date, MetaData, Time
from datetime import datetime

import os

db = create_engine(os.environ['DATABASE_URL'])
meta = MetaData(db)
proline_games_table = Table('proline_games', meta,
    Column('id',             Integer, primary_key=True),
    Column('created_at',     Time,    default=datetime.utcnow),
    Column('updated_at',     Time,    default=datetime.utcnow, onupdate=datetime.utcnow),
    Column('ticket_id',      Integer, nullable=False),
    Column('game_handle',    Integer, nullable=False),
    Column('cutoff_date',    Time,    nullable=False),
    Column('home',           String,  nullable=False),
    Column('visitor',        String,  nullable=False),
    Column('sport',          String,  nullable=False),
    Column('outcomes',       String),
    Column('v_plus',         Float),
    Column('v',              Float),
    Column('t',              Float),
    Column('h',              Float),
    Column('h_plus',         Float),
    Index('idx_ticket_game_handle', 'ticket_id', 'game_handle', unique=True)
    )

with db.connect() as conn:
    proline_games_table.create()
