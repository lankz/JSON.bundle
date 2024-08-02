import os, json

class JSONAgent(Agent.Movies):
    name = 'JSON Metadata'

    primary_provider = False

    languages = [Locale.Language.NoLanguage]

    persist_stored_files = False

    accepts_from = [
        'com.plexapp.agents.localmedia'
    ]

    contributes_to = [
        'com.plexapp.agents.none'
    ]

    def search(self, results, media, lang):
        part = media.items[0].parts[0]
        path = os.path.join(os.path.dirname(part.file), 'Info.json')

        if os.path.exists(path):
            results.Append(MetadataSearchResult(id = 'null', score = 100))

    def update(self, metadata, media, lang):
        part = media.items[0].parts[0]
        path = os.path.join(os.path.dirname(part.file), 'Info.json')

        info = json.loads(Core.storage.load(path))

        try: metadata.title = info['title']
        except: pass

        try: metadata.summary = info['summary']
        except: pass

        try: metadata.year = info['year']
        except: pass

        try: metadata.rating = info['rating']
        except: pass

        try: metadata.content_rating = info['content_rating']
        except: pass

        try: metadata.studio = info['studio']
        except: pass

        try: metadata.duration = info['duration']
        except: pass

        metadata.directors.clear()

        try:
            for r in info['directors']:
                director = metadata.directors.new()

                try: director.name = r['name']
                except: pass

        except:
            pass

        metadata.genres.clear()

        try:
            for g in info['genres']:
                metadata.genres.add(g)
        except:
            pass

        metadata.roles.clear()

        try:
            for r in info['roles']:
                role = metadata.roles.new()

                try: role.actor = r['actor']
                except: pass

                try: role.role = r['role']
                except: pass
        except:
            pass

        metadata.collections.clear()

        try:
            for c in info['collections']:
                metadata.collections.add(c)
        except:
            pass


        metadata.countries.clear()

        try:
            for d in info['countries']:
                metadata.countries.add(d)
        except:
            pass

        try: metadata.original_title = info['original_title']
        except: pass
