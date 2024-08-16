import csv
import json

import requests


# Fetch game from the provided URL with error handling.
def fetch_game_schedules(url):
    """
    Fetch game from the provided URL with error handling.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching data from {url}: {e}")
        return []
    except (KeyError, IndexError, json.JSONDecodeError) as e:
        print(f"Error processing data from {url}: {e}")
        return []


# Fetch game data from the gamePk with error handling.
def fetch_game_data(gamePk):
    """
    Fetch game data from the gamePk with error handling.
    """
    try:
        response = requests.get(
            f"https://statsapi.mlb.com/api/v1/game/{gamePk}/content")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching data from {gamePk}: {e}")
        return []
    except (KeyError, IndexError, json.JSONDecodeError) as e:
        print(f"Error processing data from {gamePk}: {e}")
        return []


# Extract required game information and return as a dictionary.
def extract_game_schedule_info(date, game, game_info):
    """
    Extract required game information and return as a dictionary.
    """

    # Extract the highlight first item from the game info data.
    highlights_item = game_info.get("highlights", {}).get(
        "highlights", {}).get("items", [])[0]
    # Extract the first playback item from the highlight item.
    playback = highlights_item.get("playbacks", [])[0]
    # Return the extracted data as a dictionary.
    return {
        "Date": date,
        "Home Team": game.get("teams", {}).get("home", {}).get("team", {}).get("name", "N/A"),
        "Away Team": game.get("teams", {}).get("away", {}).get("team", {}).get("name", "N/A"),
        "Game PK": game.get("gamePk", "N/A"),
        "Headline": highlights_item.get("headline", "N/A"),
        "MP4": playback.get("url", "N/A")
    }


# Save extracted game information to a CSV file.
def save_to_csv(games, filename):
    """
    Save extracted game information to a CSV file.
    """
    # Define the header for the CSV file.
    header = ["Date", "Home Team", "Away Team", "Game PK", "Headline", "MP4"]
    with open(filename, 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(
            output_file, fieldnames=header, delimiter=',', quoting=csv.QUOTE_ALL)
        dict_writer.writeheader()  # Write the header to the CSV file.
        dict_writer.writerows(games)  # Write the game data to the CSV file.


# Main function to read URLs from file, fetch game data, extract required fields, and save to CSV.
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
        # Fetch game schedules from the URL.
        game_schedules = fetch_game_schedules(url)
        date = game_schedules.get("dates", [])[0].get("date", "N/A")
        games = game_schedules.get("dates", [])[0].get("games", [])
        for game in games:
            # Fetch game info data from the gamePk.
            game_info = fetch_game_data(game["gamePk"])
            # Extract game data and append to the list.
            game_data_dict = extract_game_schedule_info(date, game, game_info)
            all_games.append(game_data_dict)

    # Save the extracted game data to a CSV file, if any data is found in all_games.
    if all_games:
        save_to_csv(all_games, filename)
        print(f"Data has been successfully saved to {filename}.")
    else:
        print("No game data found.")


if __name__ == "__main__":
    url_file = "urls.txt"  # The file containing URLs
    filename = "MLBData.csv"  # The output CSV filename
    main(url_file, filename)
