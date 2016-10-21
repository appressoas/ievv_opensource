from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'A build system (for sass, javascript, ...).'

    def add_arguments(self, parser):
        parser.add_argument('-w', '--watch', dest='watch',
                            required=False, action='store_true',
                            help='Starts a blocking process that watches for changes.')
        parser.add_argument('-a', '--appname', dest='appnames',
                            required=False, default=[], action='append',
                            help='Specify one or more apps to build. If not specified, all '
                                 'apps are built. Example: "-a ievv_jsbase -a demoapp2"')
        parser.add_argument('-s', '--skip', dest='skipgroups',
                            required=False, action='append',
                            help='Skip a plugin group. Can be repeated. Example: "-s test -s css".')
        parser.add_argument('--skip-js', dest='skipgroups',
                            required=False, action='append_const', const='js',
                            help='Skip building javascript. The same as "--skip js".')
        parser.add_argument('--skip-css', dest='skipgroups',
                            required=False, action='append_const', const='css',
                            help='Skip building css. The same as "--skip css".')
        parser.add_argument('--skip-jstests', dest='skipgroups',
                            required=False, action='append_const', const='jstest',
                            help='Skip running javascript tests. The same as "--skip jstest".')
        parser.add_argument('--skip-slow-tests', dest='skipgroups',
                            required=False, action='append_const', const='slow-jstest',
                            help='Skip running slow javascript tests. The same as "--skip slow-jstest". '
                                 'Slow javascript tests are also skipped if you use "--skip-jstests".')

    def handle(self, *args, **options):
        appnames = options['appnames']
        skipgroups = options['skipgroups']
        skipgroups = set(skipgroups or [])
        if appnames:
            try:
                settings.IEVVTASKS_BUILDSTATIC_APPS.validate_appnames(appnames=appnames)
            except ValueError as error:
                self.stderr.write(str(error))
                raise SystemExit()
        settings.IEVVTASKS_BUILDSTATIC_APPS.log_help_header()
        settings.IEVVTASKS_BUILDSTATIC_APPS.configure_logging()
        settings.IEVVTASKS_BUILDSTATIC_APPS.install(appnames=appnames, skipgroups=skipgroups)
        settings.IEVVTASKS_BUILDSTATIC_APPS.run(appnames=appnames, skipgroups=skipgroups)
        if options['watch']:
            settings.IEVVTASKS_BUILDSTATIC_APPS.watch(appnames=appnames, skipgroups=skipgroups)
