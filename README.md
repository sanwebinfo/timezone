# Timezone

Search the country name or timezone to get the current date and time.  

## usage

- Require Python 3
- Download and run it (it use JSON data as fallback database from external Source)

```sh

## Download the script file
wget https://raw.githubusercontent.com/sanwebinfo/timezone/main/wt.py

## Run the CLI
python wt.py

```

- install locally
- it uses the sqlite3 database from locally installed source

```sh

## Clone the Repo
git clone https://github.com/sanwebinfo/timezone.git
cd timezone

## install Modules
python -m pip install -r requirements.txt

## Run the CLI
python wt.py

```

- Downlaoad timezone database

```sh

## Download database file
curl -sSLfOJ https://github.com/sanwebinfo/timezone/raw/main/database/country.db

## specify the path of the database file
python wt.py ./your_directory/country.db

```

- Learn more about this timezone search CLI

```sh
python wt.py -h
```

## Database

- all the timezone and country zone name was stored in the folder `/database`
- stored as `db`, `JSON`, and `CSV` data files
- Database was built using sqlite3, pytz and pycountry Module

## LICENSE

MIT
