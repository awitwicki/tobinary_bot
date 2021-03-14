# tobinary_bot
Telegram bot for converting number values

## Install

```python
    pip install -r requirements.txt
```

Fill credentials at `main.py` and run

```python
    token ='TELEGRAM_BOT_TOKEN'
    admin_id = 9379992 #Your telegram id
    influx_db_address = 'http://server_address:8086/write?db=database_name'
    influx_db_credentials = 'login:password'
```

What is [influxDB](https://www.influxdata.com/)?