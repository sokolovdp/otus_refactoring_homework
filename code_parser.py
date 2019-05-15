# -*- coding: utf-8 -*-
import os
import ast
import aiofiles
import chardet
import asyncio
from abc import ABC, abstractmethod

from collections import namedtuple
from nltk import pos_tag
from concurrent.futures import ALL_COMPLETED

ParseResult = namedtuple('ParseResult', ['file', 'verbs'])

PYTHON_FILES = ('.py',)
PYTHON_INTERNAL_NAMES = {
    'sys', 'os', 're', 'kwargs', 'args', 'argparse', 'self',
    'ArithmeticError', 'AssertionError', 'AttributeError', 'BaseException', 'BlockingIOError',
    'BrokenPipeError', 'BufferError', 'BytesWarning', 'ChildProcessError', 'ConnectionAbortedError',
    'ConnectionError', 'ConnectionRefusedError', 'ConnectionResetError', 'DeprecationWarning', 'EOFError',
    'Ellipsis', 'EnvironmentError', 'Exception', 'False', 'FileExistsError', 'FileNotFoundError',
    'FloatingPointError', 'FutureWarning', 'GeneratorExit', 'IOError', 'ImportError', 'ImportWarning',
    'IndentationError', 'IndexError', 'InterruptedError', 'IsADirectoryError', 'KeyError', 'KeyboardInterrupt',
    'LookupError', 'MemoryError', 'ModuleNotFoundError', 'NameError', 'None', 'NotADirectoryError',
    'NotImplemented', 'NotImplementedError', 'OSError', 'OverflowError', 'PendingDeprecationWarning',
    'PermissionError', 'ProcessLookupError', 'RecursionError', 'ReferenceError', 'ResourceWarning', 'RuntimeError',
    'RuntimeWarning', 'StopAsyncIteration', 'StopIteration', 'SyntaxError', 'SyntaxWarning', 'SystemError',
    'SystemExit', 'TabError', 'TimeoutError', 'True', 'TypeError', 'UnboundLocalError', 'UnicodeDecodeError',
    'UnicodeEncodeError', 'UnicodeError', 'UnicodeTranslateError', 'UnicodeWarning', 'UserWarning', 'ValueError',
    'Warning', 'WindowsError', 'ZeroDivisionError', 'abs', 'all', 'any', 'ascii', 'bin', 'bool', 'bytearray',
    'bytes', 'callable', 'chr', 'classmethod', 'compile', 'complex', 'copyright', 'credits', 'delattr', 'dict',
    'dir', 'divmod', 'enumerate', 'eval', 'exec', 'exit', 'filter', 'float', 'format', 'frozenset', 'getattr',
    'globals', 'hasattr', 'hash', 'help', 'hex', 'id', 'input', 'int', 'isinstance', 'issubclass', 'iter', 'len',
    'license', 'list', 'locals', 'map', 'max', 'memoryview', 'min', 'next', 'object', 'oct', 'open', 'ord', 'pow',
    'print', 'property', 'quit', 'range', 'repr', 'reversed', 'round', 'set', 'setattr', 'slice', 'sorted',
    'staticmethod', 'str', 'sum', 'super', 'tuple', 'type', 'vars', 'zip'
}
INTERNAL_PYTHON_FOLDERS = {
    'venv',
    'bin',
    'lib',
    'dist',
    'build',
    '.idea',
    '__pycache__',
    '.git'
}

JAVA_FILES = ('.java',)
JAVA_INTERNAL_NAMES = {}
INTERNAL_JAVA_FOLDERS = {}

MAX_NUMBER_OF_FILES = 200


class BaseCodeParser(ABC):
    @abstractmethod
    def get_words_from_source_code(self, source_code: str) -> list:
        pass


def build_list_of_files(path: str = None, extensions: tuple = None, excludes: set = None) -> list:
    files_in_the_path = []
    for root, sub_dirs, files in os.walk(path):
        sub_dirs[:] = [d for d in sub_dirs if d not in excludes]
        for file_name in files:
            for extension in extensions:
                if file_name.endswith(extension):
                    full_path_file_name = os.path.join(root, file_name)
                    files_in_the_path.append(full_path_file_name)
        if len(files_in_the_path) > MAX_NUMBER_OF_FILES:
            files_in_the_path = files_in_the_path[:MAX_NUMBER_OF_FILES]
            break
    return files_in_the_path


async def read_from_file(file_name: str) -> str:
    try:
        async with aiofiles.open(file_name, 'rb') as file:
            raw_data = await file.read()
        if raw_data:
            encoding = chardet.detect(raw_data)['encoding']
            file_data = raw_data.decode(encoding)
        else:
            file_data = None
    except (IOError, Exception):
        file_data = None
    return file_data


async def process_file(file_name: str, parser=None) -> ParseResult:
    file_content = await read_from_file(file_name)
    if file_content is not None:
        result = ParseResult(file=file_name, verbs=parser.get_words_from_source_code(file_content))
    else:
        result = ParseResult(file=file_name, verbs=[])
    return result


async def process_all_files(file_list: list, parser=None) -> list:
    futures = [process_file(file, parser) for file in file_list]
    done, pending = await asyncio.wait(futures, return_when=ALL_COMPLETED)
    analysis_data = [d.result() for d in done if d.result is not None]
    return analysis_data


def is_verb(word: str) -> bool:
    if not word or len(word) < 2:
        return False
    pos_info = pos_tag([word])
    return pos_info[0][1] == 'VB'


class PythonCodeParser(BaseCodeParser):
    def __init__(self):
        self.code_tree = None
        self.verbs = None

    @staticmethod
    def dunder(name: str) -> bool:
        return name.startswith('__') and name.endswith('__')

    def proper_name(self, name: str) -> bool:
        return name not in PYTHON_INTERNAL_NAMES and len(name) > 1 and not self.dunder(name)

    def get_words_from_source_code(self, source_code: str) -> list:
        self.code_tree = ast.parse(source_code)
        self.verbs = []
        for node in ast.walk(self.code_tree):
            if isinstance(node, ast.FunctionDef):
                new_func_name = node.name.lower()
                if self.proper_name(new_func_name):
                    verbs = [word for word in new_func_name.split('_') if is_verb(word)]
                    self.verbs.extend(verbs)
        return self.verbs


class JavaCodeParser(BaseCodeParser):
    def __init__(self):
        self.code_tree = None
        self.verbs = None

    def get_words_from_source_code(self, source_code: str) -> list:
        return []


def start_parsing(start_folder, file_extensions: tuple = PYTHON_FILES) -> list:
    if file_extensions is PYTHON_FILES:
        code_parser = PythonCodeParser()
        excludes = PYTHON_INTERNAL_NAMES
    elif file_extensions is JAVA_FILES:
        code_parser = JavaCodeParser()
        excludes = JAVA_INTERNAL_NAMES
    else:
        raise NotImplementedError(f"Can't parse files with {file_extensions} extensions")

    files_to_analyse = build_list_of_files(
        path=start_folder,
        extensions=file_extensions,
        excludes=excludes
    )
    result_list = asyncio.run(
        process_all_files(files_to_analyse, parser=code_parser)
    )
    return result_list
