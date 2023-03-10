import email
import imaplib
import importlib
import logging
import re
import glob
import os
import shutil
import time
from datetime import datetime, timedelta, date
from decimal import Decimal
from email.header import decode_header
from pathlib import Path
from typing import Union

import math
from dateutil import relativedelta
import requests

logger = logging.getLogger(__name__)


class Tools:
    @staticmethod
    def convert_text_from_dict(text: str, data: dict):
        """
        Replace all '<.*>' in text
        e.g submit_btn = "//button[.='<button_text>']", data = {"button_text": "Submit"}
        submit_btn = convert_text_from_dict(submit_btn, data)
        submit_btn = "//button[.='Submit']
        @param text: text need to convert
        @param data: a map store all possible values can be converted
        @return: converted text
        """
        r = re.compile("[<>]+").findall(text)
        if len(r) == 0:
            return text

        r = re.compile("(<.*?>)").findall(text)
        keys = data.keys()

        for v in r:
            key = v.replace("<", "").replace(">", "")
            if key in keys:
                after = str(data[key])
                text = text.replace(v, after)

        return text

    @staticmethod
    def covert_datetime_fmt(from_fmt: str, time_str: str, to_fmt: str):
        """
        Convert a datetime from fmt1 to fmt2
        e.g from_fmt = "%b, %Y %d", time_str = "Dec, 2021 12", to_fmt = "%Y-%m-%d"
        t_str = covert_datetime_fmt(from_fmt, time_str, to_fmt)
        t_str = 2021-11-12
        @param from_fmt: time str current format
        @param time_str: time str to convert
        @param to_fmt: time str format to convert
        @return: new time str
        """
        time_format = datetime.strptime(time_str, from_fmt)
        t_str = time_format.strftime(to_fmt)
        return t_str

    @staticmethod
    def match_text_by_re(pattern: str, text: str, re_type: str = "match", first_groups: bool = False):
        if re_type == "search":
            r = re.compile(pattern).search(text)
        else:
            r = re.compile(pattern).match(text)
        if r is not None:
            if first_groups:
                return r.groups()[0]
            return r.group()
        return None

    @staticmethod
    def remove_fuzzy_dir(base_dir: str, fzy_name: str):
        """
        remove_fuzzy_dir(base_dir, "payments_*.csv") will delete all payments_*.csv files
        remove_fuzzy_dir(base_dir, "payments_*") will delete all files and folder name payments_*
        @param base_dir: root path of the files and folders
        @param fzy_name: fuzzy expression
        """
        tmp_dirs = Tools.get_fuzzy_dirs(base_dir, fzy_name)
        if len(tmp_dirs) > 0:
            for tmp_dir in tmp_dirs:
                tmp_path = Path(tmp_dir)
                if tmp_path.is_dir():
                    shutil.rmtree(tmp_path)
                if tmp_path.is_file():
                    tmp_path.unlink(missing_ok=True)

    @staticmethod
    def get_fuzzy_dirs(base_dir: str, fzy_name: str):
        return glob.glob(os.path.join(base_dir, fzy_name))

    @staticmethod
    def keep_float(num: Union[float, str, Decimal], index: int, remove_zero: bool = False):
        a, b, c = str(num).partition(".")
        c = (c + index * "0")[:index]
        result = ".".join([a, c])

        if remove_zero:
            for r in reversed(result):
                if r == ".":
                    result = result[:-1]
                    break
                if result[-1] != "0":
                    return result
                if r == "0":
                    result = result[:-1]
        return result

    @staticmethod
    def get_expected_send_on_date_by_weeks(week_day_str: str):
        w_map = {"Monday": 1, "Tuesday": 2, "Wednesday": 3, "Thursday": 4, "Friday": 5, "Saturday": 6, "Sunday": 7}
        expected_week_day = w_map.get(week_day_str)
        today_week_day = date.today().weekday() + 1
        if expected_week_day <= today_week_day:  # get next weeks date
            expected_week_date = Tools.get_next_weeks_date_by_str(next_weeks=1, week_day_str=week_day_str)
        else:  # get this week's
            day_dalta = expected_week_day - today_week_day
            expected_week_date = date.today() + timedelta(days=day_dalta)
        return expected_week_date

    @staticmethod
    def get_next_weeks_date_by_str(next_weeks: int = 1, week_day_str: str = "Monday"):
        w_map = {"Monday": 1, "Tuesday": 2, "Wednesday": 3, "Thursday": 4, "Friday": 5, "Saturday": 6, "Sunday": 7}
        expected_week_day = w_map.get(week_day_str)
        today = date.today()
        next_weeks_date = today + timedelta(weeks=next_weeks)
        next_weeks_day = next_weeks_date.weekday() + 1

        if expected_week_day == next_weeks_day:
            return next_weeks_date
        else:
            interval = expected_week_day - next_weeks_day
            next_weeks_date += timedelta(days=interval)
            return next_weeks_date

    @staticmethod
    def get_next_month_date_by_index(next_month: int = 1, day_index: int = 1):
        today = date.today()
        if today.day >= 6:
            next_month_by_index = today + relativedelta.relativedelta(months=next_month, day=day_index)
        else:
            next_month_by_index = today + relativedelta.relativedelta(day=day_index)
        return next_month_by_index

    @staticmethod
    def get_suffix_by_day(day: int):
        if 4 <= day <= 20 or 24 <= day <= 30:
            suffix = "th"
        else:
            suffix = ["st", "nd", "rd"][day % 10 - 1]
        return suffix

    @staticmethod
    def get_random_int_from_list(a_list: list):
        from random import randint

        count = len(a_list) - 1
        index = 0 if count == 0 else randint(0, count)
        return index

    @staticmethod
    def sleep(timeout: int = 0.5, sleep_type: str = "event"):
        from threading import Event

        if sleep_type == "event":
            e = Event()
            e.wait(timeout=timeout)
        else:
            end_time = time.time() + timeout
            while True:
                if time.time() > end_time:
                    break

    @staticmethod
    def format_email(email_content, length: int = 75, fill_char: str = "="):
        """
        Format email with fixed length and ending with fill_char
        e.g email_content="Crypto.com Pay cannot process a payment (Payment ID: 825bcf0c-4fae-474b-b092-d5cb6b8f1d44"
        formatted_content= format_email(email_content,75,"=")
        formatted_content="
        Crypto.com Pay cannot process a payment (Payment ID: 825bcf0c-4fae-474b-b09=
        2-d5cb6b8f1d44
        "
        @param email_content: email to be formatted
        @param length: character length each line, not including fill_char
        @param fill_char: ending char for each line if char length==length
        @return: formatted email content
        """
        str_list = []
        for i in range(0, len(email_content), length):
            end = length + i
            str_list.append(email_content[i:end])
        new_list = []
        for content in str_list:
            if len(content) == length:
                content += fill_char
            new_list.append(content)
        formatted_email = "\n".join(new_list)
        return formatted_email

    @staticmethod
    def get_curl_format(r: requests.Response):
        method = r.request.method
        uri = r.url
        data = r.request.body
        headers = ['"{0}: {1}"'.format(k, v) for k, v in r.request.headers.items()]
        headers = " -H ".join(headers)
        command = f"curl -X {method} -H {headers} -d '{data}' '{uri}'"
        return command

    @staticmethod
    def get_object(package_name: str, class_name: str):
        obj_p = importlib.import_module(name=package_name)
        obj = obj_p.__getattribute__(class_name)
        return obj

    @staticmethod
    def get_currency_type(tmp_currency: str):
        fiat_currency = ["USD", "AUD", "EUR"]
        currency = tmp_currency.upper()
        if currency in fiat_currency:
            return "fiat_currency"
        else:
            return "crypto_currency"

    @staticmethod
    def round_decimals_up(number: float, decimals: int = 2):
        """
        Returns a value rounded up to a specific number of decimal places.
        """
        if not isinstance(decimals, int):
            raise TypeError("decimal places must be an integer")
        elif decimals < 0:
            raise ValueError("decimal places has to be 0 or more")
        elif decimals == 0:
            return math.ceil(number)

        factor = 10**decimals
        return math.ceil(number * factor) / factor

    @staticmethod
    def convert_epoch_time_to_datetime_fmt(from_fmt: str, epoch_time: int, to_fmt: str):
        format_epoch_time = str(datetime.fromtimestamp(epoch_time))
        return Tools.covert_datetime_fmt(
            from_fmt,
            format_epoch_time,
            to_fmt,
        )


