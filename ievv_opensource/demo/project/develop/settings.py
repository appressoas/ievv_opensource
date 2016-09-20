from ievv_opensource.demo.project.default.settings import *  # noqa
from ievv_opensource.utils import ievvbuildstatic
from ievv_opensource.utils import ievvdevrun

THIS_DIR = os.path.dirname(__file__)

ROOT_URLCONF = 'ievv_opensource.demo.project.develop.urls'
IEVVTASKS_DUMPDATA_DIRECTORY = os.path.join(THIS_DIR, 'dumps')


IEVVTASKS_BUILDSTATIC_APPS = ievvbuildstatic.config.Apps(
    # ievvbuildstatic.config.App(
    #     appname='demoapp',
    #     version='1.0.0',
    #     # keep_temporary_files=False,
    #     plugins=[
    #         ievvbuildstatic.lessbuild.Plugin(sourcefile='theme.less'),
    #         ievvbuildstatic.mediacopy.Plugin(),
    #         ievvbuildstatic.coffeebuild.Plugin(
    #             destinationfile='coffeetest.js',
    #             lintconfig={
    #                 "max_line_length": {
    #                     'value': 102,
    #                     'level': "warn",
    #                     'limitComments': True,
    #                 }
    #             }
    #         ),
    #         ievvbuildstatic.npminstall.Plugin(
    #             packages={
    #                 'uniq': None,
    #                 'momentjs': None
    #             }
    #         ),
    #         ievvbuildstatic.browserify_jsbuild.Plugin(
    #             sourcefile='jstest.js',
    #             destinationfile='jstest.js',
    #         )
    #     ]
    # ),
    # ievvbuildstatic.config.App(
    #     appname='demoapp2',
    #     version='2.0.1',
    #     plugins=[
    #         ievvbuildstatic.sassbuild.Plugin(
    #             sourcefolder='styles/theme',
    #             sourcefile='theme.scss',
    #             other_sourcefolders=[
    #                 'styles/base',
    #             ]
    #         ),
    #         ievvbuildstatic.sassbuild.Plugin(
    #             sourcefolder='styles/theme2',
    #             sourcefile='theme2.scss',
    #             other_sourcefolders=[
    #                 'styles/base',
    #             ]
    #         ),
    #         ievvbuildstatic.mediacopy.Plugin(),
    #     ]
    # ),
    ievvbuildstatic.config.App(
        appname='reactjs_demo',
        version='0.1.0',
        plugins=[
            ievvbuildstatic.npminstall.Plugin(
                packages={
                    'react': None,
                    'react-dom': None,
                }
            ),
            ievvbuildstatic.nodemodulescopy.Plugin(
                sourcefiles=[
                    'react/dist/react.js',
                    'react-dom/dist/react-dom.js',
                ]
            ),
            ievvbuildstatic.typescriptbuild.Plugin(
                main_sourcefile='stuff.tsx',
                typings_for_dependencies=[
                    # 'dt~react',
                    # 'dt~react-dom',
                    # 'dt~react-global',
                    'npm~react@15.0.1',
                    'npm~react-dom@15.0.1',
                ],
                tsc_compiler_options={
                    'jsx': 'react'
                },
            )
        ]
    ),
    help_header='You can configure the settings for ievv buildstatic in '
                'the IEVVTASKS_BUILDSTATIC_APPS setting in: '
                '{configfile}'.format(configfile=__file__),
)


IEVVTASKS_DEVRUN_RUNNABLES = {
    'default': ievvdevrun.config.RunnableThreadList(
        ievvdevrun.runnables.dbdev_runserver.RunnableThread(),
        ievvdevrun.runnables.django_runserver.RunnableThread(port=9001),
        ievvdevrun.runnables.redis_server.RunnableThread(port='6381'),
        ievvdevrun.runnables.celery_worker.RunnableThread(app='ievv_opensource.demo'),
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
        'port': '9252',
        'transport_class': 'ievv_opensource.ievv_elasticsearch2.transport.debug.DebugTransport'
    }
}

# IEVV_ELASTICSEARCH2_DEBUGTRANSPORT_PRETTYPRINT_ALL_REQUESTS = True
IEVV_BATCHFRAMEWORK_ALWAYS_SYNCRONOUS = False
