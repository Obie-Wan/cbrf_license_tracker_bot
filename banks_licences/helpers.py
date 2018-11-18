import logging


def localize_date(date):
    """replace russian months to numeric"""
    month_dict = {
        'января': 1,
        'февраля': 2,
        'марта': 3,
        'апреля': 4,
        'мая': 5,
        'июня': 6,
        'июля': 7,
        'августа': 8,
        'сентября': 9,
        'октября': 10,
        'ноября': 11,
        'декабря':12
    }
    d, m, y = date.split()
    return '{} {} {}'.format(d, month_dict[m], y)


def set_logging(log_level=logging.INFO, log_format=None):
    logging.basicConfig(level=log_level,
                        format=log_format)

