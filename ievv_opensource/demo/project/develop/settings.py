from ievv_opensource.demo.project.default.settings import *  # noqa
from ievv_opensource.utils import ievvbuildstatic

THIS_DIR = os.path.dirname(__file__)

IEVVTASKS_DUMPDATA_DIRECTORY = os.path.join(THIS_DIR, 'dumps')


IEVVTASKS_BUILDSTATIC_APPS = ievvbuildstatic.config.Apps(
    ievvbuildstatic.config.App(
        appname='demoapp',
        version='1.0.0',
        plugins=[
            ievvbuildstatic.lessbuild.Plugin(sourcefile='theme.less'),
            ievvbuildstatic.lessbuild.Plugin(
                sourcefolder='styles/themes/default',
                sourcefile='theme.less',
                other_sourcefolders=[
                    'styles/cradmin_theme_base',
                    'styles/cradmin_theme_default',
                ],
            ),
            ievvbuildstatic.mediacopy.Plugin(),
            # CoffeeBuild(sourcefolder='scripts'),
        ]
    ),
    ievvbuildstatic.config.App(
        appname='themeapp',
        version='2.0.1',
        plugins=[
            ievvbuildstatic.lessbuild.Plugin(
                sourcefolder='styles/theme',
                sourcefile='theme.less',
                other_sourcefolders=[
                    'styles/base',
                ],
            ),
            ievvbuildstatic.mediacopy.Plugin(),
        ]
    ),
)
