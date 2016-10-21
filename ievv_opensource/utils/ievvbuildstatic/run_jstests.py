import json

from ievv_opensource.utils.ievvbuildstatic import pluginbase
from ievv_opensource.utils.shellcommandmixin import ShellCommandError
from ievv_opensource.utils.shellcommandmixin import ShellCommandMixin


class Plugin(pluginbase.Plugin, ShellCommandMixin):
    """
    Run javascript tests by running ``npm test`` if the
    ``package.json`` has a ``"test"`` entry in ``"scripts"``.

    Examples:

        Lets say you have the following in your package.json::

            {
              "scripts": {
                "test": "jest"
              }
            }

        You can then make ``jest`` run at startup (not on watch change)
        with::

            IEVVTASKS_BUILDSTATIC_APPS = ievvbuildstatic.config.Apps(
                ievvbuildstatic.config.App(
                    appname='demoapp',
                    version='1.0.0',
                    plugins=[
                        ievvbuildstatic.run_jstests.Plugin(),
                    ]
                )
            )
    """
    name = 'run_jstests'

    def __init__(self, **kwargs):
        """

        Args:
            **kwargs: Kwargs for :class:`ievv_opensource.utils.ievvbuildstatic.pluginbase.Plugin`.
        """
        super(Plugin, self).__init__(**kwargs)

    def has_tests(self):
        return 'test' in self.app.get_installer('npm').get_packagejson_dict().get('scripts', {})

    def run(self):
        if self.has_tests():
            self.get_logger().command_start('Running tests for {appname}'.format(
                appname=self.app.appname))
            try:
                self.run_shell_command('npm',
                                       args=['test'],
                                       _cwd=self.app.get_source_path())
            except ShellCommandError:
                self.get_logger().command_error('npm test FAILED!')
                raise SystemExit()
            else:
                self.get_logger().command_success('npm test succeeded :)')
