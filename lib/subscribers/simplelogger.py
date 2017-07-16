from bitsows.abstracts.pubsub import AbsSubscriber
from multiprocessing import Process, SimpleQueue


def worker(q):
    import logging
    import logging.config
    import lib.configs.logging
    logging.config.dictConfig(lib.configs.logging.d)
    logger = logging.getLogger('stream')
    while True:
        if not q.empty():
            o = q.get()
            logger.info(o)
            for _o in o.payload:
                logger.info(_o)


class SimpleLoggerSubscriber(AbsSubscriber):

    def __init__(self, bitsoclient):
        self._bitsoclient = bitsoclient
        self._bitsoclient.attach(self)
        self.q = SimpleQueue()
        Process(target=worker, args=(self.q,)).start()

    def update(self, o):
        self.q.put(o)

    def __exit__(self, exc_type, exc_value, traceback):
        self._bitsoclient.detach(self)

