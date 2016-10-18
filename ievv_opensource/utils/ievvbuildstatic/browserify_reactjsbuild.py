from ievv_opensource.utils.ievvbuildstatic.installers.npm import NpmInstaller
from . import browserify_babelbuild


class Plugin(browserify_babelbuild.Plugin):
    """
    Browserify javascript babel build plugin.

    Examples:

        Simple example::

            IEVVTASKS_BUILDSTATIC_APPS = ievvbuildstatic.config.Apps(
                ievvbuildstatic.config.App(
                    appname='demoapp',
                    version='1.0.0',
                    plugins=[
                        ievvbuildstatic.browserify_reactjsbuild.Plugin(
                            sourcefile='app.js',
                            destinationfile='app.js',
                        ),
                    ]
                )
            )

        Custom source folder example::

            IEVVTASKS_BUILDSTATIC_APPS = ievvbuildstatic.config.Apps(
                ievvbuildstatic.config.App(
                    appname='demoapp',
                    version='1.0.0',
                    plugins=[
                        ievvbuildstatic.browserify_reactjsbuild.Plugin(
                            sourcefolder=os.path.join('scripts', 'javascript', 'api'),
                            sourcefile='api.js',
                            destinationfile='api.js',
                        ),
                    ]
                )
            )

    """
    name = 'browserify_reactjsbuild'

    def install(self):
        """
        Installs the ``babel-preset-react`` NPM package
        in addition to the packages installed by
        :meth:`ievv_opensource.utils.ievvbuildstatic.browserify_babelbuild.Plugin.install`.

        The packages are installed with no version specified, so you
        probably want to freeze the versions using the
        :class:`ievv_opensource.utils.ievvbuildstatic.npminstall.Plugin` plugin.
        """
        super(Plugin, self).install()
        self.app.get_installer(NpmInstaller).queue_install(
            'babel-preset-react')

    def get_babelify_presets(self):
        return super(Plugin, self).get_babelify_presets() + [
            'react',
        ]
