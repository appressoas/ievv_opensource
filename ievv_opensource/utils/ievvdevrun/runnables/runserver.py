from ievv_opensource.utils import shellcommandmixin
from ievv_opensource.utils.ievvdevrun.runnables import base


class RunnableThread(base.AbstractRunnableThread, shellcommandmixin.ShellCommandMixin):
    def start(self):
        self.get_logger().command_start('Starting Django development server')
        return super(RunnableThread, self).start()

    def run(self):
        self.is_running = True
        self.command = self.run_shell_command('python', args=['manage.py', 'runserver'],
                                              kwargs={'_bg': True})

    def stop(self):
        process_ids = self.terminate_process(self.command.pid)
        self.get_logger().command_success(
                'Django development server stopped :) '
                '[killed pids: {}]'.format(', '.join(map(str, process_ids))))
