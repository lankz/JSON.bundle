import unittest
import os
import sys
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


class JinfTestCase(unittest.TestCase):
    def setUp(self):
        self.jinf = load_jinf()
        self.jinf.Core = DummyCore()
        self.jinf.Datetime = DummyDatetime
        self.fixture_path = os.path.join(
            os.path.dirname(__file__), 'fixtures', 'all_fields.json'
        )

    def tearDown(self):
        sys.modules.pop('urlparse', None)
        code_path = os.path.join(os.path.dirname(__file__), '..', 'Contents', 'Code')
        if code_path in sys.path:
            sys.path.remove(code_path)
        if hasattr(self.jinf, 'Datetime'):
            delattr(self.jinf, 'Datetime')

    # helper to load fixture fresh for each test
    def load_fixture(self):
        return self.jinf.Jinf.load_file(self.fixture_path)

    def test_invalid_json(self):
        original_load = self.jinf.Core.storage.load
        self.jinf.Core.storage.load = lambda _: '{ invalid '
        try:
            with self.assertRaises(Exception) as ctx:
                self.jinf.Jinf.load_file(self.fixture_path)
            self.assertIn('Invalid JSON', str(ctx.exception))
        finally:
            self.jinf.Core.storage.load = original_load

    def test_title(self):
        info = self.load_fixture()
        self.assertEqual(info.title(), 'Test Movie')

    def test_original_title(self):
        info = self.load_fixture()
        self.assertEqual(info.original_title(), 'Original Title')

    def test_tagline(self):
        info = self.load_fixture()
        self.assertEqual(info.tagline(), 'Just a test')

    def test_summary(self):
        info = self.load_fixture()
        self.assertEqual(info.summary(), 'This is a test.')

    def test_year(self):
        info = self.load_fixture()
        self.assertEqual(info.year(), 2021)

    def test_release_date(self):
        info = self.load_fixture()
        self.assertEqual(info.release_date(), date(2021, 5, 4))

    def test_rating(self):
        info = self.load_fixture()
        self.assertEqual(info.rating(), 8.2)

    def test_content_rating(self):
        info = self.load_fixture()
        self.assertEqual(info.content_rating(), 'PG')

    def test_studio(self):
        info = self.load_fixture()
        self.assertEqual(info.studio(), 'Test Studio')

    def test_duration(self):
        info = self.load_fixture()
        self.assertEqual(info.duration(), 123)

    def test_directors(self):
        info = self.load_fixture()
        self.assertEqual(info.directors(), [
            {'name': 'Director One'},
            {'name': 'Director Two'}
        ])

    def test_writers(self):
        info = self.load_fixture()
        self.assertEqual(info.writers(), [
            {'name': 'Writer One'}
        ])

    def test_producers(self):
        info = self.load_fixture()
        self.assertEqual(info.producers(), [
            {'name': 'Producer One'}
        ])

    def test_actors(self):
        info = self.load_fixture()
        self.assertEqual(info.actors(), [
            {
                'name': 'Actor One',
                'role': 'Hero',
                'thumb': 'http://example.com/one.jpg'
            },
            {'name': 'Actor Two'}
        ])

    def test_genres(self):
        info = self.load_fixture()
        self.assertEqual(list(info.genres()), ['Drama', 'Action'])

    def test_collections(self):
        info = self.load_fixture()
        self.assertEqual(list(info.collections()), ['Collection1'])

    def test_countries(self):
        info = self.load_fixture()
        self.assertEqual(list(info.countries()), ['USA', 'Japan'])

    def test_summary_from_description(self):
        data = {
            'title': 'Test',
            'year': 2020,
            'description': 'Desc'
        }
        info = self.jinf.Jinf(data)
        self.assertEqual(info.summary(), 'Desc')

    def test_year_from_release_date(self):
        data = {
            'title': 'Test',
            'release_date': '2022-01-02'
        }
        info = self.jinf.Jinf(data)
        self.assertEqual(info.year(), 2022)
        self.assertEqual(info.release_date(), date(2022, 1, 2))


if __name__ == '__main__':
    unittest.main()