class ImapEmail:
    """
    Connect and fetch the emails
    """

    def __init__(self, user_name: str, password: str, imap_url: str):
        self.user_name = user_name
        self.password = password
        self.imap_url = imap_url
        self.con: imaplib.IMAP4_SSL = None

    def login(self):
        self.con = imaplib.IMAP4_SSL(self.imap_url)
        self.con.login(self.user_name, self.password)
        return self

    def select_box(self, inbox_name: str, readonly=True):
        self.con.select(mailbox=inbox_name, readonly=readonly)
        return self

    def search_mail_by_sender(self, from_email: str):
        return self.con.search(None, f"FROM {from_email}")

    def fetch_by_mail_id(self, mail_id: str):
        return self.con.fetch(mail_id, "(RFC822)")

    def close_and_logout(self):
        self.con.close()
        self.con.logout()

    def get_latest_email(self, inbox_name: str = "INBOX", sender: str = "hello@crypto.com"):
        text_body = None
        date_time = None
        subject = None
        from_email = None
        to_email = None

        resp, items = self.login().select_box(inbox_name=inbox_name).search_mail_by_sender(from_email=sender)
        items = items[0].decode("utf-8").split(" ")
        item = items[-1]
        res, msg = self.fetch_by_mail_id(item)

        for response in msg:
            if isinstance(response, tuple):
                msg = email.message_from_bytes(response[1])
                to, encoding = decode_header(msg.get("To"))[0]
                to_email = str(to)
                date_time, encoding = decode_header(msg.get("Date"))[0]
                date_time = str(date_time)
                subject, encoding = decode_header(msg.get("Subject"))[0]
                subject = str(subject)
                From, encoding = decode_header(msg.get("From"))[0]
                from_email = str(From)

                for part in msg.walk():
                    body: list = part.get_payload()
                    text_body = body[0]
                    text_body = text_body.as_string()
                    break

        new_text_body_list = text_body.split("\n\n")
        for i in range(len(new_text_body_list)):
            line_str = new_text_body_list[i]
            if "http:" in line_str:
                new_text_body_list[i] = ""
                continue
            if "=\n" in line_str:
                new_line_str = line_str.replace("=\n", "")
                new_text_body_list[i] = new_line_str
                continue

        text_body = ""
        for line_str in new_text_body_list:
            if line_str != "":
                text_body += f"{line_str}\n"
        return to_email, from_email, date_time, subject, text_body
