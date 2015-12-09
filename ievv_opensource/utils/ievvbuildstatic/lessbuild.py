import os
import sh
from ievv_opensource.utils.ievvbuildstatic import pluginbase
from ievv_opensource.utils.ievvbuildstatic.installers.npm import NpmInstaller


class Plugin(pluginbase.Plugin):
    name = 'lessbuild'

    def __init__(self, sourcefile, sourcefolder='styles',
                 other_sourcefolders=None):
        """
        Parameters:
            sourcefile: Main source file (the one including all other less files)
                relative to ``sourcefolder``.
            sourcefolder: The folder where ``sourcefile`` is located relative to
                the source folder of the :class:`~ievv_opensource.utils.ievvbuild.config.App`.

        """
        self.sourcefolder = sourcefolder
        self.other_sourcefolders = other_sourcefolders
        self.sourcefile = os.path.join(sourcefolder, sourcefile)

    def get_sourcefile_path(self):
        return self.app.get_source_path(self.sourcefile)

    def get_destinationfile_path(self):
        return self.app.get_destination_path(
            self.sourcefile, new_extension='.css')

    def get_less_version(self):
        return None

    def install(self):
        self.app.get_installer(NpmInstaller).queue_install(
            'less', version=self.get_less_version())

    def run(self):
        lessc = sh.Command(self.app.get_installer(NpmInstaller).find_executable(
            'lessc'))
        output = lessc(self.get_sourcefile_path(), self.get_destinationfile_path())
        self.get_logger().info(output)

    def get_watch_folders(self):
        """
        We only watch the folder where the less sources are located,
        so this returns the absolute path of the ``sourcefolder``.
        """
        folders = [self.app.get_source_path(self.sourcefolder)]
        if self.other_sourcefolders:
            folders.extend(self.other_sourcefolders)
        return folders

    def get_watch_regexes(self):
        return ['^.+[.]less$']
