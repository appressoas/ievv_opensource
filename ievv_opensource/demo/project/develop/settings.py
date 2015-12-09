from ievv_opensource.demo.project.default.settings import *  # noqa
from ievv_opensource.utils import ievvbuild

THIS_DIR = os.path.dirname(__file__)

IEVVTASKS_DUMPDATA_DIRECTORY = os.path.join(THIS_DIR, 'dumps')


IEVVTASKS_BUILD_APPS = ievvbuild.config.Apps(
    ievvbuild.config.App(
        appname='demoapp',
        version='1.0.0',
        plugins=[
            ievvbuild.lessbuild.Plugin(sourcefile='theme.less'),
            ievvbuild.mediacopy.Plugin(),
            # ievvbuild.clessbuild.Plugin(),
            # ievvbuild.lessbuild.Plugin(
            #     sourcefolder='styles/themes/default',
            #     sourcefile='theme.less',
            #     other_sourcefolders=[
            #         'styles/cradmin_theme_base',
            #         'styles/cradmin_theme_default',
            #     ],
            # ),
            # ievvbuild.lessbuild.Plugin(sourcefolder='less/themes/dark'),
            # ievvbuild.lessbuild.Plugin(sourcefolder='less/themes/red'),
            # CoffeeBuild(sourcefolder='scripts'),
            # CopyMedia(validate_structure=True,
            #           sourcefolder='media'),
        ]
    ),
    # ievvbuild.config.App(
    #     'themeapp',
    #     LessBuild()
    # ),
)
