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
            ievvbuildstatic.sassbuild.Plugin(
                sourcefolder='styles/theme',
                sourcefile='theme.scss',
                other_sourcefolders=[
                    'styles/base',
                ],
                sass_include_paths=[
                    'bower_components',
                ]
            ),
            ievvbuildstatic.sassbuild.Plugin(
                sourcefolder='styles/theme2',
                sourcefile='theme2.scss',
                other_sourcefolders=[
                    'styles/base',
                ],
                sass_include_paths=[
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
        ievvdevrun.runnables.django_runserver.RunnableThread(port=9001),
        ievvdevrun.runnables.elasticsearch.RunnableThread(configpath='not_for_deploy/elasticsearch.unittest/'),
        ievvdevrun.runnables.elasticsearch.RunnableThread(configpath='not_for_deploy/elasticsearch.develop/'),
    ),
    'design': ievvdevrun.config.RunnableThreadList(
        ievvdevrun.runnables.dbdev_runserver.RunnableThread(),
        ievvdevrun.runnables.django_runserver.RunnableThread(port=9001),
        ievvdevrun.runnables.ievv_buildstatic.RunnableThread(),
        ievvdevrun.runnables.elasticsearch.RunnableThread(configpath='not_for_deploy/elasticsearch.unittest/'),
        ievvdevrun.runnables.elasticsearch.RunnableThread(configpath='not_for_deploy/elasticsearch.develop/'),
    ),
}

IEVV_ELASTICSEARCH_MAJOR_VERSION = 2


IEVV_ELASTICSEARCH2_CONNECTION_ALIASES = {
    'default': {
        'host': '127.0.0.1',
        'port': '9252'
    }
}
