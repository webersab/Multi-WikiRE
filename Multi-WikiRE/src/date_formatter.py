import datetime
import locale
from abc import ABC

import numeral
from dateutil.parser import parse
from natural.number import ordinal

MILLENNIUM_TOKEN = {
    'en': '{millennium} millennium {era}',
    'fr': '{millennium}e millénaire {era}',
    'it': '{millennium} millennio {era}',
    'es': '{millennium} milenio {era}',
    'de': '{millennium}. Jahrtausend {era}'
}

CENTURY_TOKEN = {
    'en': '{century} century {era}',
    'fr': '{century}e siècle {era}',
    'it': '{century} secolo {era}',
    'es': 'siglo {century} {era}',
    'de': '{century}. Jahrhundert {era}'
}

BC_TOKEN = {
    'en': 'BC',
    'fr': 'J.-C',
    'it': 'a.C.',
    'es': 'a. C.',
    'de': 'v. Chr.'
}

MONTH_TEMPLATE = {
    'es': '%B de %#Y'
}

DAY_TEMPLATE = {
    'es': "%#d de %B de %#Y",
    'de': "%#d. %B %#Y",
    'it': "%#d{suff} %B %#Y",
    'fr': "%#d{suff} %B %#Y"
}

DAY_SUFFIX = {
    'it': {1: '°'},
    'fr': {1: 'er'}
}


class DateFormatter(ABC):
    def __init__(self, lang='en', out_locale="en-US"):
        self._default_datetime = datetime.datetime(1, 1, 1)
        self._precisions = {
            6: self._parse_millennium,
            7: self._parse_century,
            9: self._parse_year,
            10: self._parse_month,
            11: self._parse_day
        }

        if out_locale:
            locale.setlocale(locale.LC_TIME, out_locale)
        self._BCE_TOKEN = BC_TOKEN[lang]
        self._millenium_template = MILLENNIUM_TOKEN.get(lang, "")
        self._century_template = CENTURY_TOKEN.get(lang, "")
        self._day_template = DAY_TEMPLATE.get(lang, "%#d %B %#Y")
        self._month_template = MONTH_TEMPLATE.get(lang, "%B %#Y")
        self._year_template = "{year} {era}"
        self._day_suffix = DAY_SUFFIX.get(lang, False)

    def format(self, date: str, precision: int):
        if date.startswith("-"):
            era = self._BCE_TOKEN
        else:
            era = ""
        formatted = self._precisions.get(precision, self._default_parse)(date[1:], era)
        return formatted

    def _default_parse(self, date, era=""):
        year = date.split("-")[0]
        return self._year_template.format(year=year, era=era)

    def _parse_millennium(self, date, era=""):
        year = int(int(date.split("-")[0]) / 1000) + 1
        millennium = self.to_human(year)
        return self._millenium_template.format(millennium=millennium, era=era).strip()

    def _parse_century(self, date, era=""):
        year = int(int(date.split("-")[0]) / 100) + 1
        century = self.to_human(year)
        return self._century_template.format(century=century, era=era).strip()

    def _parse_year(self, date, era=""):
        year = int(date.split("-")[0])
        return self._year_template.format(year=year, era=era).strip()

    def _parse_month(self, date, era=""):
        splitted_date = date.split('-')
        year = int(splitted_date[0])
        month = int(splitted_date[1])
        date = datetime.datetime(year, month, 1)
        formatted = date.strftime(self._month_template) + " " + era
        return formatted.strip()

    def _parse_day(self, date, era=""):
        date = parse(date)
        formatted = date.strftime(self._day_template) + " " + era
        if self._day_suffix:
            if date.day in self._day_suffix:
                suff = self._day_suffix[date.day]
            else:
                suff = ''
            formatted = formatted.format(suff=suff)

        return formatted.strip()

    def to_human(self, value):
        return int(value)


class EnglishDateFormatter(DateFormatter):
    def to_human(self, value):
        return ordinal(int(value))


class RomanLanguageDateFormatter(DateFormatter):
    def to_human(self, value):
        return numeral.int2roman(int(value), only_ascii=True)


class DateFormatterFactory(object):
    @staticmethod
    def get_formatter(lang, out_locale):
        if lang in ['en']:
            return EnglishDateFormatter(lang, out_locale)
        elif lang in ['de']:
            return DateFormatter(lang, out_locale)
        else:
            return RomanLanguageDateFormatter(lang, out_locale)
