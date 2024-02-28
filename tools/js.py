import sqlite3
import json

def sqlite_to_json(db_file, output_file):
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM country_timezones")
        rows = cursor.fetchall()

        conn.close()

        data = []
        for row in rows:
            data.append({
                'country': row[0],
                'timezones': row[1],
            })

        with open(output_file, 'w') as f:
            json.dump(data, f, indent=4)

        print("Data has been successfully converted and written to", output_file)

    except sqlite3.Error as e:
        print("Error:", e)

sqlite_to_json("../database/country.db", "../database/data.json")