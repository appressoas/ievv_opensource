from __future__ import unicode_literals

import os

from ievv_opensource.utils.ievvbuildstatic import pluginbase
from ievv_opensource.utils.ievvbuildstatic import utils
from ievv_opensource.utils.ievvbuildstatic.installers.npm import NpmInstaller
from ievv_opensource.utils.shellcommandmixin import ShellCommandMixin, ShellCommandError


class JavascriptMerger(object):
    def __init__(self):
        self.javascript_filepaths = []

    def add(self, javascript_filepath):
        self.javascript_filepaths.append(javascript_filepath)

    def merge(self, rootdirectory):
        output = []
        for javascript_filepath in self.javascript_filepaths:
            filecontent = open(javascript_filepath, 'rb').read().decode('utf-8')
            output.append('/* {} */'.format(
                            os.path.relpath(javascript_filepath, rootdirectory)))
            output.append(filecontent)
        return '\n\n'.join(output)


class Plugin(pluginbase.Plugin, ShellCommandMixin):
    """
    CoffeeScript build plugin --- builds .coffee files into css, and supports watching
    for changes.

    Examples:

        Very simple example where the source file is in
        ``demoapp/staticsources/scripts/coffeescript/app.coffee``::

            IEVVTASKS_BUILDSTATIC_APPS = ievvbuildstatic.config.Apps(
                ievvbuildstatic.config.App(
                    appname='demoapp',
                    version='1.0.0',
                    plugins=[
                        ievvbuildstatic.coffeebuild.Plugin(sourcefile='app.coffee'),
                    ]
                )
            )
    """

    name = 'coffeebuild'

    def __init__(self, destinationfile, sourcefile_include_patterns=None,
                 sourcefile_exclude_patterns=None,
                 sourcefolder=os.path.join('scripts', 'coffeescript'),
                 extra_watchfolders=None):
        """
        Parameters:
            sourcefile_include_patterns: List of source file regexes. Same format as
                as for :class:`ievv_opensource.utils.ievvbuildstatic.utils.RegexFileList`.
                Defaults to ``['^.*\.coffee$']``.
            sourcefile_exclude_patterns: List of source file regexes. Same format as
                as for :class:`ievv_opensource.utils.ievvbuildstatic.utils.RegexFileList`.
            sourcefolder: The folder where ``sourcefiles`` is located relative to
                the source folder of the :class:`~ievv_opensource.utils.ievvbuild.config.App`.
                Defaults to ``scripts/coffeescript``.
            extra_watchfolders: List of extra folders to watch for changes.
                Relative to the source folder of the
                :class:`~ievv_opensource.utils.ievvbuild.config.App`.
        """
        self.destinationfile = destinationfile
        self.sourcefiles = utils.RegexFileList(
            include_patterns=sourcefile_include_patterns or ['^.*\.coffee$'],
            exclude_patterns=sourcefile_exclude_patterns
        )
        self.sourcefolder = sourcefolder
        self.extra_watchfolders = extra_watchfolders or []

    def get_sourcefolder_path(self):
        return self.app.get_source_path(self.sourcefolder)

    def get_destinationfile_path(self):
        return self.app.get_destination_path(self.destinationfile)

    def get_coffee_version(self):
        return None

    def install(self):
        self.app.get_installer(NpmInstaller).queue_install(
            'coffee-script', version=self.get_coffee_version())

    def get_coffee_executable(self):
        return self.app.get_installer(NpmInstaller).find_executable('coffee')

    def get_all_sourcefiles(self):
        return self.sourcefiles.get_files_as_list(rootfolder=self.get_sourcefolder_path())

    def compile_coffescript_file(self, js_directory, relative_filepath):
        executable = self.get_coffee_executable()
        sourcefile_path = os.path.join(self.get_sourcefolder_path(), relative_filepath)
        destinationfile_directory = os.path.dirname(
            os.path.join(js_directory, relative_filepath))
        try:
            self.run_shell_command(executable,
                                   args=[
                                       '-b',
                                       '-o', destinationfile_directory,
                                       '-c', sourcefile_path,
                                   ])
        except ShellCommandError:
            self.get_logger().error('CoffeeScript build of {!r} FAILED!'.format(
                relative_filepath))
            raise
        else:
            self.get_logger().debug('CoffeeScript build of {!r} successful :)'.format(
                relative_filepath))

    def build_coffeescript_files(self, js_directory):
        for relative_filepath in self.get_all_sourcefiles():
            self.compile_coffescript_file(
                js_directory=js_directory,
                relative_filepath=relative_filepath)

    def merge_javascript_files(self, js_directory):
        javascript_merger = JavascriptMerger()
        for root, dirs, files in os.walk(js_directory):
            for filename in files:
                filepath = os.path.abspath(os.path.join(root, filename))
                javascript_merger.add(filepath)
        return javascript_merger.merge(rootdirectory=js_directory)

    def build(self, temporary_directory):
        js_directory = os.path.join(temporary_directory, 'js')
        os.mkdir(js_directory)
        try:
            self.build_coffeescript_files(js_directory=js_directory)
        except ShellCommandError:
            self.get_logger().command_error('CoffeeScript build FAILED!')
        else:
            javascript_source = self.merge_javascript_files(js_directory=js_directory)
            open(self.get_destinationfile_path(), 'wb').write(
                javascript_source.encode('utf-8'))
            self.get_logger().command_success(
                'CoffeeScript build successful :) Output in {}'.format(
                    self.get_destinationfile_path()))

    def run(self):
        self.get_logger().command_start('CoffeeScript building all files in {!r} matching {}'.format(
            self.get_sourcefolder_path(),
            self.sourcefiles.prettyformat_patterns()))
        temporary_directory = self.make_temporary_build_directory()
        try:
            self.build(temporary_directory=temporary_directory)
        except:
            self.delete_temporary_build_directory()
            raise
        else:
            self.delete_temporary_build_directory()

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
        return ['^.+[.]coffee$']

    def __str__(self):
        return '{}({})'.format(super(Plugin, self).__str__(), self.sourcefolder)
