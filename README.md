# reddit-scraper

## About ##
This project is designed to interact with Reddit and facilitate the bulk download of videos from a specific subreddit.

## Development Setup ##

### Prerequisites ###
- Install [Python](https://www.python.org/downloads/)

### Project Setup ###
In order to have a easy transaction the best, that can be do it's create a new `env` in order to use this project.

```shell
python -m venv env
```

Once the virtual environment is set up, activate it and install all necessary dependencies:

```shell
#For Linux
source env/bin/activate
pip install -r requirements.txt
```

### Run Script ###
To execute the script, pass the subreddit URL as an argument to Python:
```shell
#For Linux
python main <subredit_url>
```
> NOTE: Make sure to replace <subreddit_url> with the actual URL of the subreddit you want to scrape.


