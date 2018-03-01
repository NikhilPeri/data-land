from datetime import datetime

import requests
import json
import time

class UpdateProlineTicketsStage(Object)
    def process(self):
        for ticket in fetch_ticket_list():
            create_ticket(ticket)

    def create_ticket(ticket_data):
        ticket_id = int(ticket_data['listNumber'])
        ticket_date = datetime.fromtimestamp(ticket_data['listDate']/1000)

        for game_data in ticket_data['eventList']:
            create_game(ticket_id, game_data)

    def create_game(ticket_id, game_data):
        game_id = game_data['id']
        cuttoff_date = datetime.strptime(game_data['cutoffDate'], '%Y-%m-%d %H:%M:%S.0')
        home_symbol = game_data['home']
        visitor_symbol = game_data['visitor']
        home_name = game_data['homeName']
        visitor_name = game_data['visitorName']
        sport = game_data['sport']
        v_plus = game_data['vplus']
        v = game_data['v']
        h = game_data['h']
        h_plus = game_data['hplus']


    def fetch_ticket_list():
        OLG_TICKETS_ENDPOINT = "https://www.proline.ca/olg-proline-services/rest/api/proline/events/all.json"
        response = requests.get(OLG_TICKETS_ENDPOINT, verify=False).text
        return json.loads(response)['events']['eventList']



















eventsAdded = 0
mlbEventsAdded = 0
for event in events:
    eventId = event.get("listNumber")
    #listNumber
    if not(data.has_key(eventId)):
        data[eventId] = {}

    #listDate
    if not(data[eventId].has_key("date")):
        data[eventId]["date"] = event.get("listDate")

    #eventsList
    if not(data[eventId].has_key("games")):
        data[eventId]["games"] = {}

    for game in event.get("eventList"):
        #gameId
        gameId = game.get("id")
        if not(data[eventId]["games"].has_key(gameId)):
            #gameId
            data[eventId]["games"][gameId] = {}

            # gameData
            data[eventId]["games"][gameId]["home"] = game.get("homeName")
            data[eventId]["games"][gameId]["visitor"] = game.get("visitorName")
            data[eventId]["games"][gameId]["sport"] = game.get("sport")
            data[eventId]["games"][gameId]["cutoffDate"] = game.get("cutoffDate")
            data[eventId]["games"][gameId]["outcomes"] = []

            #odds
            data[eventId]["games"][gameId]["v+"] = game.get("odds").get("vplus")
            data[eventId]["games"][gameId]["v"] = game.get("odds").get("v")
            data[eventId]["games"][gameId]["t"] = game.get("odds").get("t")
            data[eventId]["games"][gameId]["h"] = game.get("odds").get("h")
            data[eventId]["games"][gameId]["h+"] = game.get("odds").get("hplus")

            if game.get("sport") == "BBL":
                data[eventId]["games"][gameId]["mlb_standings"] = {}
                data[eventId]["games"][gameId]["mlb_standings"]["home"] = {}
                home_stats = mlb_data[data[eventId]["games"][gameId]["home"].upper()]
                data[eventId]["games"][gameId]["mlb_standings"]["home"]["rank"] = home_stats["rank"]
                data[eventId]["games"][gameId]["mlb_standings"]["home"]["points_scored_per_game"] = home_stats["points_scored_per_game"]
                data[eventId]["games"][gameId]["mlb_standings"]["home"]["points_allowed_per_game"] = home_stats["points_allowed_per_game"]
                data[eventId]["games"][gameId]["mlb_standings"]["home"]["win_percentage"] = home_stats["win_percentage"]
                data[eventId]["games"][gameId]["mlb_standings"]["home"]["location_win_percentage"] = home_stats["home_win_percentage"]
                data[eventId]["games"][gameId]["mlb_standings"]["home"]["last_five_won_percentage"] = home_stats["last_five_won_percentage"]
                data[eventId]["games"][gameId]["mlb_standings"]["home"]["last_ten_won_percentage"] = home_stats["last_ten_won_percentage"]
                data[eventId]["games"][gameId]["mlb_standings"]["home"]["streak"] = home_stats["streak"]

                data[eventId]["games"][gameId]["mlb_standings"]["visitor"] = {}
                visitor_stats = mlb_data[data[eventId]["games"][gameId]["visitor"].upper()]
                data[eventId]["games"][gameId]["mlb_standings"]["visitor"]["rank"] = visitor_stats["rank"]
                data[eventId]["games"][gameId]["mlb_standings"]["visitor"]["points_scored_per_game"] = visitor_stats["points_scored_per_game"]
                data[eventId]["games"][gameId]["mlb_standings"]["visitor"]["points_allowed_per_game"] = visitor_stats["points_allowed_per_game"]
                data[eventId]["games"][gameId]["mlb_standings"]["visitor"]["win_percentage"] = visitor_stats["win_percentage"]
                data[eventId]["games"][gameId]["mlb_standings"]["visitor"]["location_win_percentage"] = visitor_stats["visitor_win_percentage"]
                data[eventId]["games"][gameId]["mlb_standings"]["visitor"]["last_five_won_percentage"] = visitor_stats["last_five_won_percentage"]
                data[eventId]["games"][gameId]["mlb_standings"]["visitor"]["last_ten_won_percentage"] = visitor_stats["last_ten_won_percentage"]
                data[eventId]["games"][gameId]["mlb_standings"]["visitor"]["streak"] = visitor_stats["streak"]

                mlbEventsAdded += 1

            eventsAdded += 1

print "Events Added: ", eventsAdded
print "MLB Events Added: ", mlbEventsAdded

print(OLG_RESULTS_ENDPOINT + "&_" + str(int(time.time()*1000)))
response = requests.get(OLG_RESULTS_ENDPOINT + "&_" + str(int(time.time()*1000)), verify=False).text
response = response.replace('_jqjsp(', '', 1)
response = response.replace(');', '', 1)

results = json.loads(response).get("response").get("results").get("resultList")

eventsUpdated = 0
for eventResult in results:
    eventId = eventResult.get("listNumber")
    if not(data.has_key(eventId)):
        break

    for gameResult in eventResult.get("results"):
        gameId = gameResult.get("id")

        if data[eventId]["games"].has_key(gameId):
            outcome = gameResult["odds"]
            data[eventId]["games"][gameId]["outcomes"] = []

            updated = False
            if outcome["vplus"] is not None:
                data[eventId]["games"][gameId]["outcomes"].append("v+")
                updated = True
            if outcome["v"] is not None:
                data[eventId]["games"][gameId]["outcomes"].append("v")
                updated = True
            if outcome["hplus"] is not None:
                data[eventId]["games"][gameId]["outcomes"].append("h+")
                updated = True
            if outcome["h"] is not None:
                data[eventId]["games"][gameId]["outcomes"].append("h")
                updated = True
            if outcome["t"] is not None:
                data[eventId]["games"][gameId]["outcomes"].append("t")
                updated = True
            if updated:
                eventsUpdated += 1

print "Events Updated: ", eventsUpdated

with open('data/events.json', 'w') as data_file:
    data_file.write(json.dumps(data, indent=2))
