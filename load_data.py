from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

client = MongoClient(os.getenv("MONGODB_URI"))
db = client["matchday"]

# Clear existing data
db.matches.drop()
db.venues.drop()
db.teams.drop()

# World Cup 2026 Venues
venues = [
    {"name": "AT&T Stadium", "city": "Dallas", "country": "USA", "capacity": 80000, "timezone": "CST"},
    {"name": "MetLife Stadium", "city": "New York", "country": "USA", "capacity": 82500, "timezone": "EST"},
    {"name": "SoFi Stadium", "city": "Los Angeles", "country": "USA", "capacity": 70240, "timezone": "PST"},
    {"name": "Estadio Azteca", "city": "Mexico City", "country": "Mexico", "capacity": 87523, "timezone": "CST"},
    {"name": "Rose Bowl", "city": "Pasadena", "country": "USA", "capacity": 92542, "timezone": "PST"},
    {"name": "Arrowhead Stadium", "city": "Kansas City", "country": "USA", "capacity": 76416, "timezone": "CST"},
    {"name": "Levi's Stadium", "city": "San Francisco", "country": "USA", "capacity": 68500, "timezone": "PST"},
    {"name": "Hard Rock Stadium", "city": "Miami", "country": "USA", "capacity": 65326, "timezone": "EST"},
    {"name": "Estadio Akron", "city": "Guadalajara", "country": "Mexico", "capacity": 46232, "timezone": "CST"},
    {"name": "BC Place", "city": "Vancouver", "country": "Canada", "capacity": 54500, "timezone": "PST"},
    {"name": "BMO Field", "city": "Toronto", "country": "Canada", "capacity": 45736, "timezone": "EST"},
    {"name": "Stade Olympique", "city": "Montreal", "country": "Canada", "capacity": 66308, "timezone": "EST"},
]

# World Cup 2026 Teams (48 teams)
teams = [
    {"name": "Brazil", "group": "A", "confederation": "CONMEBOL", "fifa_ranking": 5},
    {"name": "Argentina", "group": "A", "confederation": "CONMEBOL", "fifa_ranking": 1},
    {"name": "France", "group": "B", "confederation": "UEFA", "fifa_ranking": 2},
    {"name": "England", "group": "B", "confederation": "UEFA", "fifa_ranking": 4},
    {"name": "Spain", "group": "C", "confederation": "UEFA", "fifa_ranking": 3},
    {"name": "Germany", "group": "C", "confederation": "UEFA", "fifa_ranking": 6},
    {"name": "Portugal", "group": "D", "confederation": "UEFA", "fifa_ranking": 7},
    {"name": "Netherlands", "group": "D", "confederation": "UEFA", "fifa_ranking": 8},
    {"name": "USA", "group": "E", "confederation": "CONCACAF", "fifa_ranking": 11},
    {"name": "Mexico", "group": "E", "confederation": "CONCACAF", "fifa_ranking": 15},
    {"name": "Nigeria", "group": "F", "confederation": "CAF", "fifa_ranking": 28},
    {"name": "Senegal", "group": "F", "confederation": "CAF", "fifa_ranking": 20},
    {"name": "Morocco", "group": "G", "confederation": "CAF", "fifa_ranking": 14},
    {"name": "Japan", "group": "G", "confederation": "AFC", "fifa_ranking": 17},
    {"name": "South Korea", "group": "H", "confederation": "AFC", "fifa_ranking": 23},
    {"name": "Australia", "group": "H", "confederation": "AFC", "fifa_ranking": 24},
    {"name": "Canada", "group": "I", "confederation": "CONCACAF", "fifa_ranking": 12},
    {"name": "Uruguay", "group": "I", "confederation": "CONMEBOL", "fifa_ranking": 13},
    {"name": "Colombia", "group": "J", "confederation": "CONMEBOL", "fifa_ranking": 9},
    {"name": "Belgium", "group": "J", "confederation": "UEFA", "fifa_ranking": 10},
]

