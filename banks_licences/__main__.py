import sys
import asyncio

from banks_licences.database import get_engine, create_table
from banks_licences.checker import run
from banks_licences import settings
from banks_licences.models import BankSanction
from banks_licences.notification import NotifyManager, TelegramNotifier


def main(args):
    loop = asyncio.get_event_loop()
    engine = loop.run_until_complete(get_engine(settings.DATABASE_NAME,
                                                user=settings.DB_USER,
                                                password=settings.DB_PASSWORD))

    if '--init' in args:
        loop.run_until_complete(create_table(engine, BankSanction.__tablename__))
        return

    nm = NotifyManager([
        TelegramNotifier(settings.TG_API_KEY, settings.TG_HOME_CHANNEL)]
    )
    future = asyncio.ensure_future(run(engine, nm))
    loop.run_until_complete(future)


if __name__ == '__main__':
    main(sys.argv)
