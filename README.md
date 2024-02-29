# Timezone

Search the country name or timezone to get the current date and time.  

## usage

- Require Python 3
- Download and run it (it use JSON data as fallback database from external Source)

```sh

wget https://raw.githubusercontent.com/sanwebinfo/timezone/main/wt.py

python wt.py

or

python3 wt.py

```

- install locally
- it uses the sqlite3 database from locally installed source

```sh

## Clone the Repo
git clone https://github.com/sanwebinfo/timezone.git
cd timezone

## install Modules
python3 -m pip install -r requirements.txt

or

python -m pip install -r requirements.txt

## Run the CLI
python wt.py

or

python3 wt.py

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
