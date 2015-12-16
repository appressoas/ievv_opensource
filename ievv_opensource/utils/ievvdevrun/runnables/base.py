import threading

from ievv_opensource.utils import logmixin


class AbstractRunnableThread(threading.Thread, logmixin.LogMixin):
    """
    Abstract class for a thread that runs something for the ``ievvrun`` framework.
    """

    def get_logger_name(self):
        return self.__class__.__module__

    def stop(self):
        """
        Must stop the code running in the thread (the code in the run method).
        """
        pass
