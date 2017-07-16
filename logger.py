import logging.config
import tornado
from bitsows.client import BitsoClient

import lib.configs.logging
from lib.subscribers.simplelogger import SimpleLoggerSubscriber

logging.config.dictConfig(lib.configs.logging.d)

with BitsoClient() as client:
    with SimpleLoggerSubscriber(client):
        client.connect()
        try:
            tornado.ioloop.IOLoop.instance().start()
        except KeyboardInterrupt:
            client.close()

