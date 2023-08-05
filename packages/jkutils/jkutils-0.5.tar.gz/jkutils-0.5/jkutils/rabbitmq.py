# -*- coding: utf-8 -*-

import logging
import traceback

import pika

LOGGER = logging.getLogger(__name__)


class MQPublisher:
    def __init__(self, amqp_url):
        self._url = amqp_url

    def publish(self, exchange: str, exchange_type: str, durable: bool, routing_key, msg):
        try:

            parameters = pika.URLParameters(self._url)

            connection = pika.BlockingConnection(parameters)
            channel = connection.channel()
            channel.exchange_declare(exchange=exchange, exchange_type=exchange_type, durable=durable)
            channel.basic_publish(exchange=exchange, routing_key=routing_key, body=msg)
        except Exception as e:
            LOGGER.warning(f"send_msg:{str(e)}, Exception:{traceback.format_exc()}")
            raise
        finally:
            connection.close()


if __name__ == "__main__":
    p = MQPublisher("amqp://xxwdev:xxwdev2018@172.16.1.49:20003/")
    p.send_msg(exchange="teddy", exchange_type="topic", durable=True, routing_key="teddy", msg="xxx")
