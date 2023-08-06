import time
import logging


class NodeModule(object):
    active = False

    def __init__(self, mbus, queue, active, stop, cache):
        """Create the module, receives the message bus and queue"""
        self.id = self.__class__.__name__
        self.__mbus = mbus
        self.__queue = queue
        self.__active = active
        self.__stop = stop
        self.cache = cache

    def worker(self):
        while True:
            if self.__stop.is_set():
                break
            if self.__active.is_set():
                self.active = True
            else:
                self.active = False
            try:
                if not self.__queue.empty():
                    self.__processQueue(self.__queue.get())
                    self.__queue.task_done()
                self.tick()
            except Exception as e:
                logging.error("Exception: " + str(e))
                time.sleep(5)

    def __processQueue(self, data):

        callback = getattr(self, "callback_" + data["type"], None)

        if data["type"] == "shutdown":
            exit()

        elif data["type"] == "__icache":
            self.cache = data["data"]

        elif callable(callback):
            callback(data)

        else:
            self.processMessage(data)

    def store(self, key, value):
        data = {"type": "store", "key": key, "value": value}
        self.__mbus.put(data)

    def get(self, key):
        if key in self.cache:
            return self.cache[key]
        return None

    def push(self, data):
        if "type" not in data:
            data = {"type": "unspecified", "data": data, }
        self.__mbus.put(data)

    def pushToModule(self, name, data):
        data["target"] = name
        self.__send(data)

    def wait(self):
        if self.__queue.empty():
            time.sleep(0.1)

    def tick(self):
        self.wait()

    def processMessage(self, data):
        pass
