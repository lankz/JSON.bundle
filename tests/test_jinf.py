import unittest
import os
import sys
import tempfile
import types
import importlib
import builtins
import json

class DummyStorage:
    def load(self, path):
        with open(path, 'r') as fh:
            return fh.read()

class DummyCore:
    def __init__(self):
        self.storage = DummyStorage()

def load_jinf():
    builtins.unicode = str
    import urllib.parse
    urlparse_module = types.ModuleType('urlparse')
    urlparse_module.urlparse = urllib.parse.urlparse
    sys.modules['urlparse'] = urlparse_module
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'Contents', 'Code'))
    return importlib.import_module('jinf')

class LoadFileTest(unittest.TestCase):
    def setUp(self):
        self.jinf = load_jinf()
        self.jinf.Core = DummyCore()

    def tearDown(self):
        sys.modules.pop('urlparse', None)
        code_path = os.path.join(os.path.dirname(__file__), '..', 'Contents', 'Code')
        if code_path in sys.path:
            sys.path.remove(code_path)

    def test_invalid_json(self):
        with tempfile.NamedTemporaryFile('w', delete=False) as tmp:
            tmp.write('{ invalid ')
            tmp_path = tmp.name
        try:
            with self.assertRaises(Exception) as ctx:
                self.jinf.Jinf.load_file(tmp_path)
            self.assertIn('Invalid JSON', str(ctx.exception))
        finally:
            os.unlink(tmp_path)

    def test_producers(self):
        info = {
            "title": "Test",
            "year": 2000,
            "producers": [
                {"name": "Prod A"},
                {"name": "Prod B"}
            ]
        }
        with tempfile.NamedTemporaryFile('w', delete=False) as tmp:
            tmp.write(json.dumps(info))
            tmp_path = tmp.name
        try:
            j = self.jinf.Jinf.load_file(tmp_path)
            self.assertEqual(j.producers(), [
                {"name": "Prod A"},
                {"name": "Prod B"}
            ])
        finally:
            os.unlink(tmp_path)

if __name__ == '__main__':
    unittest.main()
