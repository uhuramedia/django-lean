import os
import types
import unittest

for filename in os.listdir(os.path.dirname(__file__)):
    if (filename[-3:] == ".py" and
        filename != "__init__.py" and
        filename[0] != '.'):
        module = __import__('.'.join((__name__, filename[:-3])), (), (), ["*"])
        for name in dir(module):
            function = getattr(module, name)
            if (isinstance(function, types.TypeType) and
                issubclass(function, unittest.TestCase)):
                globals()[name] = function
