import os, json

from jinf import Jinf

def Start():
  pass

class JSONAgent(Agent.Movies):
    name = 'JSON Metadata'

    primary_provider = True

    languages = [
        Locale.Language.NoLanguage
    ]

    accepts_from = [
        'com.plexapp.agents.localmedia'
    ]

    contributes_to = [
        'com.plexapp.agents.none'
    ]

    def load_info(self, media):
        try: part = media.items[0].parts[0]
        except: raise Exception('Unable to find media file')

        return Jinf.load_file(
           os.path.join(os.path.dirname(part.file), 'Info.json'))

    def search(self, results, media, lang):
        try: info = self.load_info(media)
        except: return

        results.Append(MetadataSearchResult(
            id =  media.id,
            name = info.title(),
            year = info.year(),
            lang = lang,
            score = 100
        ))

    def update(self, metadata, media, lang):
        info = self.load_info(media)

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
