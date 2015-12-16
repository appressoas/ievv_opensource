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


IEVVTASKS_DEVELOPRUN_THREADLIST = ievvdevrun.config.RunnableThreadList(
    ievvdevrun.runnables.runserver.RunnableThread(),
)
