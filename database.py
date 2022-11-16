import json
import threading
import time


class Database:
    path = 'db.json'
    write_lock = threading.Lock()
    read_lock = threading.Semaphore(10)
    count = 0
    delay = 1

    @staticmethod
    def __read_db():
        with open(Database.path, 'r') as f:
            try:
                return json.load(f)

            except json.decoder.JSONDecodeError:
                return {}

    @staticmethod
    def __write_db(data):
        with open(Database.path, 'w') as f:
            json.dump(data, f)

    @staticmethod
    def get_value(thread_id, key):
        while Database.write_lock.locked():
            continue

        Database.read_lock.acquire()
        Database.count += 1
        time.sleep(5)

        print(f'\n{thread_id}: read from db in location: {key} -- {time.time()}', end='')

        data = Database.__read_db()
        Database.count -= 1
        Database.read_lock.release()

        return data[key]

    @staticmethod
    def remove_key(thread_id, key):
        while Database.count != 0:
            continue

        Database.write_lock.acquire()
        time.sleep(Database.delay)

        print(f'{thread_id}: removing from db in location: {key}')

        data = Database.__read_db()
        data.pop(key)
        Database.__write_db(data)

        Database.write_lock.release()

    @staticmethod
    def insert(thread_id, key, value):
        while Database.count != 0:
            continue

        Database.write_lock.acquire()
        time.sleep(Database.delay)
        print(f'\n{thread_id}: insert: {value} in location: "{key}" -- {time.time()}', end='')

        data = Database.__read_db()
        data[key] = value
        Database.__write_db(data)

        Database.write_lock.release()
