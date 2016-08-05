from __future__ import unicode_literals

import json
import os

import sh

from ievv_opensource.utils.ievvbuildstatic import pluginbase
from ievv_opensource.utils.ievvbuildstatic import utils
from ievv_opensource.utils.ievvbuildstatic.installers.npm import NpmInstaller
from ievv_opensource.utils.shellcommandmixin import ShellCommandMixin, ShellCommandError


class Plugin(pluginbase.Plugin, ShellCommandMixin):
    name = 'typescriptbuild'

    def __init__(self,
                 destinationfile,
                 sourcefile_include_patterns=None,
                 sourcefile_exclude_patterns=None,
                 sourcefolder=os.path.join('scripts', 'typescript'),
                 destinationfolder=os.path.join('scripts'),
                 extra_watchfolders=None,
                 with_function_wrapper=True,
                 lint=True,
                 lintconfig=None,
                 tsc_compiler_options=None):

        self.destinationfile = destinationfile
        self.sourcefiles = utils.RegexFileList(
            include_patterns=sourcefile_include_patterns or ['^.*\.ts'],
            exclude_patterns=sourcefile_exclude_patterns
        )
        self.destinationfolder = destinationfolder
        self.sourcefolder = sourcefolder
        self.extra_watchfolders = extra_watchfolders or []
        self.with_function_wrapper = with_function_wrapper
        self.lint = lint
        self.lintconfig = lintconfig or {}
        self.tsc_compiler_options = {
            "target": "es5",
            "module": "commonjs",
            "moduleResolution": "node",
            "sourceMap": True,
            "emitDecoratorMetadata": True,
            "experimentalDecorators": True,
            "removeComments": False,
            "noImplicitAny": True,
            "suppressImplicitAnyIndexErrors": True
        }
        if tsc_compiler_options:
            self.tsc_compiler_options.update(tsc_compiler_options);

    def get_sourcefolder_path(self):
        return self.app.get_source_path(self.sourcefolder)

    def get_destinationfile_path(self):
        return self.app.get_destination_path(self.destinationfolder, self.destinationfile)

    def get_typescript_version(self):
        return None

    def get_tslint_version(self):
        return None

    def install(self):
        self.app.get_installer(NpmInstaller).queue_install(
            'typescript', version=self.get_typescript_version())
        if self.lint:
            self.app.get_installer(NpmInstaller).queue_install(
                'tslint', version=self.get_tslint_version())

    def get_tsc_executable(self):
        return self.app.get_installer(NpmInstaller).find_executable('tsc')

    def get_tslint_executable(self):
        return self.app.get_installer(NpmInstaller).find_executable('tslint')

    def get_all_sourcefiles(self, absolute_paths=False):
        return self.sourcefiles.get_files_as_list(rootfolder=self.get_sourcefolder_path(), absolute_paths=absolute_paths)

    def lint_typescript_file(self, relative_filepath, lintconfig_path):
        executable = self.get_tslint_executable()
        sourcefile_path = os.path.join(self.get_sourcefolder_path(), relative_filepath)
        self.get_logger().debug('Typescript linting {!r}'.format(
            relative_filepath))
        try:
            self.run_shell_command(executable,
                                   args=[
                                       '-f', lintconfig_path,
                                       sourcefile_path
                                   ])
        except ShellCommandError:
            self.get_logger().error('Typescript linting of {!r} FAILED!'.format(
                relative_filepath))

    def make_lintconfig_file(self, temporary_directory):
        lintconfig_path = os.path.join(temporary_directory, 'coffeelint.json')
        try:
            coffeelint = sh.Command(self.get_tslint_executable())
            default_lintconfig_json = coffeelint('--makeconfig',
                                                 _err=self.log_shell_command_stderr)
        except sh.ErrorReturnCode:
            self.get_logger().error('Failed to create coffeelint config file.')
            raise ShellCommandError()
        else:
            lintconfig = json.loads(str(default_lintconfig_json))
            lintconfig.update(self.lintconfig)
            open(lintconfig_path, 'wb').write(json.dumps(lintconfig, indent=2).encode('utf-8'))
            return lintconfig_path

    def lint_typecript_files(self, temporary_directory):
        # lintconfig_path = self.make_lintconfig_file(temporary_directory=temporary_directory)
        # for relative_filepath in self.get_all_sourcefiles():
        #     self.lint_typescript_file(relative_filepath=relative_filepath,
        #                               lintconfig_path=lintconfig_path)
        pass

    def make_tsconfig_dict(self, output_directory):
        tsc_compiler_options = self.tsc_compiler_options.copy()
        tsc_compiler_options['outDir'] = output_directory
        output = {
            "compilerOptions": tsc_compiler_options,
            "files": self.get_all_sourcefiles(absolute_paths=True)
        }
        return output

    def make_tsconfig(self, output_directory):
        tsconfig_dict = self.make_tsconfig_dict(output_directory)
        path = self.app.get_source_path("tsconfig.json")
        open(path, 'wb').write(json.dumps(tsconfig_dict, indent=2).encode('utf-8'))

    def compile_typescript(self):
        executable = self.get_tsc_executable()
        sourcefolder_path = self.get_sourcefolder_path()

        try:
            self.run_shell_command(executable, _cwd=self.app.get_source_path())
        except ShellCommandError:
            self.get_logger().error('TypeScript build of {!r} FAILED!'.format(sourcefolder_path))
            raise
        else:
            self.get_logger().debug('TypeScript build of {!r} successful :)'.format(sourcefolder_path))

    def build(self, temporary_directory):
        if self.lint:
            self.lint_typecript_files(temporary_directory=temporary_directory)
        js_directory = os.path.join(temporary_directory, 'js')
        os.mkdir(js_directory)
        self.make_tsconfig(js_directory)

        try:
            self.compile_typescript()
        except ShellCommandError:
            self.get_logger().command_error('Typescript build FAILED!')
        else:
            # javascript_source = self.merge_javascript_files(js_directory=js_directory)
            # destination_directory = os.path.dirname(self.get_destinationfile_path())
            # if not os.path.exists(destination_directory):
            #     os.makedirs(destination_directory)
            # open(self.get_destinationfile_path(), 'wb').write(
            #     javascript_source.encode('utf-8'))
            self.get_logger().command_success(
                'TypeScript build successful :) Output in {}'.format(
                    self.get_destinationfile_path()))

    def run(self):
        self.get_logger().command_start('TypeScript building all files in {!r} matching {}'.format(
            self.get_sourcefolder_path(),
            self.sourcefiles.prettyformat_patterns()))
        temporary_directory = self.make_temporary_build_directory()
        try:
            self.build(temporary_directory=temporary_directory)
        except:
            # self.delete_temporary_build_directory()
            raise
        # else:
            # self.delete_temporary_build_directory()

    def get_extra_watchfolder_paths(self):
        return map(self.app.get_source_path, self.extra_watchfolders)

    def get_watch_folders(self):
        """
        We only watch the folder where the coffee sources are located,
        so this returns the absolute path of the ``sourcefolder``.
        """
        folders = [self.app.get_source_path(self.sourcefolder)]
        if self.extra_watchfolders:
            folders.extend(self.get_extra_watchfolder_paths())
        return folders

    def get_watch_regexes(self):
        return ['^.+[.]ts']

    def __str__(self):
        return '{}({})'.format(super(Plugin, self).__str__(), self.sourcefolder)
