class Jinf:
    def __init__(self, data):
        self.data = data

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
        return str(self.data.get('title')).strip()

    def release_date(self):
        try:
            release_date = self.data.get('release_date')

            if release_date:
                return Datetime.ParseDate(release_date).date()
        except:
            pass

    def year(self):
        try:
            year = int(self.data.get('year'))
            if year > 1900 and year < 2100:
                return year
        except:
            pass

        # if we didn't get a year from info.json, try extracting it
        # from the release date
        if self.release_date():
            return self.release_date().year
