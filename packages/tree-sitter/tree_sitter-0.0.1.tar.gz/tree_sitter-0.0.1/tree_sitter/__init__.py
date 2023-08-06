from ctypes import cdll, c_void_p
from distutils.ccompiler import new_compiler
from tempfile import TemporaryDirectory
from tree_sitter_binding import Parser
import os.path as path


INCLUDE_PATH = path.join(path.dirname(__file__), "core", "lib", "include")


class Language:
    def build_library(output_path, *repo_paths):
        """
        Build a dynamic library at the given path, based on the parser
        repositories at the given paths.

        Returns `True` if the dynamic library was compiled and `False` if
        the library already existed and was modified more recently than
        any of the source files.
        """
        compiler = new_compiler()
        compiler.add_include_dir(INCLUDE_PATH)

        output_mtime = 0
        if path.exists(output_path):
            output_mtime = path.getmtime(output_path)

        source_paths = []
        source_mtimes = []
        for repo_path in repo_paths:
            src_path = path.join(repo_path, 'src')
            source_paths.append(path.join(src_path, "parser.c"))
            source_mtimes.append(path.getmtime(source_paths[-1]))
            if path.exists(path.join(src_path, "scanner.cc")):
                compiler.add_library('c++')
                source_paths.append(path.join(src_path, "scanner.cc"))
                source_mtimes.append(path.getmtime(source_paths[-1]))
            elif path.exists(path.join(src_path, "scanner.c")):
                source_paths.append(path.join(src_path, "scanner.c"))
                source_mtimes.append(path.getmtime(source_paths[-1]))

        if max(source_mtimes) > output_mtime:
            with TemporaryDirectory(suffix = 'tree_sitter_language') as dir:
                object_paths = []
                for source_path in source_paths:
                    object_paths.append(compiler.compile([source_path], output_dir = dir)[0])
                compiler.link_shared_object(object_paths, output_path)
            return True
        else:
            return False

    def __init__(self, library_path, name):
        """
        Load the language with the given name from the dynamic library
        at the given path.
        """
        self.name = name
        self.lib = cdll.LoadLibrary(library_path)
        language_function = getattr(self.lib, "tree_sitter_%s" % name)
        language_function.restype = c_void_p
        self.language_id = language_function()
