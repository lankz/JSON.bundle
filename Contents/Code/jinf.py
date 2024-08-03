import os, json, re

class Jinf:
    def __init__(self, data):
        self.data = data

        # must have at least these two values to be considered valid info
        if not self.title():
            raise Exception('Missing title')

        if not self.year():
            raise Exception('Missing year')

    @classmethod
    def load_file(cls, path):
        if not os.path.exists(path):
            raise Exception('No file exists at path: %s' % path)

        try:
            data = json.loads(Core.storage.load(path))
        except json.decoder.JSONDecodeError as json_error:
            raise Exception('Invalid JSON: %s' % json_error)

        if not isinstance(data, dict):
            raise Exception('Invalid JSON: must be a dictionary')

        return cls(data)

    def title(self):
        return self.get_str('title')

    def original_title(self):
        return self.get_str('original_title')

    def summary(self):
        return self.get_str('summary') or self.get_str('description')

    def release_date(self):
        return self.get_date('release_date')

    def year(self):
        year = self.get_int('year')

        if year and year > 1900 and year < 2100:
            return year

        # if there's no explicit year key, we try extracting it
        # from the release date
        if self.release_date():
            return self.release_date().year

    def rating(self):
        return self.get_float('rating') or self.get_decimal('rating')

    def content_rating(self):
        return self.get_str('content_rating')

    def studio(self):
        return self.get_str('studio')

    def duration(self):
        return self.get_int('duration')

    def genres(self):
        return filter(None, [
            str(value).strip()
            for value in self.get_array('genres')
            if isinstance(value, (str, unicode))
        ])

    def collections(self):
        return filter(None, [
            str(value).strip()
            for value in self.get_array('collections')
            if isinstance(value, (str, unicode))
        ])

    def countries(self):
        return filter(None, [
            str(value).strip()
            for value in self.get_array('countries')
            if isinstance(value, (str, unicode))
        ])

    def get_str(self, key):
        value = self.data.get(key)

        if value and isinstance(value, (str, unicode)):
            value = str(value).strip()

            if value:
                return value

    def get_int(self, key):
        value = self.data.get(key)

        if value and isinstance(value, int):
            return value

    def get_float(self, key):
        value = self.data.get(key)

        if value:
          if isinstance(value, float):
            return value

          if isinstance(value, int):
            return float(value)

          if isinstance(value, (str, unicode)):
            value = str(value)

            # support floats represented as strings in the json to avoid any
            # weirdness with floating point precision
            if re.match(r'^\d+(\.\d+)?$', value):
              return float(value)

    def get_date(self, key):
        try:
            value = self.data.get(key)

            if value:
                return Datetime.ParseDate(value).date()
        except:
            pass

    def get_array(self, key):
        value = self.data.get(key)

        if isinstance(value, list):
            return value

        return []
