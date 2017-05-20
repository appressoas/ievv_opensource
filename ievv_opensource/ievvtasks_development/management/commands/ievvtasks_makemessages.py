import fnmatch
import os

from django.conf import settings
from django.core import management
from django.core.management.base import BaseCommand
from django.core.management.utils import handle_extensions


class Command(BaseCommand):
    help = 'Run makemessages for the languages specified in the ' \
           'IEVVTASKS_MAKEMESSAGES_LANGUAGE_CODES setting.'

    def __makemessages(self, ignore, extensions, domain):
        management.call_command(
            'makemessages',
            locale=settings.IEVVTASKS_MAKEMESSAGES_LANGUAGE_CODES,
            ignore=ignore,
            extensions=extensions,
            domain=domain,
            verbosity=self.verbosity)

    def __build_python_translations(self):
        ignore = getattr(settings, 'IEVVTASKS_MAKEMESSAGES_IGNORE', [
            'static/*'
        ])
        extensions = getattr(settings, 'IEVVTASKS_MAKEMESSAGES_EXTENSIONS', [
            'py', 'html', 'txt'])
        self.__makemessages(ignore=ignore,
                            extensions=extensions,
                            domain='django')

    def __is_ignored(self, path, ignore_patterns):
        filename = os.path.basename(path)

        def ignore(pattern):
            return fnmatch.fnmatchcase(filename, pattern) or fnmatch.fnmatchcase(path, pattern)

        return any(ignore(pattern) for pattern in ignore_patterns)

    def __normalize_directory_patterns(self, ignore_patterns):
        norm_patterns = []
        dir_suffixes = {'%s*' % path_sep for path_sep in {'/', os.sep}}
        for p in ignore_patterns:
            for dir_suffix in dir_suffixes:
                if p.endswith(dir_suffix):
                    norm_patterns.append(p[:-len(dir_suffix)])
                    break
            else:
                norm_patterns.append(p)
        return norm_patterns

    def __iterate_jsx_files(self, directory, extensions, ignore_patterns):
        directory_ignore_patterns = self.__normalize_directory_patterns(
            ignore_patterns)
        ignored_roots = [os.path.normpath(p)
                         for p in (settings.MEDIA_ROOT, settings.STATIC_ROOT) if p]
        for dirpath, dirnames, files in os.walk(directory, topdown=True):
            for dirname in dirnames[:]:
                path = os.path.normpath(os.path.join(dirpath, dirname))
                if (self.__is_ignored(path=path, ignore_patterns=directory_ignore_patterns)
                        or path in ignored_roots):
                    dirnames.remove(dirname)
                elif dirname == 'locale':
                    dirnames.remove(dirname)
            for filename in files:
                path = os.path.normpath(os.path.join(dirpath, filename))
                extension = os.path.splitext(filename)[1]
                if extension not in extensions:
                    if self.verbosity > 1:
                        self.stdout.write('ignoring file {} in {} - Extension, {!r}, not in {!r}'.format(
                            filename, dirpath, extension, extensions))
                elif self.__is_ignored(path=path, ignore_patterns=ignore_patterns):
                    if self.verbosity > 1:
                        self.stdout.write('ignoring file {} in {} - Matches ignore pattern.'.format(filename, dirpath))
                else:
                    yield path

    def __postprocess_jsx_files(self, directory, extensions, ignore_patterns):
        try:
            from react import jsx
        except ImportError:
            self.stderr.write('Translating jsx files requires '
                              'react-python (https://github.com/facebookarchive/react-python).')
            raise
        jsxfile_paths = self.__iterate_jsx_files(
                directory=directory,
                extensions=extensions,
                ignore_patterns=ignore_patterns)
        for jsxfile_path in jsxfile_paths:
            print(jsxfile_path)
            jsx.transform(jsxfile_path, js_path='/Users/espenak/code/hellsapp/tull.js')
            break

    def __build_javascript_translations(self, directory):
        ignore_patterns = getattr(settings, 'IEVVTASKS_MAKEMESSAGES_JAVASCRIPT_IGNORE', [
            'node_modules/*',
            'bower_components/*',
            'not_for_deploy/*',
        ])
        ignore_patterns = [os.path.normcase(p) for p in ignore_patterns]
        js_extensions = handle_extensions(getattr(settings, 'IEVVTASKS_MAKEMESSAGES_JAVASCRIPT_EXTENSIONS', [
            'js']))
        jsx_extensions = handle_extensions(getattr(settings, 'IEVVTASKS_MAKEMESSAGES_JSX_EXTENSIONS', [
            'jsx']))
        self.__postprocess_jsx_files(directory=directory,
                                     extensions=jsx_extensions,
                                     ignore_patterns=ignore_patterns)
        # self.__makemessages(ignore=ignore_patterns,
        #                     extensions=extensions,
        #                     domain='djangojs')

    def handle(self, *args, **options):
        current_directory = os.getcwd()
        self.verbosity = options['verbosity']
        for directory in getattr(settings, 'IEVVTASKS_MAKEMESSAGES_DIRECTORIES', [current_directory]):
            directory = os.path.abspath(directory)
            self.stdout.write('Running makemessages for python files in {}'.format(directory))
            os.chdir(directory)
            # self.__build_python_translations()
            if getattr(settings, 'IEVVTASKS_MAKEMESSAGES_BUILD_JAVASCRIPT_TRANSLATIONS', False):
                self.stdout.write('Running makemessages for javascript files in {}'.format(directory))
                self.__build_javascript_translations(directory=directory)
            os.chdir(current_directory)
