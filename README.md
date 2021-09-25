# tobinary_bot
Telegram bot for converting number values

## Install


Use next environment variables:

* `TOBINARYBOT_TELEGRAM_TOKEN={YOUR_TOKEN}` - telegram token
* `TOBINARYBOT_INFLUX_QUERY={URL}` - url for [influxDB](https://www.influxdata.com/) logging, bot won't log metrics if that URL not defined.

**Python:** Add to system environment that variables.

**Docker compose:**  create `.env` file and fill it with that variables.

## Run

### Docker compose

Then run in console command:

```
docker-compose up -d
```

### Python

```
pip3 install -r requirements.txt
python main.py
```
