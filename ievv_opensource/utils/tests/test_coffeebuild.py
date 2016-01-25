from __future__ import unicode_literals
import os
import shutil
import tempfile
from unittest import mock

from django import test

from ievv_opensource.utils import ievvbuildstatic


class MockApp(ievvbuildstatic.config.App):
    def __init__(self, appname='testapp', version='1.0', appfolder='testapp', **kwargs):
        self.appfolder = appfolder
        super(MockApp, self).__init__(appname=appname, version=version, **kwargs)

    def get_app_config(self):
        mock_app_config = mock.MagicMock
        mock_app_config.path = self.appfolder
        return mock_app_config


class TestCoffeeBuildPlugin(test.TestCase):
    def tearDown(self):
        if hasattr(self, 'temporary_directory'):
            shutil.rmtree(self.temporary_directory)

    def test_init(self):
        plugin = ievvbuildstatic.coffeebuild.Plugin(sourcefile='test.coffee')
        self.assertEqual('scripts', plugin.sourcefolder)
        self.assertEqual(os.path.join('scripts', 'test.coffee'), plugin.sourcefile)

    def test_get_sourcefile_path(self):
        plugin = ievvbuildstatic.coffeebuild.Plugin(sourcefile='test.coffee')
        plugin.app = MockApp(plugins=[plugin])
        self.assertEqual(os.path.join('testapp', 'staticsources', 'testapp', 'scripts', 'test.coffee'),
                         plugin.get_sourcefile_path())

    def test_get_sourcefolder_path(self):
        plugin = ievvbuildstatic.coffeebuild.Plugin(sourcefile='test.coffee')
        plugin.app = MockApp(plugins=[plugin])
        self.assertEqual(os.path.join('testapp', 'staticsources', 'testapp', 'scripts'),
                         plugin.get_sourcefolder_path())

    def test_get_destinationfile_path(self):
        plugin = ievvbuildstatic.coffeebuild.Plugin(sourcefile='test.coffee')
        plugin.app = MockApp(plugins=[plugin])
        self.assertEqual(os.path.join('testapp', 'static', 'testapp', '1.0', 'scripts', 'test.js'),
                         plugin.get_destinationfile_path())

    def test_is_coffeescript_filename(self):
        plugin = ievvbuildstatic.coffeebuild.Plugin(sourcefile='test.coffee')
        self.assertTrue(plugin.is_coffeescript_filename('test.coffee'))
        self.assertFalse(plugin.is_coffeescript_filename('test.js'))

    def __get_temporary_app_directory(self):
        self.temporary_directory = tempfile.mkdtemp()
        return self.temporary_directory

    def __make_folder(self, rootdirectory, foldermap):
        for key, value in foldermap.items():
            keypath = os.path.join(rootdirectory, key)
            if isinstance(value, dict):
                self.__make_folder(rootdirectory=keypath, foldermap=value)
            else:
                directorypath = os.path.dirname(keypath)
                if not os.path.exists(directorypath):
                    os.makedirs(directorypath)
                open(keypath, 'wb').write(value.encode('utf-8'))

    def test_get_extra_source_files(self):
        plugin = ievvbuildstatic.coffeebuild.Plugin(sourcefile='app.coffee')
        plugin.app = MockApp(plugins=[plugin], appfolder=self.__get_temporary_app_directory())
        self.__make_folder(
            rootdirectory=plugin.app.get_appfolder(),
            foldermap={
                'staticsources': {
                    'testapp': {
                        'scripts': {
                            'app.coffee': 'app',
                            'other.coffee': 'other',
                            'directives': {
                                'main.coffee': 'main'
                            }
                        }
                    }
                }
            })
        self.assertEqual(
            [
                plugin.app.get_source_path('scripts/directives', 'main.coffee'),
                plugin.app.get_source_path('scripts', 'other.coffee'),
            ],
            plugin.get_extra_source_files()
        )

    def test_get_all_source_files(self):
        plugin = ievvbuildstatic.coffeebuild.Plugin(sourcefile='app.coffee')
        plugin.app = MockApp(plugins=[plugin], appfolder=self.__get_temporary_app_directory())
        self.__make_folder(
            rootdirectory=plugin.app.get_appfolder(),
            foldermap={
                'staticsources': {
                    'testapp': {
                        'scripts': {
                            'app.coffee': 'app',
                            'other.coffee': 'other',
                            'directives': {
                                'main.coffee': 'main'
                            }
                        }
                    }
                }
            })
        self.assertEqual(
            [
                plugin.get_sourcefile_path(),
                plugin.app.get_source_path('scripts/directives', 'main.coffee'),
                plugin.app.get_source_path('scripts', 'other.coffee'),
            ],
            plugin.get_all_source_files()
        )

    # def test_get_external_js_files_absolute_paths(self):
    #     plugin = ievvbuildstatic.coffeebuild.Plugin(
    #         sourcefile='app.coffee',
    #         js_library_files=[
    #             'jslibraries/libone/scripts/stuff.js',
    #             'jslibraries/libtwo/lib.js',
    #         ])
    #     plugin.app = MockApp(plugins=[plugin])
    #     self.assertEqual(
    #         [
    #             os.path.join('testapp', 'staticsources', 'testapp',
    #                          'jslibraries', 'libone', 'scripts', 'stuff.js'),
    #             os.path.join('testapp', 'staticsources', 'testapp',
    #                          'jslibraries', 'libtwo', 'lib.js'),
    #         ],
    #         plugin.get_external_js_files_absolute_paths()
    #     )

    def test_merge_all_js_libraries(self):
        plugin = ievvbuildstatic.coffeebuild.Plugin(
            sourcefile='app.coffee',
            js_library_files=[
                'jslibraries/libone/scripts/stuff.js',
                'jslibraries/libtwo/lib.js',
            ])
        plugin.app = MockApp(plugins=[plugin], appfolder=self.__get_temporary_app_directory())
        self.__make_folder(
            rootdirectory=plugin.app.get_appfolder(),
            foldermap={
                'staticsources': {
                    'testapp': {
                        'jslibraries': {
                            'libone': {
                                'scripts': {
                                    'stuff.js': 'console.log("Stuff");'
                                }
                            },
                            'libtwo': {
                                'lib.js': 'console.log("The lib");'
                            }
                        }
                    }
                }
            })
        self.assertEqual(
            '\n'
            '\n'
            '// >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n'
            '// BEGIN jslibraries/libone/scripts/stuff.js\n'
            '// >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'
            '\n'
            '\n'
            'console.log("Stuff");\n'
            '\n'
            '// <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n'
            '// END jslibraries/libone/scripts/stuff.js\n'
            '// <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n'
            '\n'
            '\n'
            '// >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n'
            '// BEGIN jslibraries/libtwo/lib.js\n'
            '// >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n'
            '\n'
            'console.log("The lib");\n'
            '\n'
            '// <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n'
            '// END jslibraries/libtwo/lib.js\n'
            '// <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n',
            plugin.merge_all_js_libraries()
        )

    def test_merge_built_coffeescript_with_js_libraries(self):
        plugin = ievvbuildstatic.coffeebuild.Plugin(
            sourcefile='app.coffee',
            js_library_files=[
                'jslibraries/lib.js',
            ])
        plugin.app = MockApp(plugins=[plugin], appfolder=self.__get_temporary_app_directory())
        self.__make_folder(
            rootdirectory=plugin.app.get_appfolder(),
            foldermap={
                'static': {
                    'testapp': {
                        '1.0': {
                            'scripts': {
                                'app.js': 'console.log("The app")'
                            }
                        }
                    }
                },
                'staticsources': {
                    'testapp': {
                        'jslibraries': {
                            'lib.js': 'console.log("The JS lib");'
                        }
                    }
                }
            })
        self.assertEqual(
            '\n'
            '\n'
            '// >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n'
            '// BEGIN jslibraries/lib.js\n'
            '// >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n'
            '\n'
            'console.log("The JS lib");\n'
            '\n'
            '// <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n'
            '// END jslibraries/lib.js\n'
            '// <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n'
            '\n'
            '\n'
            '// >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n'
            '// BEGIN CoffeeScript output\n'
            '// >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n'
            '\n'
            'console.log("The app")\n',
            plugin.merge_built_coffeescript_with_js_libraries()
        )

    def test_get_built_js_file_paths(self):
        plugin = ievvbuildstatic.coffeebuild.Plugin(sourcefile='app.coffee')
        plugin.app = MockApp(plugins=[plugin], appfolder=self.__get_temporary_app_directory())
        self.__make_folder(
            rootdirectory=plugin.app.get_appfolder(),
            foldermap={
                'staticsources': {
                    'testapp': {
                        'scripts': {
                            'app.coffee': 'app',
                            'other.coffee': 'other',
                            'directives': {
                                'main.coffee': 'main'
                            }
                        }
                    }
                }
            })
        self.assertEqual(
            [
                plugin.app.get_source_path('coffeescript_buildtemp', 'app.js'),
                plugin.app.get_source_path('coffeescript_buildtemp', 'directives', 'main.js'),
                plugin.app.get_source_path('coffeescript_buildtemp', 'other.js'),
            ],
            plugin.get_built_js_file_paths()
        )

    def test_merge_all_built_js_files(self):
        plugin = ievvbuildstatic.coffeebuild.Plugin(sourcefile='app.coffee')
        plugin.app = MockApp(plugins=[plugin], appfolder=self.__get_temporary_app_directory())
        self.__make_folder(
            rootdirectory=plugin.app.get_appfolder(),
            foldermap={
                'staticsources': {
                    'testapp': {
                        'scripts': {
                            'app.coffee': 'app',
                            'other.coffee': 'other',
                            'directives': {
                                'main.coffee': 'main'
                            }
                        },
                        'coffeescript_buildtemp': {
                            'app.js': 'app',
                            'other.js': 'other',
                            'directives': {
                                'main.js': 'main'
                            }
                        }
                    }
                }
            })
        self.assertEqual(
            '\n'
            '\n'
            '// >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n'
            '// BEGIN scripts/app.coffee\n'
            '// >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n'
            '\n'
            'app\n'
            '\n'
            '// <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n'
            '// END scripts/app.coffee\n'
            '// <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n'
            '\n'
            '\n'
            '// >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n'
            '// BEGIN scripts/directives/main.coffee\n'
            '// >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n'
            '\n'
            'main\n'
            '\n'
            '// <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n'
            '// END scripts/directives/main.coffee\n'
            '// <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n'
            '\n'
            '\n'
            '// >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n'
            '// BEGIN scripts/other.coffee\n'
            '// >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n'
            '\n'
            'other\n'
            '\n'
            '// <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n'
            '// END scripts/other.coffee\n'
            '// <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n',
            plugin.merge_all_built_js_files()
        )