# World Cup 2026 Group Stage Matches
matches = [
    {"match_id": "M001", "home_team": "Argentina", "away_team": "Nigeria", "venue": "AT&T Stadium", "city": "Dallas", "date": "2026-06-11", "time": "15:00", "group": "A", "stage": "Group Stage", "ticket_price_usd": 150},
    {"match_id": "M002", "home_team": "Brazil", "away_team": "Mexico", "venue": "SoFi Stadium", "city": "Los Angeles", "date": "2026-06-12", "time": "18:00", "group": "B", "stage": "Group Stage", "ticket_price_usd": 180},
    {"match_id": "M003", "home_team": "France", "away_team": "USA", "venue": "MetLife Stadium", "city": "New York", "date": "2026-06-13", "time": "20:00", "group": "C", "stage": "Group Stage", "ticket_price_usd": 200},
    {"match_id": "M004", "home_team": "Spain", "away_team": "Japan", "venue": "Hard Rock Stadium", "city": "Miami", "date": "2026-06-14", "time": "17:00", "group": "D", "stage": "Group Stage", "ticket_price_usd": 160},
    {"match_id": "M005", "home_team": "England", "away_team": "Colombia", "venue": "Rose Bowl", "city": "Pasadena", "date": "2026-06-15", "time": "19:00", "group": "E", "stage": "Group Stage", "ticket_price_usd": 175},
    {"match_id": "M006", "home_team": "Germany", "away_team": "Morocco", "venue": "Arrowhead Stadium", "city": "Kansas City", "date": "2026-06-16", "time": "16:00", "group": "F", "stage": "Group Stage", "ticket_price_usd": 155},
    {"match_id": "M007", "home_team": "Portugal", "away_team": "Senegal", "venue": "Levi's Stadium", "city": "San Francisco", "date": "2026-06-17", "time": "18:00", "group": "G", "stage": "Group Stage", "ticket_price_usd": 165},
    {"match_id": "M008", "home_team": "Netherlands", "away_team": "South Korea", "venue": "BC Place", "city": "Vancouver", "date": "2026-06-18", "time": "15:00", "group": "H", "stage": "Group Stage", "ticket_price_usd": 145},
    {"match_id": "M009", "home_team": "USA", "away_team": "Nigeria", "venue": "AT&T Stadium", "city": "Dallas", "date": "2026-06-19", "time": "20:00", "group": "I", "stage": "Group Stage", "ticket_price_usd": 190},
    {"match_id": "M010", "home_team": "Brazil", "away_team": "Argentina", "venue": "Estadio Azteca", "city": "Mexico City", "date": "2026-06-20", "time": "21:00", "group": "A", "stage": "Group Stage", "ticket_price_usd": 250},
    {"match_id": "M011", "home_team": "France", "away_team": "England", "venue": "MetLife Stadium", "city": "New York", "date": "2026-06-21", "time": "20:00", "group": "B", "stage": "Group Stage", "ticket_price_usd": 220},
    {"match_id": "M012", "home_team": "Spain", "away_team": "Germany", "venue": "SoFi Stadium", "city": "Los Angeles", "date": "2026-06-22", "time": "19:00", "group": "C", "stage": "Group Stage", "ticket_price_usd": 210},
    {"match_id": "QF001", "home_team": "TBD", "away_team": "TBD", "venue": "MetLife Stadium", "city": "New York", "date": "2026-07-04", "time": "18:00", "group": "N/A", "stage": "Quarter Final", "ticket_price_usd": 350},
    {"match_id": "QF002", "home_team": "TBD", "away_team": "TBD", "venue": "AT&T Stadium", "city": "Dallas", "date": "2026-07-05", "time": "18:00", "group": "N/A", "stage": "Quarter Final", "ticket_price_usd": 350},
    {"match_id": "SF001", "home_team": "TBD", "away_team": "TBD", "venue": "Rose Bowl", "city": "Pasadena", "date": "2026-07-14", "time": "20:00", "group": "N/A", "stage": "Semi Final", "ticket_price_usd": 500},
    {"match_id": "SF002", "home_team": "TBD", "away_team": "TBD", "venue": "MetLife Stadium", "city": "New York", "date": "2026-07-15", "time": "20:00", "group": "N/A", "stage": "Semi Final", "ticket_price_usd": 500},
    {"match_id": "FINAL", "home_team": "TBD", "away_team": "TBD", "venue": "MetLife Stadium", "city": "New York", "date": "2026-07-19", "time": "18:00", "group": "N/A", "stage": "Final", "ticket_price_usd": 1000},
]

# Insert all data
db.venues.insert_many(venues)
db.teams.insert_many(teams)
db.matches.insert_many(matches)

print(f"Loaded {db.venues.count_documents({})} venues")
print(f"Loaded {db.teams.count_documents({})} teams")
print(f"Loaded {db.matches.count_documents({})} matches")
print("World Cup 2026 data loaded successfully!")