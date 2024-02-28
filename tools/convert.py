import json
import sqlite3

def create_country_timezones_table(cursor):
    cursor.execute('''CREATE TABLE IF NOT EXISTS country_timezones (
                        country TEXT PRIMARY KEY,
                        timezones TEXT
                      )''')

def insert_country_timezones(cursor, country, timezones):
    cursor.execute("INSERT OR REPLACE INTO country_timezones (country, timezones) VALUES (?, ?)", (country, json.dumps(timezones)))

def convert_json_to_sqlite(json_file, db_file):
    with open(json_file, 'r') as file:
        country_timezones = json.load(file)

    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    create_country_timezones_table(cursor)

    for country, timezones in country_timezones.items():
        insert_country_timezones(cursor, country, timezones)

    conn.commit()
    conn.close()

    print(f"Data from {json_file} has been successfully converted and saved to {db_file}.")

if __name__ == "__main__":
    convert_json_to_sqlite("../database/country.json", "../database/country.db")
