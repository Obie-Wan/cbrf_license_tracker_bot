import logging
import os

# database settings
DATABASE_NAME = os.environ.get('CBRF_LICENSE_TRACKER_DB_NAME', 'bank_sanctions')
DB_HOST = os.environ.get('CBRF_LICENSE_TRACKER_DB_HOST', '127.0.0.1')
DB_USER = os.environ.get('CBRF_LICENSE_TRACKER_DB_USER', 'postgres')
DB_PASSWORD = os.environ.get('CBRF_LICENSE_TRACKER_DB_PASSWORD', '')

# log settings
LOG_LEVEL = logging.INFO
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

# notification settings
# telegram
TG_API_KEY = os.environ['CBRF_LICENSE_TRACKER_TG_API_KEY']
TG_HOME_CHANNEL = os.environ['CBRF_LICENSE_TRACKER_TG_CHANNEL']

# misc settings
CBR_URL = 'http://cbr.ru/analytics/insideinfo/'
SLEEP_INTERVAL = 15 * 60 # every 15 minutes

