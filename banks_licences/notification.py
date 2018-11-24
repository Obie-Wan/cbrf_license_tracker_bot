from datetime import datetime
import aiohttp
import logging

logger = logging.getLogger(__name__)


class NotifyManager:
    def __init__(self, notifiers):
        self.notifiers = notifiers

    async def start(self, init_data_dict):
        """Init all notifiers
        :return:
        """
        for notifier in self.notifiers:
            await notifier.start(init_data_dict)

    async def notify(self, data_item_list):
        """Call all notifiers
        :param data_dict:
        :return:
        """
        if not len(data_item_list):
            return

        for notifier in self.notifiers:
            await notifier.notify(data_item_list)


class TelegramNotifier:
    last_request = None

    def __init__(self, api_token, channel):
        """
        :param api_token: bot api token
        :param channel: linke @yourchannel
        """
        from aiotg import Bot, Chat
        self.bot = Bot(api_token=api_token)
        self.channel = self.bot.channel(channel)

        @self.bot.command(r"/last")
        async def last(chat: Chat, match):
            if self.last_request is None:
                self.last_request = datetime.now()

            if self.last_request - datetime.now() < 30:
                # ignore and stop flood
                self.last_request = datetime.now()
                return

            self.last_request = datetime.now()

            engine = self.init_data_dict['engine']
            from banks_licences.database import get_last
            from banks_licences.models import BankSanction

            rows = await get_last(engine, BankSanction.__table__, orderby='date')
            if len(rows):
                await self.notify(rows)

    async def start(self, init_data_dict: dict):
        self.init_data_dict = init_data_dict

    async def notify(self, data_list: list):
        decline_list = []
        for data_item_dict in data_list:
            decline_list.append(
                '{date} "{bank}" {link}\r\n'.format(
                    bank=data_item_dict["name"],
                    date=data_item_dict["date"],
                    link=data_item_dict["url"]
                )
            )

        try:
            await self.channel.send_text(
                'Отозваны лицензии:\r\n\r\n{banks}'.format(
                    banks='\r\n'.join(decline_list)
                )

            )
        except aiohttp.client_exceptions.ClientConnectorError as e:
            logger.exception('unable to notify')
            raise RuntimeError('Unable to notify Telegram dest')

