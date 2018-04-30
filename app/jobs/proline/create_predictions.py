import requests
import json
from datetime import datetime

from app.datasets.database import Database
from app.datasets.proline import ProlineTicket, ProlineGame

from app.jobs import BaseJob

class CreatePredictions(BaseJob):
    def run(self):
        games = self.load_games()

    def predict(self, game):
        games.order_by("ABS('v' - 'h')").limit(3)
        

    def load_ticket(self):
        self.db.query(ProlineTicket).filter_by(date=??).first()

    def load_games(self):
        ticket = self.load_ticket()
        self.db.query(ProlineGame).filter_by(ticket_id=ticket.id)

if __name__ == '__main__':
    CreatePredictions.perform()
