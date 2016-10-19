import json
import os
from collections import OrderedDict

from ievv_opensource.utils.ievvbuildstatic.installers.base import AbstractInstaller
from ievv_opensource.utils.shellcommandmixin import ShellCommandError


class NpmInstallerError(Exception):
    pass


class PackageJsonDoesNotExist(NpmInstallerError):
    pass


class NpmInstaller(AbstractInstaller):
    """
    NPM installer.
    """
    name = 'npminstall'

    def __init__(self, *args, **kwargs):
        super(NpmInstaller, self).__init__(*args, **kwargs)
        self.queued_packages = OrderedDict()

    def __validate_installtype(self, installtype):
        installtypes = (None, "dev", "optional")
        if installtype not in installtypes:
            raise ValueError(
                'Invalid installtype {installtype!r}. Must be '
                'one of {installtypes}'.format(
                    installtype=installtype,
                    installtypes=', '.join(installtypes)
                ))

    def queue_install(self, package, version=None, installtype=None):
        """
        Installs the given npm package in the build
        directory for the app.

        Does nothing if the package is already installed.

        Parameters:
            package: The package name.
            version: The package version.
            installtype: Determines where the package ends up in
                package.json. Can be one of:

                - ``None`` (the default): Ends up in dependencies.
                - ``"dev"``: Ends up in devDependencies.
                - ``"optional"`` (the default): Ends up in optionalDependencies.
        """
        self.__validate_installtype(installtype=installtype)
        self.get_logger().debug('Queued install of {} (version={}) for {}.'.format(
            package, version, self.app.appname))
        queue = True
        if package in self.queued_packages:
            queued_version = self.queued_packages[package]
            if version is None:
                queue = False
            elif queued_version is None:
                queue = True
            else:
                self.get_logger().warning(
                    'Multiple explicit versions of the same NPM package {package} '
                    'specified for {appname}: {version!r} and {queued_version!r}. '
                    'Using {version!r}.'.format(
                        package=package,
                        version=version,
                        queued_version=queued_version,
                        appname=self.app.appname))
                queue = True
        if queue:
            self.queued_packages[package] = {
                'version': version,
                'installtype': installtype
            }

    def get_packagejson_path(self):
        return self.app.get_source_path('package.json')

    def packagejson_exists(self):
        return os.path.exists(self.get_packagejson_path())

    def packagejson_created_by_ievv_buildstatic(self):
        return 'ievv_buildstatic' in self.get_packagejson_dict()

    def create_packagejson(self):
        packagedata = {
            'name': self.app.appname,
            'private': True,
            'ievv_buildstatic': {},
            # We do not care about the version. We are not building a distributable package.
            'version': '0.0.1',
        }
        open(self.get_packagejson_path(), 'wb').write(
            json.dumps(packagedata, indent=2).encode('utf-8'))

    def __get_packagejson_dict(self):
        package_json_string = open(self.get_packagejson_path()).read()
        package_json_dict = json.loads(package_json_string)
        return package_json_dict

    def get_packagejson_dict(self):
        if not hasattr(self, '_packagejson_dict'):
            self._packagejson_dict = self.__get_packagejson_dict()
        return self._packagejson_dict

    def get_packagejson_key_from_installtype(self, installtype):
        if installtype is None:
            return 'dependencies'
        elif installtype == 'dev':
            return 'devDependencies'
        elif installtype == 'optional':
            return 'optionalDependencies'

    def package_is_in_packages_json(self, package, properties):
        package_json_dict = self.get_packagejson_dict()
        key = self.get_packagejson_key_from_installtype(installtype=properties['installtype'])
        packages = package_json_dict.get(key, {})
        return package in packages

    def install_packages_from_packagejson(self):
        try:
            self.run_shell_command('yarn',
                                   args=['--json'],
                                   _cwd=self.app.get_source_path())
        except ShellCommandError:
            self.get_logger().command_error('yarn FAILED!')
            raise SystemExit()
        else:
            self.get_logger().command_success('yarn succeeded :)')

    def yarn_json_output_handler(self, outputdict):
        messagetype = outputdict.get('type')
        data = outputdict.get('data', {})
        ignored_messagetypes = {
            'progressTick',
            'step',
        }
        ignored_messages = {
            'Saved 0 new dependencies.',
            'Saved lockfile.',
        }
        if isinstance(data, dict):
            message = data.get('message')
        elif isinstance(data, str):
            message = data
        else:
            message = None
        if message and messagetype and message not in ignored_messages:
            if messagetype == 'error':
                super(NpmInstaller, self).log_shell_command_stderr(line=message)
            elif messagetype not in ignored_messagetypes:
                super(NpmInstaller, self).log_shell_command_stdout(line=message)

    def log_shell_command_stdout(self, line):
        try:
            outputdict = json.loads(line)
        except ValueError:
            super(NpmInstaller, self).log_shell_command_stdout(line=line)
        else:
            self.yarn_json_output_handler(outputdict=outputdict)

    def log_shell_command_stderr(self, line):
        try:
            outputdict = json.loads(line)
        except ValueError:
            super(NpmInstaller, self).log_shell_command_stdout(line=line)
        else:
            self.yarn_json_output_handler(outputdict=outputdict)

    def yarn_install_package(self, package, properties):
        package_spec = package
        if properties['version']:
            package_spec = '{package}@{version}'.format(
                package=package, version=package['version'])
        args = ['add', '--json', package_spec]
        if properties['installtype'] is not None:
            args.append('--{}'.format(properties['installtype']))
        try:
            self.run_shell_command('yarn',
                                   args=args,
                                   _cwd=self.app.get_source_path())
        except ShellCommandError:
            self.get_logger().command_error(
                'yarn add {package} (properties: {properties!r}) FAILED!'.format(
                    package=package, properties=properties))
            raise SystemExit()

    def npm_install_package(self, package, properties):
        package_spec = package
        if package['version']:
            package_spec = '{package}@{version}'.format(
                package=package, version=package['version'])
        args = ['install', package_spec]
        if properties['installtype'] is None:
            args.append('--save')
        else:
            args.append('--save-{}'.format(properties['installtype']))
        try:
            self.run_shell_command('npm',
                                   args=args,
                                   _cwd=self.app.get_source_path())
        except ShellCommandError:
            self.get_logger().command_error(
                'npm install {package} (properties: {properties!r}) FAILED!'.format(
                    package=package, properties=properties))
            raise SystemExit()

    def install_queued_packages(self):
        for package, properties in self.queued_packages.items():
            if not self.package_is_in_packages_json(package=package,
                                                    properties=properties):
                self.yarn_install_package(package=package, properties=properties)

    def install(self):
        self.get_logger().command_start(
            'Installing npm packages for {}'.format(self.app.get_source_path()))
        if self.packagejson_exists() and self.packagejson_created_by_ievv_buildstatic():
            self.install_packages_from_packagejson()
        else:
            self.create_packagejson()
        self.install_queued_packages()

    def find_executable(self, executablename):
        """
        Find an executable named ``executablename``.

        Returns the absolute path to the executable.
        """
        executablepath = self.app.get_source_path(
            'node_modules', '.bin', executablename)
        return executablepath

    # def log_shell_command_stderr(self, line):
    #     if 'npm WARN package.json' in line:
    #         return
    #     super(NpmInstaller, self).log_shell_command_stderr(line)

    def get_package_json_dict_for_package(self, package_name):
        package_json_path = self.app.get_source_path(
            'node_modules', package_name, 'package.json')
        package_json_string = open(package_json_path).read()
        package_json_dict = json.loads(package_json_string)
        return package_json_dict

    def get_package_version(self, package_name):
        return self.get_package_json_dict_for_package(package_name)['version']

    def get_installed_package_names(self):
        if not os.path.exists(self.get_packagejson_path()):
            raise PackageJsonDoesNotExist()
        package_json_string = open(self.get_packagejson_path()).read()
        package_json_dict = json.loads(package_json_string)
        package_names = []
        for package_name, version in package_json_dict.get('devDependencies', {}).items():
            package_names.append(package_name)
        return package_names
