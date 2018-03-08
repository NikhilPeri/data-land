from ..app.utils.database import Database
import csv

def main():
    db = Database()

    with open('/data/csv/backfill_tickets.csv') as tickets_file:
        tickets_reader = csv.DictReader(tickets_file)
        for ticket in tickets_reader:
            print ticket

if __name__ == '__main__':
    main()
