import threading
import time
import settings
import asyncore
import socket
from storage import cache_key_storage


class AsyncUdpServer(asyncore.dispatcher):
    def __init__(self, write_handler):
        asyncore.dispatcher.__init__(self)
        self.write_handler = write_handler
        self.create_socket(socket.AF_INET6, socket.SOCK_DGRAM)
        self.bind((settings.host_conf['ip'], settings.host_conf['port']))

    def handle_connect(self):
        print "Server started..."

    def handle_read(self):
        print "Log: received data, updating local storage"
        self.write_handler(data=self.recv(1024))

    def handle_write(self):
        pass


class WsnCollectDriver(object):
    def __init__(self):
        self.__storage = cache_key_storage
        self.__async_handler = AsyncUdpServer(self.write_handler)
        self.__loop_thread = threading.Thread(target=self.loop_handler)
        self.__loop_thread.start()

    @staticmethod
    def loop_handler():
        print "Asyncore loop thread running!"
        while True:
            asyncore.loop(count=5)
            time.sleep(0.05)

    def write_handler(self, data):
        self.__storage.insert('key', data)

    def get_storage(self):
        return self.__storage