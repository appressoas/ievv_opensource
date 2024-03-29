from ievv_opensource.demo.project.default.settings import *  # noqa
from ievv_opensource.utils import ievvbuildstatic
from ievv_opensource.utils import ievvdevrun

THIS_DIR = os.path.dirname(__file__)

ROOT_URLCONF = 'ievv_opensource.demo.project.develop.urls'
IEVVTASKS_DUMPDATA_DIRECTORY = os.path.join(THIS_DIR, 'dumps')


IEVVTASKS_BUILDSTATIC_APPS = ievvbuildstatic.config.Apps(
    ievvbuildstatic.config.App(
        appname='demoapp',
        version='1.0.0',
        # keep_temporary_files=False,
        plugins=[
            ievvbuildstatic.lessbuild.Plugin(sourcefile='theme.less'),
            ievvbuildstatic.mediacopy.Plugin(),
            ievvbuildstatic.coffeebuild.Plugin(
                destinationfile='coffeetest.js',
                lintconfig={
                    "max_line_length": {
                        'value': 102,
                        'level': "warn",
                        'limitComments': True,
                    }
                }
            ),
            ievvbuildstatic.browserify_jsbuild.Plugin(
                sourcefolder=os.path.join('scripts', 'javascript', 'browserify_jsbuild_demo'),
                sourcefile='browserify_jsbuild_demo.js',
                destinationfile='browserify_jsbuild_demo.js',
            ),
            ievvbuildstatic.browserify_babelbuild.Plugin(
                sourcefolder=os.path.join('scripts', 'javascript', 'browserify_babelbuild_demo'),
                sourcefile='browserify_babelbuild_demo.js',
                destinationfile='browserify_babelbuild_demo.js',
            ),
            ievvbuildstatic.browserify_reactjsbuild.Plugin(
                sourcefolder=os.path.join('scripts', 'javascript', 'browserify_reactjsbuild_demo'),
                sourcefile='browserify_reactjsbuild_demo.js',
                destinationfile='browserify_reactjsbuild_demo.js',
            ),
        ]
    ),
    ievvbuildstatic.config.App(
        appname='demoapp2',
        version='2.0.1',
        # installers_config={
        #     'npm': {
        #         'installer_class': ievvbuildstatic.installers.npm.NpmInstaller
        #     }
        # },
        plugins=[
            ievvbuildstatic.sassbuild.Plugin(
                sourcefolder='styles/theme',
                sourcefile='theme.scss',
                other_sourcefolders=[
                    'styles/base',
                ]
            ),
            ievvbuildstatic.sassbuild.Plugin(
                sourcefolder='styles/theme2',
                sourcefile='theme2.scss',
                other_sourcefolders=[
                    'styles/base',
                ]
            ),
            ievvbuildstatic.mediacopy.Plugin(),
        ]
    ),
    help_header='You can configure the settings for ievv buildstatic in '
                'the IEVVTASKS_BUILDSTATIC_APPS setting in: '
                '{configfile}'.format(configfile=__file__),
)


IEVVTASKS_DEVRUN_RUNNABLES = {
    'default': ievvdevrun.config.RunnableThreadList(
        ievvdevrun.runnables.django_runserver.RunnableThread(port=9005),
        ievvdevrun.runnables.rq_worker.RunnableThread(),
    ),
}

IEVV_BATCHFRAMEWORK_ALWAYS_SYNCRONOUS = False


EMAIL_BACKEND = 'ievv_opensource.ievv_developemail.email_backend.DevelopEmailBackend'
