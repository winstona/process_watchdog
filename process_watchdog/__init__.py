from multiprocessing import Process, Queue
import time
import traceback
import os
import signal

class ProcessWatchdog():
    def __init__(self):
        self.deadline_threshold = 300
        self.interval = 60

    def loop(self, q):
        try:
            last_message = None

            while True:
                print("loop iter")
                while not q.empty():
                    last_message = q.get(block=False)

                print(f"got last message: {last_message}")

                if time.time() - last_message > self.deadline_threshold or last_message == None:
                    print("deadline passed, killing")
                    os.kill(os.getppid(), signal.SIGKILL)
                time.sleep(self.interval)
        except Exception as ex:
            print(f"got exception in process watchdog, killing parent:")
            traceback.print_exc()
            os.kill(os.getppid(), signal.SIGKILL)

    def __enter__(self):
        print("enter begin")
        self.q = Queue()
        p = Process(target=self.loop, args=(self.q,))
        p.start()
        self.ping()
        #p.join()
        return self


    def __exit__(self):
        print("exit begin")

    def ping(self):
        print("got ping")
        self.q.put(time.time())