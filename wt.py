import datetime
import json
import os
import sqlite3
import sys
import importlib.util
import pytz
import requests
import time
from yaspin import yaspin

spinner = yaspin(text="Searching...", color="cyan")

packages = ['pytz', 'requests', 'yaspin']
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

def load_country_timezones_from_db(db_file):
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM country_timezones")
        country_timezones = dict(cursor.fetchall())
        conn.close()
        return {country.lower(): json.loads(timezones) for country, timezones in country_timezones.items()}
    except sqlite3.Error as e:
        # print(f"{ERROR_EMOJI} Error loading data from SQLite database: {e}")
        print("ℹ️ load data from fallback sources...")

        fallback_data = load_country_timezones_from_url("https://sanwebinfo.github.io/timezone/database/country.json")
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

def get_timezones_for_country(country, country_timezones):
    country = country.lower()
    matching_countries = [(c, tzs) for c, tzs in country_timezones.items() if country in c]
    if len(matching_countries) == 1:
        return matching_countries[0][1]
    elif len(matching_countries) > 1:
        print("ℹ️ Multiple matches found:")
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
    
def print_help():
    print("\nUsage:")
    print("\npython wt.py or python wt.py [DB_FILE_LOCATION]")
    print("\nArguments:\n")
    print("> python wt.py  # Using External JSON data as fallback database.")
    print("> python wt.py ./database/country.db # DB_FILE Path to the SQLite database file containing country timezones.")
    print('> python wt.py ./database/country.db "country_Name" # Search Timezone with your custom DB_FILE_PATH.')
    print("> Use 'quit' to exit.\n")

def main(db_file="./database/country.db", search_input=None):
    try:

        country_timezones = load_country_timezones_from_db(db_file)
        print("\n")

        if search_input:
            while search_input.lower() != 'quit':
                print("\n")

                if not search_input:
                    print(f"{ERROR_EMOJI} Error: Please enter a country or timezone.")
                    print("\n")
                    break

                spinner.start()
                time.sleep(3) 
                spinner.stop()

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

                search_input = input("Enter a country or timezone to get the current time (or 'quit' to exit): ").strip()

        else:
            while True:
                search_input = input("Enter a country or timezone to get the current time (or 'quit' to exit): ").strip()
                print("\n")

                if search_input.lower() == 'quit':
                    break

                if not search_input:
                    print(f"{ERROR_EMOJI} Error: Please enter a country or timezone.")
                    print("\n")
                    continue

                spinner.start()
                time.sleep(3) 
                spinner.stop()

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
        print("\n")
        print("\nProgram terminated by user.")
        print("\n")
    except Exception as e:
        print("\n")
        print("\nAn error occurred")
        print("\n")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] in ("-h", "--help"):
        print_help()
    else:
        if len(sys.argv) > 2:
            db_file = sys.argv[1]
            search_input = sys.argv[2]
            main(db_file, search_input)
        elif len(sys.argv) > 1:
            db_file = sys.argv[1]
            if not os.path.isfile(db_file):
              print("Error: The specified database file is not a valid file path.")
              sys.exit(1)
            else: 
              main(db_file)
        else:
            main()