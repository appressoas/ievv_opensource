import typing as t

import os
import shutil
import glob

from ievv_opensource.utils.ievvbuildstatic import pluginbase

class Plugin(pluginbase.Plugin):

    def __init__(self, glob_patterns: t.List[str] | str, destinationfolder: str, sourcefolder: str, **kwargs) -> None:
        """Glob copy plugin

        Args:
            glob_patterns (t.List[str] | str): List of glob pattern strings or a single glob pattern string
            destinationfolder (str): The destination folder to copy
            sourcefolder (str): The source folder to copy from
        """
        super(Plugin, self).__init__(**kwargs)
        self.glob_patterns = glob_patterns
        if isinstance(glob_patterns, str):
            self.glob_patterns = [glob_patterns]
        self.destinationfolder = destinationfolder
        self.sourcefolder = sourcefolder

    def get_sourcefolder_path(self):
        return self.app.get_source_path(self.sourcefolder)

    def get_destinationfolder_path(self):
        return self.app.get_destination_path(self.destinationfolder)
    
    def run(self) -> None:
        self.get_logger().debug(f"Glob patterns: {','.join(self.glob_patterns)}")
        if not os.path.exists(self.get_destinationfolder_path()):
            self.get_logger().debug('Destination folder does not exists, creating it!')
            os.makedirs(self.get_destinationfolder_path())
        
        files_of_patterns = [
            (glob.glob(os.path.join(self.get_sourcefolder_path(), pattern), recursive=True), pattern)
            for pattern in self.glob_patterns
        ]
        for files, pattern in files_of_patterns:
            if not files:
                self.get_logger().warning(f"No files found for pattern: {pattern}")
                continue
            self.get_logger().debug(f"Pattern: {pattern}, Files: {','.join(files)}")
            for file in files:
                relative_path = os.path.relpath(file, self.get_sourcefolder_path())
                destination_path = os.path.join(self.get_destinationfolder_path(), relative_path)
                os.makedirs(os.path.dirname(destination_path), exist_ok=True)
                shutil.copy2(file, destination_path)
                self.get_logger().info(f"Matching {pattern}, Copying {file} to {destination_path}")

    def __str__(self) -> str:
        return '{}({})'.format(super(Plugin, self).__str__(), self.sourcefolder)
