from watchdog.observers import Observer

from ievv_opensource.utils.ievvbuild.buildloggable import BuildLoggable
from ievv_opensource.utils.ievvbuild.watcher import EventHandler


class Plugin(BuildLoggable):
    name = None

    def __init__(self):
        self.app = None
        self.is_executing = False

    def install(self):
        """
        Install any packages required for this plugin.

        Should use :meth:`ievv_opensource.utils.ievvbuild.config.App.get_installer`.

        Examples:

            Install an npm package::

                def install(self):
                    self.app.get_installer(NpmInstaller).install(
                        'somepackage')
                    self.app.get_installer(NpmInstaller).install(
                        'otherpackage', version='~1.0.0')
        """

    def run(self):
        pass

    def watch(self):
        watchfolder = self.get_watch_folder()
        if watchfolder is None:
            return
        watchregexes = self.get_watch_regexes()
        event_handler = EventHandler(
            plugin=self,
            regexes=watchregexes
        )
        observer = Observer()
        observer.schedule(event_handler, watchfolder, recursive=True)
        self.get_logger().info('Starting watcher for folder %s with regexes %r',
                               watchfolder, watchregexes)
        observer.start()
        return observer

    def get_watch_regexes(self):
        return [r'^.*$']

    def get_watch_folder(self):
        return None

    def get_logger_name(self):
        return '{}.{}'.format(self.app.get_logger_name(), self.name)
