# -*- coding: utf-8 -*_
#import thread
import threading
import time
import Queue

exitFlag = 0

def process_data(thradName, q):
    while not exitFlag:
        queueLock.acquire()
        if not workQueue.empty():
            data = q.get()
            queueLock.release()
            print "%s processing %s" % (thradName, data)
        else:
            queueLock.release()
        time.sleep(1)

class myThread(threading.Thread):
    def __init__(self, threadID, name, q):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.q = q
    def run(self):
        print "Staring " + self.name
        process_data(self.name, self.q)
        print "Exiting " + self.name

threadList = ["Thread-1", "Thread-2", "Thread-3"]
nameList = ["One", "Two", "Three", "Four", "Five"]
queueLock = threading.Lock()
workQueue = Queue.Queue(10)
threads = []
threadID = 1

for tName in threadList:
    thread = myThread(threadID, tName, workQueue)
    thread.start()
    threads.append(thread)
    threadID += 1

queueLock.acquire()
for word in nameList:
    workQueue.put(word)
queueLock.release()

while not workQueue.empty():
    pass

exitFlag = 1

for t in threads:
    t.join()
print "Exiting Main Thread"


'''
def print_time(threadName, delay):
    count = 0
    while count < 5:
        time.sleep(delay)
        count += 1
        print "%s: %s" % (threadName, time.ctime(time.time()))

try:
    thread.start_new_thread(print_time, ("Thread-1", 2))
    thread.start_new_thread(print_time, ("Thread-2", 4))
except:
    print "Error：unable to start thread"

while 1:
    pass
'''

'''
exitFlag = 0
threads = []
threadLock = threading.Lock()

def print_time(threadName, delay, counter):
    while counter:
        if exitFlag:
            threading.Thread.exit()
        time.sleep(delay)
        print "%s: %s" % (threadName, time.ctime(time.time()))
        counter -= 1

class myThread(threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
    def run(self):
        print "Starting " + self.name
        threadLock.acquire()
        print_time(self.name, self.counter, 5)
        threadLock.release()
        print "Exiting " + self.name

thread1 = myThread(1, "Thread-1", 1)
thread2 = myThread(2, "Thread-2", 2)

thread1.start()
thread2.start()

threads.append(thread1)
threads.append(thread2)

for t in threads:
    t.join()
print "exiting Main Thread"
'''

