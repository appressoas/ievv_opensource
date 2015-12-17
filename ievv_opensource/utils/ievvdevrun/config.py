import time

import sys
import signal


class RunnableThreadList(object):
    def __init__(self, *runnablethreads):
        self._runnablethreads = []
        for runnablethread in runnablethreads:
            self.append(runnablethread)

    def append(self, runnablethread):
        self._runnablethreads.append(runnablethread)

    def start(self):
        def start_all():
            for runnablethread in self._runnablethreads:
                runnablethread.start()

        def stop_all():
            for runnablethread in self._runnablethreads:
                runnablethread.stop()

        def join_all():
            for runnablethread in self._runnablethreads:
                runnablethread.join()

        def on_terminate(*args):
            print('', file=sys.stderr)
            print('*' * 70, file=sys.stderr)
            print('ievvdevrun terminated', file=sys.stderr)
            print('*' * 70, file=sys.stderr)
            stop_all()
            join_all()
            sys.exit(0)

        start_all()
        signal.signal(signal.SIGTERM, on_terminate)
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print('', file=sys.stderr)
            print('*' * 70, file=sys.stderr)
            print('ievvdevrun KeyboardInterrupt', file=sys.stderr)
            print('*' * 70, file=sys.stderr)
            stop_all()
        join_all()
