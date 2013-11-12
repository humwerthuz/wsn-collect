class CacheKeyStorage(object):
    def __init__(self):
        self.__storage = {}

    def insert(self, key, value):
        self.__storage[key] = value

    def get(self, key):
        if key in self.__storage:
            return self.__storage[key]
        else:
            return None

    def get_all(self):
        return self.__storage

cache_key_storage = CacheKeyStorage()