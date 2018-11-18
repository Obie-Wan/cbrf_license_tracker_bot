Telegram bot for tracking CBRF license declines.

Retranslates bank licensing info from official site http://cbr.ru into selected telegram channel.

# Installation
- Install package with requirements
- Install postgresql
- Create bot and make it admin of your channel
- Setup environment variables before starting this module:
  1. CBRF_LICENSE_TRACKER_TG_API_KEY: telegram bot api key
  2. CBRF_LICENSE_TRACKER_TG_CHANNEL: your telegram channel for bot reports
  3. CBRF_LICENSE_TRACKER_DB_PASSWORD: your DB password

- Optional variables:
  1. CBRF_LICENSE_TRACKER_DB_HOST: your DB host
  2. CBRF_LICENSE_TRACKER_DB_USER: your DB user

# Running
- Init DB: ```python -m banks_licenses --init```
- Run module: ```python -m banks_licenses```

