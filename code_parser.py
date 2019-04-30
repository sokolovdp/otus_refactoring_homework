# -*- coding: utf-8 -*-
import ast
from nltk import pos_tag

PYTHON_FILE_EXTENSIONS = ('.py',)
PYTHON_INTERNAL_NAMES = {
    'BeautifulSoup', 'sys', 'os', 're', 'kwargs', 'args', 'argparse', 'self',
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


def is_verb(word: str) -> bool:
    if not word or len(word) < 2:
        return False
    pos_info = pos_tag([word])
    return pos_info[0][1] == 'VB'


class PythonCodeParser:
    def __init__(self):
        self.code_tree = None
        self.verbs = None
        super().__init__()

    @staticmethod
    def dunder(name: str) -> bool:
        return name.startswith('__') and name.endswith('__')

    def proper_name(self, name: str) -> bool:
        return name not in PYTHON_INTERNAL_NAMES and len(name) > 1 and not self.dunder(name)

    def get_verbs_from_functions_names(self, source_code: str) -> list:
        self.code_tree = ast.parse(source_code)
        self.verbs = []
        for node in ast.walk(self.code_tree):
            if isinstance(node, ast.FunctionDef):
                new_func_name = node.name.lower()
                if self.proper_name(new_func_name):
                    verbs = [word for word in new_func_name.split('_') if is_verb(word)]
                    self.verbs.extend(verbs)
        return self.verbs
