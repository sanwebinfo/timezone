import pycountry
import pytz

def get_full_timezone_database():
    timezone_dict = {}
    for country in pycountry.countries:
        country_name = country.name
        timezones = pytz.country_timezones.get(country.alpha_2, [])
        timezone_dict[country_name] = timezones
    return timezone_dict

timezone_database = get_full_timezone_database()
for country, timezones in timezone_database.items():
    print(f"{country}: {', '.join(timezones)}")
