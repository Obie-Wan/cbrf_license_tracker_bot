#!/usr/bin/python3.6

import logging
import asyncio
from datetime import datetime
from aiohttp import ClientSession
from bs4 import BeautifulSoup

from banks_licences.database import create_sanction
from banks_licences import settings
from banks_licences.helpers import localize_date, set_logging
from banks_licences.notification import NotifyManager


set_logging(log_level=settings.LOG_LEVEL, log_format=settings.LOG_FORMAT)
logger = logging.getLogger(__name__)


async def get_check_result(url, session, filter_text='отзыве'):
    """parse sanction page"""
    body = await fetch(url, session)
    soup = BeautifulSoup(body, "html.parser")
    div1 = soup.find('div', attrs={'id': 'content'})

    c = div1.find('table', attrs={'class': 'data'})
    if not c:
        c = div1.find('p')

    if str(c.contents).find(filter_text) != -1:
        sanction_data = c.contents[0].split('\r\n')
        organisation = sanction_data[3]
        date = localize_date(sanction_data[2].split('года')[0].strip())
        date = datetime.strptime(date, '%d %m %Y').date()

        if organisation.endswith(','):
            organisation = organisation[:-1]
        logging.info('date: %s, name: %s, link: %s', date, organisation.strip(), url)
        return {'date': date, 'name': organisation.strip(), 'url': url}


async def get_urls(session):
    urls = []

    body = await fetch(settings.CBR_URL, session)
    soup = BeautifulSoup(body, "html.parser")

    div1_sanctions = soup.find('ul', attrs={'class': 'without_dash without_indent'})
    arr = div1_sanctions.findAll('a', href=True, target='_blank')
    for url in arr:        
        urls.append('{}{}'.format(settings.CBR_URL, url['href']))
            
    return urls


async def fetch(url, session):
    try:
        async with session.get(url) as response:
            body = await response.read()
            logger.info('%s', url)
            return body
    except Exception as e:
      logger.exception('unable to fetch data')
      raise RuntimeError('unable to fetch data')


async def run(engine, notify_manager: NotifyManager):
    """"""
    tasks = []
    new_item_list = []
    stopped = False
    logger.info('Started')

    await notify_manager.start({'engine': engine})

    while not stopped:
        async with ClientSession() as session:
            urls = await get_urls(session)
            logger.info('fetching %s', urls)
            for url in urls:
                task = asyncio.ensure_future(get_check_result(url, session))
                tasks.append(task)

            responses = await asyncio.gather(*tasks)
            logging.debug(responses)

            for response_dict in responses:
                if response_dict is not None:
                    created = await create_sanction(engine, response_dict)
                    if created:
                        new_item_list.append(response_dict)

            logger.info('Created %d items', len(new_item_list))
            await notify_manager.notify(new_item_list)
            new_item_list = []

            logger.info('Sleeping ...')
            await asyncio.sleep(settings.SLEEP_INTERVAL)

