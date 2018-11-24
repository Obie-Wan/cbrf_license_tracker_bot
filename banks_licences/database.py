from sqlalchemy.sql.expression import ClauseElement
from aiopg.sa import create_engine
import logging

from banks_licences.models import BankSanction

logger = logging.getLogger(__name__)


async def create_table(engine, name):
    async with engine.acquire() as conn:
        await conn.execute('DROP TABLE IF EXISTS {}'.format(name))
        await conn.execute('''CREATE TABLE {} (
                                  id serial PRIMARY KEY,
                                  name varchar(255) UNIQUE NOT NULL,
                                  url varchar(255) UNIQUE NOT NULL,
                                  date DATE NOT NULL)'''.format(name))


async def get_engine(database, user='', password='', host='127.0.0.1'):
    return await create_engine('postgresql://{user}:{pwd}@{host}/{db}'.format(
        user=user,
        pwd=password,
        host=host,
        db=database
    ))


async def get_last(engine, table, limit=5, orderby='id'):
    async with engine.acquire() as conn:
        results = [x for x in
                   await conn.execute(table.select().order_by(
                       getattr(table.c, orderby)).limit(limit))]
        return results


async def get_or_create(conn, table, defaults=None, **kwargs):
        row = None
        #expressions = {getattr(table.c, k): v for k, v in kwargs.items()}
        results = [x for x in await conn.execute(table.select().where(table.c.url == kwargs['url']))]
        if len(results):
            return False
        else:
            params = dict((k, v) for k, v in kwargs.items() if not isinstance(v, ClauseElement))
            params.update(defaults or {})
            await conn.execute(table.insert().values(**params))
            return True


async def create_sanction(conn, sanction_dict: dict) -> tuple:
        return await get_or_create(conn, BankSanction.__table__,
                                   defaults=sanction_dict,
                                   url=sanction_dict['url'])

