from ievv_opensource.demo.project.default.settings import *  # noqa
from ievv_opensource.utils import ievvbuildstatic
from ievv_opensource.utils import ievvdevrun

THIS_DIR = os.path.dirname(__file__)

IEVVTASKS_DUMPDATA_DIRECTORY = os.path.join(THIS_DIR, 'dumps')


IEVVTASKS_BUILDSTATIC_APPS = ievvbuildstatic.config.Apps(
    ievvbuildstatic.config.App(
        appname='demoapp',
        version='1.0.0',
        plugins=[
            ievvbuildstatic.lessbuild.Plugin(sourcefile='theme.less'),
            ievvbuildstatic.mediacopy.Plugin(),
            # CoffeeBuild(sourcefolder='scripts'),
        ]
    ),
    ievvbuildstatic.config.App(
        appname='demoapp2',
        version='2.0.1',
        plugins=[
            ievvbuildstatic.bowerinstall.Plugin(
                packages={
                    'bootstrap': '~3.1.1'
                }
            ),
            ievvbuildstatic.lessbuild.Plugin(
                sourcefolder='styles/theme',
                sourcefile='theme.less',
                other_sourcefolders=[
                    'styles/base',
                ],
                less_include_paths=[
                    'bower_components',
                ]
            ),
            ievvbuildstatic.mediacopy.Plugin(),
        ]
    ),
)


IEVVTASKS_DEVRUN_RUNNABLES = {
    'default': ievvdevrun.config.RunnableThreadList(
        ievvdevrun.runnables.dbdev_runserver.RunnableThread(),
        ievvdevrun.runnables.django_runserver.RunnableThread(),
        # ievvdevrun.runnables.base.ShellCommandRunnableThread(
        #     autorestart_on_crash=False,
        #     name='Manually configured Django development server',
        #     command_config={
        #         'executable': sys.executable,
        #         'args': ['manage.py', 'runserver']
        #     }
        # ),
    ),
    'design': ievvdevrun.config.RunnableThreadList(
        ievvdevrun.runnables.dbdev_runserver.RunnableThread(),
        ievvdevrun.runnables.django_runserver.RunnableThread(),
        ievvdevrun.runnables.ievv_buildstatic.RunnableThread(),
    )
}
