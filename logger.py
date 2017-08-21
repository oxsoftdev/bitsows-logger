import logging.config
import tornado
from bitsoapi import Client as Api
from bitsows import Client as Websocket

import lib.configs.logging
from lib.subscribers import SimpleLoggerSubscriber


logging.config.dictConfig(lib.configs.logging.d)


if __name__ == '__main__':
    books = Api().available_books().books
    with Websocket(books) as client:
        with SimpleLoggerSubscriber(client):
            client.connect()
            try:
                tornado.ioloop.IOLoop.instance().start()
            except KeyboardInterrupt:
                client.close()

