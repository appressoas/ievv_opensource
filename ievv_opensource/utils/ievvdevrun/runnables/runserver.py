import time

from ievv_opensource.utils import shellcommandmixin
from ievv_opensource.utils.ievvdevrun.runnables import base


class RunnableThread(base.AbstractRunnableThread, shellcommandmixin.ShellCommandMixin):
    def start(self):
        self.get_logger().command_start('Starting Django development server')
        return super(RunnableThread, self).start()

    def __restartloop(self):
        while True:
            # Check if alive every 3 second, but check if we have been stopped
            # every 200ms.
            for x in range(12):
                time.sleep(0.2)
                if not self.is_running:
                    return
            if self.is_running:
                if not self.command.process.is_alive():
                    self.get_logger().warning('Restarting Django server because of crash.')
                    self.runserver()
            else:
                return

    def runserver(self):
        self.command = self.run_shell_command('python', args=['manage.py', 'runserver'],
                                              kwargs={'_bg': True})

    def run(self):
        self.is_running = True
        self.runserver()
        self.__restartloop()

    def stop(self):
        self.is_running = False
        process_ids = self.terminate_process(self.command.pid)
        self.get_logger().command_success(
                'Django development server stopped :) '
                '[killed pids: {}]'.format(', '.join(map(str, process_ids))))
