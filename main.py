import csv
import json

import requests


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


def fetch_game_data(gamePk):
    """
    Fetch game data from the provided URL with error handling.
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


def extract_game_schedule_info(date, game, game_info):
    """
    Extract required game information and return as a dictionary.
    """
    highlights_item = game_info.get("highlights", {}).get(
        "highlights", {}).get("items", [])[0]
    playback = highlights_item.get("playbacks", [])[0]
    return {
        "Date": date,
        "Home Team": game.get("teams", {}).get("home", {}).get("team", {}).get("name", "N/A"),
        "Away Team": game.get("teams", {}).get("away", {}).get("team", {}).get("name", "N/A"),
        "Game PK": game.get("gamePk", "N/A"),
        "Headline": highlights_item.get("headline", "N/A"),
        "MP4": playback.get("url", "N/A")
    }
    # game_data_dict = []
    # highlights_items = game_info.get("highlights", {}).get(
    #     "highlights", {}).get("items", [])
    # for item in highlights_items:
    #     playbacks = item.get("playbacks", [])
    #     for playback in playbacks:
    #         game_data_dict.append({
    #             "Date": date,
    #             "Home Team": game.get("teams", {}).get("home", {}).get("team", {}).get("name", "N/A"),
    #             "Away Team": game.get("teams", {}).get("away", {}).get("team", {}).get("name", "N/A"),
    #             "Game PK": game.get("gamePk", "N/A"),
    #             "Headline": item.get("headline", "N/A"),
    #             "MP4": playback.get("url", "N/A")
    #         })
    # return game_data_dict


def save_to_csv(games, filename):
    """
    Save extracted game information to a CSV file.
    """
    header = ["Date", "Home Team", "Away Team", "Game PK", "Headline", "MP4"]
    with open(filename, 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(
            output_file, fieldnames=header, delimiter=',', quoting=csv.QUOTE_ALL)
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
        game_schedules = fetch_game_schedules(url)
        date = game_schedules.get("dates", [])[0].get("date", "N/A")
        games = game_schedules.get("dates", [])[0].get("games", [])
        for game in games:
            game_info = fetch_game_data(game["gamePk"])
            game_data_dict = extract_game_schedule_info(date, game, game_info)
            all_games.append(game_data_dict)

    if all_games:
        save_to_csv(all_games, filename)
        print(f"Data has been successfully saved to {filename}.")
    else:
        print("No game data found.")


if __name__ == "__main__":
    url_file = "urls.txt"  # The file containing URLs
    filename = "MLBData.csv"
    main(url_file, filename)
