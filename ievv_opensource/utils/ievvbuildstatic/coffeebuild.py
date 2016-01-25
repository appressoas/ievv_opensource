from __future__ import unicode_literals
import os
import shutil

from ievv_opensource.utils.ievvbuildstatic import pluginbase
from ievv_opensource.utils.ievvbuildstatic.installers.npm import NpmInstaller
from ievv_opensource.utils.shellcommandmixin import ShellCommandMixin, ShellCommandError


JS_FILE_WRAPPER_TEMPLATE = """

// >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
// BEGIN {filepath}
// >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

{sourcecode}

// <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
// END {filepath}
// <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
"""

MERGE_JS_AND_COFFEESCRIPT_TEMPLATE = """{jslibraries}

// >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
// BEGIN CoffeeScript output
// >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

{built_coffeescript}
"""


class Plugin(pluginbase.Plugin, ShellCommandMixin):
    """
    CoffeeScript build plugin --- builds .coffee files into javascript, and supports watching
    for changes.

    Examples:

        Very simple example where the source file is in
        ``demoapp/staticsources/javascript/app.coffee``, and that
        is the only source file::

            IEVVTASKS_BUILDSTATIC_APPS = ievvbuildstatic.config.Apps(
                ievvbuildstatic.config.App(
                    appname='demoapp',
                    version='1.0.0',
                    plugins=[
                        ievvbuildstatic.coffeebuild.Plugin(
                            sourcefile='app.coffee'
                        ),
                    ]
                )
            )
    """

    name = 'coffeebuild'

    def __init__(self, sourcefile, sourcefolder='scripts',
                 other_sourcefolders=None,
                 js_library_files=None):
        """
        Parameters:
            sourcefile: Main source file (the one including all other less files)
                relative to ``sourcefolder``. The JS file built from this coffeescript
                file is added to the built JS file below any ``js_library_files``, but
                 above any other coffeescript files.
            sourcefolder: The folder where ``sourcefile`` is located relative to
                the source folder of the :class:`~ievv_opensource.utils.ievvbuild.config.App`.
                All coffee files in this folder (recursively) is added to the built JS file.
                Defaults to ``"scripts"``.
            other_sourcefolders (list): Other source folders. All coffeescript files in these
                folders is added to the built JS file.
            js_library_files (list): List of javascript files to include in the build.
                Paths are relative to the source folder of the app.
                These are added to the top of the built JS file in the listed order.
        """
        self.sourcefolder = sourcefolder
        self.other_sourcefolders = other_sourcefolders
        self.js_library_files = js_library_files
        self.sourcefile = os.path.join(sourcefolder, sourcefile)

    def get_sourcefile_path(self):
        return self.app.get_source_path(self.sourcefile)

    def get_sourcefolder_path(self):
        return self.app.get_source_path(self.sourcefolder)

    def get_destinationfile_path(self):
        return self.app.get_destination_path(self.sourcefile, new_extension='.js')

    def get_destinationfile_directory(self):
        return self.app.get_destination_path(self.sourcefolder)

    def get_other_sourcefolders_paths(self):
        return map(self.app.get_source_path, self.other_sourcefolders)

    def format_less_include_paths(self):
        if self.less_include_paths:
            return ':'.join(map(self.app.get_source_path, self.less_include_paths))
        else:
            return ''

    def get_coffee_version(self):
        """
        Override this if you want to use an exact version of the
        ``coffee-script`` package.

        Should return a version number compatible with ``npm install``,
        or ``None`` to use the latest version of the ``coffee-script``
        npm package.
        """
        return None

    def get_coffee_maker_version(self):
        """
        Override this if you want to use an exact version of the
        ``coffee-maker`` package.

        Should return a version number compatible with ``npm install``,
        or ``None`` to use the latest version of the ``coffee-maker``
        npm package.
        """
        return None

    def get_uglify_version(self):
        """
        Override this if you want to use an exact version of the
        ``uglify-js`` package.

        Should return a version number compatible with ``npm install``,
        or ``None`` to use the latest version of the ``uglify-js``
        npm package.
        """
        return None

    def install(self):
        self.app.get_installer(NpmInstaller).queue_install(
            'coffee-script', version=self.get_coffee_version())
        self.app.get_installer(NpmInstaller).queue_install(
            'coffee-maker', version=self.get_coffee_maker_version())
        self.app.get_installer(NpmInstaller).queue_install(
            'uglify-js', version=self.get_uglify_version())

    def is_coffeescript_filename(self, filename):
        """
        Should return ``True`` if the given ``filename`` is a coffeescript file.
        The only reason to override this would be if you use something other
        than ``.coffee`` for you Coffeescript sources.
        """
        return filename.endswith('.coffee')

    def is_sourcefile(self, full_coffeescript_filepath):
        """
        You can override this if you want to exclude some files.

        Args:
            full_coffeescript_filepath: The absolute path of the coffeescript file.
                The filename has already been validated as a coffeescript file
                by :meth:`.is_coffeescript_filename` before it is sent to this
                method.
        """
        return True

    def get_all_sourcefiles_in_folder(self, folderpath):
        coffee_files = []
        sourcefile_path = self.get_sourcefile_path()
        for (dirpath, dirnames, filenames) in os.walk(folderpath):
            for filename in filenames:
                if self.is_coffeescript_filename(filename):
                    full_filepath = os.path.join(dirpath, filename)
                    if full_filepath != sourcefile_path and self.is_sourcefile(full_filepath):
                        coffee_files.append(full_filepath)
        coffee_files.sort()
        return coffee_files

    def get_extra_source_files(self):
        return self.get_all_sourcefiles_in_folder(self.get_sourcefolder_path())

    def get_all_source_files(self):
        source_files = [self.app.get_source_path(self.sourcefile)]
        source_files.extend(self.get_extra_source_files())
        return source_files

    # def get_external_js_files_absolute_paths(self):
    #     return [
    #             for js_library_file in self.js_library_files]

    def get_build_directory(self):
        return self.app.get_source_path('coffeescript_buildtemp')

    def create_build_directory(self):
        self.destroy_build_directory()
        os.makedirs(self.get_build_directory())

    def destroy_build_directory(self):
        if os.path.exists(self.get_build_directory()):
            shutil.rmtree(self.get_build_directory())

    def get_built_js_file_paths(self):
        built_js_file_paths = []
        for coffeepath in self.get_all_source_files():
            relative_coffeepath = os.path.relpath(coffeepath,
                                                  self.app.get_source_path(self.sourcefolder))
            jspath = os.path.splitext(relative_coffeepath)[0] + '.js'
            jspath = os.path.join(self.get_build_directory(), jspath)
            built_js_file_paths.append(jspath)
        return built_js_file_paths

    def __get_coffeescript_relative_path_from_built_javascript_path(self, jsfile_path):
        path = os.path.join(
            self.sourcefolder,
            os.path.relpath(jsfile_path, self.get_build_directory()))
        path = os.path.splitext(path)[0] + '.coffee'
        return path

    def merge_all_built_js_files(self):
        output = []
        for jsfile_path in self.get_built_js_file_paths():
            sourcecode = open(jsfile_path, 'r').read()
            output.append(JS_FILE_WRAPPER_TEMPLATE.format(
                filepath=self.__get_coffeescript_relative_path_from_built_javascript_path(jsfile_path),
                sourcecode=sourcecode
            ))
        return ''.join(output)

    def merge_all_js_libraries(self):
        output = []
        for js_library_file in self.js_library_files:
            js_library_full_path = self.app.get_source_path(js_library_file)
            js_library_code = open(js_library_full_path, 'r').read()
            output.append(JS_FILE_WRAPPER_TEMPLATE.format(
                filepath=js_library_file,
                sourcecode=js_library_code
            ))
        return ''.join(output)

    def merge_built_coffeescript_with_js_libraries(self):
        built_coffeescript = self.merge_all_built_js_files()
        return MERGE_JS_AND_COFFEESCRIPT_TEMPLATE.format(
            jslibraries=self.merge_all_js_libraries(),
            built_coffeescript=built_coffeescript
        )

    def build_coffeescript(self):
        self.get_logger().command_start('Building {}.'.format(self.get_sourcefile_path()))
        self.create_build_directory()
        executable = self.app.get_installer(NpmInstaller).find_executable('coffee')

        # if not os.path.exists(self.get_destinationfile_directory()):
        #     os.makedirs(self.get_destinationfile_directory())
        args = [
            '--compile',
            # '--print',
            '--output', self.get_build_directory()
        ]
        args.extend(self.get_all_source_files())
        try:
            self.run_shell_command(
                executable,
                args=args,
            )
        except ShellCommandError:
            self.get_logger().command_error('CoffeeScript build FAILED!')
            return False
        else:
            self.get_logger().command_success('CoffeeScript build successful :)')
            return True

    def run(self):
        coffee_build_successful = self.build_coffeescript()
        if not coffee_build_successful:
            return
        print()
        print("*" * 70)
        print()
        print(self.merge_built_coffeescript_with_js_libraries())
        print()
        print("*" * 70)
        print()


    def get_watch_folders(self):
        """
        We only watch the folder where the less sources are located,
        so this returns the absolute path of the ``sourcefolder``.
        """
        folders = [self.app.get_source_path(self.sourcefolder)]
        if self.other_sourcefolders:
            folders.extend(self.get_other_sourcefolders_paths())
        return folders

    def get_watch_regexes(self):
        return ['^.+[.]coffee']

    def __str__(self):
        return '{}({})'.format(super(Plugin, self).__str__(), self.sourcefile)
