import time


class RunnableThreadList(object):
    def __init__(self, *runnablethreads):
        self._runnablethreads = []
        for runnablethread in runnablethreads:
            self.append(runnablethread)

    def append(self, runnablethread):
        self._runnablethreads.append(runnablethread)

    def start(self):
        for runnablethread in self._runnablethreads:
            runnablethread.start()

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            for runnablethread in self._runnablethreads:
                runnablethread.stop()

        for runnablethread in self._runnablethreads:
            runnablethread.join()
