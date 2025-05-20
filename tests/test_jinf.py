import unittest
import os
import sys
import tempfile
import types
import importlib
import builtins
import json
from datetime import datetime, date

class DummyStorage:
    def load(self, path):
        with open(path, 'r') as fh:
            return fh.read()

class DummyCore:
    def __init__(self):
        self.storage = DummyStorage()

class DummyDatetime:
    @staticmethod
    def ParseDate(value):
        return datetime.strptime(value, "%Y-%m-%d")

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
        self.jinf.Datetime = DummyDatetime

    def tearDown(self):
        sys.modules.pop('urlparse', None)
        code_path = os.path.join(os.path.dirname(__file__), '..', 'Contents', 'Code')
        if code_path in sys.path:
            sys.path.remove(code_path)
        if hasattr(self.jinf, 'Datetime'):
            delattr(self.jinf, 'Datetime')

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

    def test_writers(self):
        data = {
            "title": "Test",
            "year": 2020,
            "writers": [
                {"name": "Writer One"},
                {"name": "Writer Two"}
            ]
        }
        with tempfile.NamedTemporaryFile('w', delete=False) as tmp:
            tmp.write(json.dumps(data))
            tmp_path = tmp.name
        try:
            info = self.jinf.Jinf.load_file(tmp_path)
            self.assertEqual(info.writers(), [
                {"name": "Writer One"},
                {"name": "Writer Two"}
            ])
        finally:
            os.unlink(tmp_path)

    def test_producers(self):
        data = {
            "title": "Test",
            "year": 2020,
            "producers": [
                {"name": "Producer One"},
                {"name": "Producer Two"}
            ]
        }
        with tempfile.NamedTemporaryFile('w', delete=False) as tmp:
            tmp.write(json.dumps(data))
            tmp_path = tmp.name
        try:
            info = self.jinf.Jinf.load_file(tmp_path)
            self.assertEqual(info.producers(), [
                {"name": "Producer One"},
                {"name": "Producer Two"}
            ])
        finally:
            os.unlink(tmp_path)

    def test_all_fields(self):
        fixture_path = os.path.join(
            os.path.dirname(__file__), "fixtures", "all_fields.json"
        )
        info = self.jinf.Jinf.load_file(fixture_path)
        self.assertEqual(info.title(), "Test Movie")
        self.assertEqual(info.original_title(), "Original Title")
        self.assertEqual(info.tagline(), "Just a test")
        self.assertEqual(info.summary(), "This is a test.")
        self.assertEqual(info.year(), 2021)
        self.assertEqual(info.release_date(), date(2021, 5, 4))
        self.assertEqual(info.rating(), 8.2)
        self.assertEqual(info.content_rating(), "PG")
        self.assertEqual(info.studio(), "Test Studio")
        self.assertEqual(info.duration(), 123)
        self.assertEqual(info.directors(), [
            {"name": "Director One"},
            {"name": "Director Two"}
        ])
        self.assertEqual(info.writers(), [
            {"name": "Writer One"}
        ])
        self.assertEqual(info.producers(), [
            {"name": "Producer One"}
        ])
        self.assertEqual(info.actors(), [
            {
                "name": "Actor One",
                "role": "Hero",
                "thumb": "http://example.com/one.jpg"
            },
            {"name": "Actor Two"}
        ])
        self.assertEqual(list(info.genres()), ["Drama", "Action"])
        self.assertEqual(list(info.collections()), ["Collection1"])
        self.assertEqual(list(info.countries()), ["USA", "Japan"])

    def test_summary_from_description(self):
        data = {
            "title": "Test",
            "year": 2020,
            "description": "Desc"
        }
        with tempfile.NamedTemporaryFile('w', delete=False) as tmp:
            tmp.write(json.dumps(data))
            tmp_path = tmp.name
        try:
            info = self.jinf.Jinf.load_file(tmp_path)
            self.assertEqual(info.summary(), "Desc")
        finally:
            os.unlink(tmp_path)

    def test_year_from_release_date(self):
        data = {
            "title": "Test",
            "release_date": "2022-01-02"
        }
        with tempfile.NamedTemporaryFile('w', delete=False) as tmp:
            tmp.write(json.dumps(data))
            tmp_path = tmp.name
        try:
            info = self.jinf.Jinf.load_file(tmp_path)
            self.assertEqual(info.year(), 2022)
            self.assertEqual(info.release_date(), date(2022, 1, 2))
        finally:
            os.unlink(tmp_path)

if __name__ == '__main__':
    unittest.main()
