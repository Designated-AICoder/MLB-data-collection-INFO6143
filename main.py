import requests
import csv
import json

def fetch_game_data(url):
    """
    Fetch game data from the provided URL with error handling.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        games = data.get("dates", [])[0].get("games", [])
        return games
    except requests.RequestException as e:
        print(f"Error fetching data from {url}: {e}")
        return []
    except (KeyError, IndexError, json.JSONDecodeError) as e:
        print(f"Error processing data from {url}: {e}")
        return []

def extract_game_info(game):
    """
    Extract required game information and return as a dictionary.
    """
    return {
        "Date": game.get("officialDate", "N/A"),
        "Home Team": game.get("teams", {}).get("home", {}).get("team", {}).get("name", "N/A"),
        "Away Team": game.get("teams", {}).get("away", {}).get("team", {}).get("name", "N/A"),
        "Game PK": game.get("gamePk", "N/A"),
        "Headline": "N/A",  
        "MP4": "N/A"        
    }

def save_to_csv(games, filename):
    """
    Save extracted game information to a CSV file.
    """
    header = ["Date", "Home Team", "Away Team", "Game PK", "Headline", "MP4"]
    with open(filename, 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=header)
        dict_writer.writeheader()
        dict_writer.writerows(games)

def main(url_file, filename):
    """
    Main function to read URLs from file, fetch game data, extract required fields, and save to CSV.
    """
    try:
        with open(url_file, 'r') as file:
            urls = [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        print(f"Error: The file {url_file} was not found.")
        return

    all_games = []
    
    for url in urls:
        games = fetch_game_data(url)
        for game in games:
            game_info = extract_game_info(game)
            all_games.append(game_info)

    if all_games:
        save_to_csv(all_games, filename)
        print(f"Data has been successfully saved to {filename}.")
    else:
        print("No game data found.")

if __name__ == "__main__":
    url_file = "urls.txt"  # The file containing URLs
    filename = "MLBData.csv"
    main(url_file, filename)
