import urllib2
import urllib
from dataland.operations import UpdateOperation
from bs4 import BeautifulSoup, Comment


class ScrapeStandings(UpdateOperation):
    def __init__(self):
        pass

def standings(day, month, year, database):
    url = "https://www.basketball-reference.com/friv/standings.fcgi?" + urllib.urlencode({'day': day, 'month': month, 'year': year})
    print 'request -> ' + url
    page = urllib2.urlopen(url).read()
    doc = BeautifulSoup(page)

    for comment in doc.findAll(text=lambda text:isinstance(text, Comment)):
        soup = BeautifulSoup(str(comment))
        table = soup.find('table', {'id' : 'team'})
        if table == None:
            continue

        for row in table.find_all('tr')[1:31]:
            rank = int(row.find('th', {'data-stat': 'ranker'}).getText())
            team_name =  str(row.find('td', {'data-stat': 'team_name'}).find('a').getText())
            games = int(row.find('td', {'data-stat': 'g'}).getText())
            minutes = int(row.find('td', {'data-stat': 'mp'}).getText())

            field_goals = int(row.find('td', {'data-stat': 'fg'}).getText())
            field_goal_attempts = int(row.find('td', {'data-stat': 'fga'}).getText())
            field_goal_percentage = float(row.find('td', {'data-stat': 'fg_pct'}).getText())

            three_points = int(row.find('td', {'data-stat': 'fg3'}).getText())
            three_point_attempts = int(row.find('td', {'data-stat': 'fg3a'}).getText())
            three_point_percentage = float(row.find('td', {'data-stat': 'fg3_pct'}).getText())

            two_points = int(row.find('td', {'data-stat': 'fg2'}).getText())
            two_point_attempts = int(row.find('td', {'data-stat': 'fg2a'}).getText())
            two_point_percentage = float(row.find('td', {'data-stat': 'fg2_pct'}).getText())

            free_throws = int(row.find('td', {'data-stat': 'ft'}).getText())
            free_throw_attempts = int(row.find('td', {'data-stat': 'fta'}).getText())
            free_throw_percentage = float(row.find('td', {'data-stat': 'ft_pct'}).getText())

            offensive_rebounds = int(row.find('td', {'data-stat': 'orb'}).getText())
            defensive_rebounds = int(row.find('td', {'data-stat': 'drb'}).getText())
            total_rebounds = int(row.find('td', {'data-stat': 'trb'}).getText())

            assists = int(row.find('td', {'data-stat': 'ast'}).getText())
            steals = int(row.find('td', {'data-stat': 'stl'}).getText())
            blocks = int(row.find('td', {'data-stat': 'blk'}).getText())
            turn_overs = int(row.find('td', {'data-stat': 'tov'}).getText())
            personal_fouls = int(row.find('td', {'data-stat': 'pf'}).getText())
            points = int(row.find('td', {'data-stat': 'pts'}).getText())

            date = str(year) + '-' + str(month) + '-' + str(day)

if __name__ == '__main__':
    for month  in [1, 2, 3, 4, 5]:
        for day in range(1, 31):
            try:
                standings(day, month, 2018, database)
            except:
                print 'FAILED DAY ' + str(day) + '-' + str(month) + '-' + str(2017)
