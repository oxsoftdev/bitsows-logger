from dppy.behavioral import pubsub
from multiprocessing import Process, SimpleQueue


def worker(q):
    import logging
    import logging.config
    from ..configs.logging import d
    logging.config.dictConfig(d)
    logger = logging.getLogger('stream')
    while True:
        if not q.empty():
            o = q.get()
            logger.info(o)
            for _o in o.payload:
                logger.info(_o)


class SimpleLoggerSubscriber(pubsub.AbsSubscriber):

    def __init__(self, bitsoclient):
        self._bitsoclient = bitsoclient
        self._bitsoclient.attach(self)
        self.q = SimpleQueue()
        Process(target=worker, args=(self.q,)).start()

    def update(self, o):
        self.q.put(o)

    def __exit__(self, exc_type, exc_value, traceback):
        self._bitsoclient.detach(self)

