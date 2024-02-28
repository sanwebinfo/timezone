import pytz
import pycountry
import json

def generate_country_timezones_mapping():
    country_timezones = {}
    for country in pycountry.countries:
        if hasattr(country, 'alpha_2'):
            country_code = country.alpha_2
            country_name = country.name
            timezones = pytz.country_timezones.get(country_code, [])
            country_timezones[country_name.lower()] = timezones
    return country_timezones

def save_country_timezones_to_json(filename):
    country_timezones = generate_country_timezones_mapping()
    with open(filename, 'w') as file:
        json.dump(country_timezones, file)

if __name__ == "__main__":
    save_country_timezones_to_json("../database/country.json")
    print("Country database has been created and saved to country.json")
