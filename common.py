""" Common code used by watcher and recorder """
import collections
import logging
import re
import time


from kafka import KafkaProducer
from kafka import KafkaConsumer
import kafka.errors

from psycopg2.extras import RealDictCursor
import psycopg2

import requests
from requests.exceptions import Timeout


class MessageStream(object):
    """ Kafka wrapper """

    def __init__(self, ca_cert_path, access_cert_path, access_key_path, uri, topic):
        self.ca_cert_path = ca_cert_path
        self.access_cert_path = access_cert_path
        self.access_key_path = access_key_path
        self.uri = uri
        self.topic = topic
        self.logger = logging.getLogger(__name__)

        try:
            self.producer = KafkaProducer(
                bootstrap_servers=self.uri,
                security_protocol="SSL",
                ssl_cafile=self.ca_cert_path,
                ssl_certfile=self.access_cert_path,
                ssl_keyfile=self.access_key_path,
            )

            self.consumer = KafkaConsumer(
                self.topic,
                bootstrap_servers=self.uri,
                security_protocol="SSL",
                ssl_cafile=self.ca_cert_path,
                ssl_certfile=self.access_cert_path,
                ssl_keyfile=self.access_key_path,
            )
        except kafka.errors.NoBrokersAvailable as e:
            self.logger.error(e)
            raise e

    def send_message(self, message):
        try:
            self.producer.send(self.topic, message.encode("utf-8"))
            self.producer.flush()
        except Exception as e:
            self.logger.error(e)
            raise e

    def receive_message(self):
        try:
            for msg in self.consumer:
                yield msg
        except Exception as e:
            self.logger.error(e)
            raise e


class Database(object):
    """ Postgres database wrapper """

    def __init__(self, postgres_uri):
        self.uri = postgres_uri
        self.logger = logging.getLogger(__name__)

    def __enter__(self):
        try:
            self.db_conn = psycopg2.connect(self.uri)
            self.cursor = self.db_conn.cursor(cursor_factory=RealDictCursor)
            return self
        except psycopg2.Error as e:
            self.logger.error(e)
            raise e

    def __exit__(self, *args):
        try:
            self.db_conn.commit()
            self.cursor.close()
            self.db_conn.close()
        except psycopg2.Error as e:
            self.logger.error(e)
            raise e

    def insert_event(self, status):
        try:
            url = status['url']
            code = status['code']
            response_time = status['response_time']
            content_ok = status['content_ok']
            timestamp = status['timestamp']
        except KeyError as e:
            self.logger.error(e)
            raise e

        try:
            self.cursor.execute(
                "INSERT INTO site_check_events (url, code, response_time, content_ok, timestamp) values (%s, %s, %s, %s, %s)",
                (url, code, response_time, content_ok, timestamp))
        except psycopg2.Error as e:
            self.logger.error(e)
            raise e


class WebsiteChecker(object):
    """ Contain logic for checking website """

    Status = collections.namedtuple('Status', 'url code response_time content_ok timestamp')

    def __init__(self, website_url, timeout=1, regex=None):
        self.url = website_url
        self.timeout = timeout
        self.regex = regex
        self.logger = logging.getLogger(__name__)

    def get_status(self):
        timestamp = time.time()
        try:
            response = requests.get(self.url, timeout=self.timeout)
        except Timeout as e:
            self.logger.warning(e)
            return self.Status(url=self.url, code=0, response_time=0, content_ok=False, timestamp=timestamp)

        content_ok = self.check_content(response.text)
        response_time = time.time() - timestamp
        return self.Status(url=self.url, code=response.status_code, response_time=response_time, content_ok=content_ok,
                           timestamp=timestamp)

    def check_content(self, text):
        """ Check request result text against regex """
        if self.regex is None:
            return True
        else:
            if re.search(self.regex, text):
                return True
            return False
