import os

from ievv_opensource.utils.ievvbuildstatic import pluginbase
from ievv_opensource.utils.ievvbuildstatic.filepath import AbstractDjangoAppPath
from ievv_opensource.utils.shellcommandmixin import ShellCommandError
from ievv_opensource.utils.shellcommandmixin import ShellCommandMixin


class Plugin(pluginbase.Plugin, ShellCommandMixin):
    """
    Webpack builder plugin.

    Examples:

        Simple example::

            IEVVTASKS_BUILDSTATIC_APPS = ievvbuildstatic.config.Apps(
                ievvbuildstatic.config.App(
                    appname='demoapp',
                    version='1.0.0',
                    plugins=[
                        ievvbuildstatic.webpack.Plugin(),
                    ]
                )
            )
    """
    name = 'webpack'
    default_group = 'js'

    def make_npm_run_environment(self):
        return None
    #     environment = os.environ.copy()
    #     environment.update({
    #         'NODE_PATH': ':'.join(self._get_import_paths_as_strlist())
    #     })
    #     return environment

    def run(self):
        self.get_logger().command_start('Running "npm run jsbuild"')
        destination_folder = self.app.get_destination_path(self.destinationfolder)
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)
        try:
            self.run_shell_command('npm',
                                   args=['run', 'jsbuild'],
                                   _cwd=self.app.get_source_path(),
                                   _env=self.make_npm_run_environment())
        except ShellCommandError:
            self.get_logger().command_error('browserify build FAILED!')
        else:
            self.get_logger().command_success('browserify build succeeded :)')

    def __str__(self):
        return '{}({})'.format(super(Plugin, self).__str__(), self.sourcefolder)
