import datetime
import json
import sqlite3
import sys
import csv
import importlib.util
import pytz
import requests

packages = ['pytz', 'requests']
missing_packages = [package for package in packages if importlib.util.find_spec(package) is None]

if missing_packages:
    print("The following required packages are missing:")
    for package in missing_packages:
        print(f"- {package}")
    
    try:
        install_prompt = input("Do you want to install these packages? (yes/no): ")
    except KeyboardInterrupt:
        print("\nInstallation process interrupted.")
        sys.exit(0)
    if install_prompt.lower() == 'yes':
        try:
            import subprocess
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', *missing_packages])
        except Exception as e:
            print(f"Error installing packages: {e}")
            sys.exit(1)
        except KeyboardInterrupt:
           print("\nScript terminated by user.")
           sys.exit(0)
    else:
        print("Please install the required packages manually and rerun the script.")
        sys.exit(1)

GREEN = "\033[92m"
BLUE = "\033[94m"
RED = "\033[91m"
RESET = "\033[0m"

ERROR_EMOJI = "❌"
INFO_EMOJI = "ℹ️"

def load_country_timezones_from_db(db_file):
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM country_timezones")
        country_timezones = dict(cursor.fetchall())
        conn.close()
        return {country.lower(): json.loads(timezones) for country, timezones in country_timezones.items()}
    except sqlite3.Error as e:
        print(f"{ERROR_EMOJI} Error loading data from SQLite database: {e}")
        print(f"{INFO_EMOJI} Attempting to load from fallback sources...")

        fallback_data = load_country_timezones_from_url("")
        if fallback_data:
            return fallback_data

        fallback_data = load_country_timezones_from_json("")
        if fallback_data:
            return fallback_data

        fallback_data = load_country_timezones_from_csv("")
        if fallback_data:
            return fallback_data

        return {}

def load_country_timezones_from_url(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return {country.lower(): timezones for country, timezones in data.items()}
        else:
            print(f"{ERROR_EMOJI} Error loading data from URL: {response.status_code}")
            return None
    except Exception as e:
        print(f"{ERROR_EMOJI} Error loading data from URL: {e}")
        return None

def load_country_timezones_from_json(json_file):
    try:
        with open(json_file, "r") as file:
            data = json.load(file)
            return {country.lower(): timezones for country, timezones in data.items()}
    except FileNotFoundError:
        print(f"{ERROR_EMOJI} JSON file not found: {json_file}")
        return None
    except Exception as e:
        print(f"{ERROR_EMOJI} Error loading data from JSON file: {e}")
        return None

def load_country_timezones_from_csv(csv_file):
    try:
        with open(csv_file, "r") as file:
            reader = csv.DictReader(file)
            data = {row["country"].lower(): json.loads(row["timezones"]) for row in reader}
            return data
    except FileNotFoundError:
        print(f"{ERROR_EMOJI} CSV file not found: {csv_file}")
        return None
    except Exception as e:
        print(f"{ERROR_EMOJI} Error loading data from CSV file: {e}")
        return None

def get_timezones_for_country(country, country_timezones):
    country = country.lower()
    matching_countries = [(c, tzs) for c, tzs in country_timezones.items() if country in c]
    if len(matching_countries) == 1:
        return matching_countries[0][1]
    elif len(matching_countries) > 1:
        print(f"{INFO_EMOJI} Multiple matches found:")
        print("\n")
        for matched_country, timezones in matching_countries:
            print(f"{BLUE}{matched_country.capitalize()}:")
            for timezone in timezones:
                time_now = get_world_time(timezone)
                if time_now is not None:
                    print(f"- {timezone}: {time_now}")
            print(RESET)
        return None
    else:
        print(f"{ERROR_EMOJI} No matches found.")
        print("\n")
        return None

def get_world_time(timezone):
    try:
        tz = pytz.timezone(timezone)
        local_time = datetime.datetime.now(tz)
        time_format = "%A, %Y-%m-%d %I:%M:%S %p"
        return local_time.strftime(time_format)
    except pytz.UnknownTimeZoneError as e:
        print(f"{ERROR_EMOJI} Error: Unknown timezone '{timezone}': {e}")
        print("\n")
        return None

def main():
    try:
        country_timezones = load_country_timezones_from_db("./database/country.db")
        print("\n")
        search_input = input("Enter a country or timezone to get the current time: ")
        print("\n")
        search_input = search_input.strip()
        if not search_input:
            print(f"{ERROR_EMOJI} Error: Please enter a country or timezone.")
            print("\n")
            return

        timezones = None
        if '/' in search_input:
            timezones = [search_input]
        else: 
            timezones = get_timezones_for_country(search_input, country_timezones)

        if timezones is not None:
            for timezone in timezones:
                time_now = get_world_time(timezone)
                if time_now is not None:
                    print(f"The current time in {GREEN}{timezone}{RESET} is: {RED}{time_now}{RESET}")
                    print("\n")
    except KeyboardInterrupt:
        print("\nProgram terminated by user.")

if __name__ == "__main__":
    main()
