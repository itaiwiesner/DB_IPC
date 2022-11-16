from database import Database
import threading

# --------------
# TESTS:
# --------------


def insert_range(thread_id, nums):
    for i in nums:
        Database.insert(thread_id, thread_id, i)


def read_range(thread_id, keys):
    pass


def test1():
    print('-------------------')
    print('test #1:')
    print('10 threads are writing a range of numbers simultaneously to the database')
    print('-------------------')
    threads = []
    for i in range(10):
        threads.append(threading.Thread(target=insert_range, args=(f'Thread {i}', range(10, 11))))
        threads[i].start()

    for t in threads:
        t.join()


def test2():
    print('-------------------')
    print('test #2:')
    print('20 threads read from the database, but only 10 threads can read from it simultaneously. '
          'Another thread tries to write to the database, '
          'and wait until no thread reads from the file anymore')
    print('-------------------')
    threads = []
    for i in range(20):
        threads.append(threading.Thread(target=Database.get_value, args=(f'Thread {i}', 'Thread 1')))
        threads[i].start()

    threads.append(threading.Thread(target=Database.insert, args=(f'Thread {20}', f'Thread {20}', 222)))
    threads[20].start()

    for t in threads:
        t.join()


def main():
    test1()
    test2()


if __name__ == '__main__':
    main()
