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
        try: info = self.load_info(media)
        except: return

        # we should always have these
        metadata.title = info.title()
        metadata.year = info.year()

        original_title = info.original_title()
        if original_title:
            metadata.original_title = original_title

        tagline = info.tagline()
        if tagline:
            metadata.tagline = tagline

        summary = info.summary()
        if summary:
            metadata.summary = summary

        release_date = info.release_date()
        if release_date:
            metadata.originally_available_at = release_date

        rating = info.rating()
        if rating:
            metadata.rating = rating

        content_rating = info.content_rating()
        if content_rating:
            metadata.content_rating = content_rating

        studio = info.studio()
        if studio:
            metadata.studio = studio

        duration = info.duration()
        if duration:
            metadata.duration = duration

        metadata.directors.clear()
        for d in info.directors():
            director = metadata.directors.new()
            director.name = d.get('name')

        metadata.genres.clear()
        for g in info.genres():
            metadata.genres.add(g)

        metadata.roles.clear()
        for a in info.actors():
            role = metadata.roles.new()
            role.name = a.get('name')

            if a.get('role'):
                role.role = a.get('role')

            if a.get('thumb'):
                role.photo = a.get('thumb')

        metadata.collections.clear()
        for c in info.collections():
            metadata.collections.add(c)

        metadata.countries.clear()
        for c in info.countries():
            metadata.countries.add(c)
