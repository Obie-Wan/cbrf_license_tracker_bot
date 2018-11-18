Telegram bot for tracking CBRF license declines (parses official site info)

# Installation
- Install package with requirements
- Install postgresql
- Create bot and make it admin of your channel
- Setup environment variable before starting this module:
  CBRF_LICENSE_TRACKER_TG_API_KEY: telegram bot api key
  CBRF_LICENSE_TRACKER_TG_CHANNEL: your telegram channel for bot reports
  CBRF_LICENSE_TRACKER_DB_PASSWORD: your DB password

Optional:
  CBRF_LICENSE_TRACKER_DB_HOST: your DB host
  CBRF_LICENSE_TRACKER_DB_USER: your DB user
