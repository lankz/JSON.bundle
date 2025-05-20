# JSON Metadata Agent for Plex

A small Plex metadata agent that imports information from `Info.json` or `Movie.json` files stored next to your movies. It is useful when a traditional web scraper cannot easily gather metadata.

## Features

- Reads metadata directly from JSON files alongside your movie files
- Avoids the need for complex or brittle HTML scraping
- Designed to work with any external tool that generates the JSON
- Currently supports **movies only**

## Installation

1. Clone or download this repository.
2. Copy the `JSON.bundle` directory into your Plex plug-ins folder. On most systems this is located under `Plex Media Server/Plug-ins`.
3. Restart Plex Media Server.
4. When creating or editing a movie library choose **JSON Metadata** as the agent.

## Usage

Place an `Info.json` or `Movie.json` file in the same directory as your movie file. The file name is case-insensitive. A typical layout looks like:

```
Movies
  └─ Akira (1988)
      ├─ akira.1988.720p.bluray.x264.mp4
      ├─ Info.json
      └─ Poster.jpg
```

Only one movie and one info file should exist per folder.

### Example info JSON

The structure of the JSON follows Plex's internal movie model. A minimal example is shown below.

```json
{
    "title": "Akira",
    "tagline": "Neo-Tokyo is about to explode",
    "summary": "Childhood friends Tetsuo and Kaneda are pulled into the...",
    "year": 1988,
    "rating": 7.7,
    "content_rating": "M",
    "studio": "Bandai Visual Company",
    "duration": 124,
    "directors": [
        {
            "name": "Katsuhiro \u014Ctomo"
        }
    ],
    "writers": [
        {
            "name": "Izô Hashimoto"
        }
    ],
    "actors": [
        {
            "name": "Mitsuo Iwata",
            "role": "Sh\u00f4tar\u00f4 Kaneda"
        }
    ],
    "genres": [
        "Animation",
        "Science Fiction"
    ],
    "collections": [
        "Anime"
    ]
}
```

See `movie-schema.json` for a full description of the supported fields.

## Development

Run the unit tests with:

```
python -m unittest tests.test_jinf -v
```

## License

This project is licensed under the terms found in the [LICENSE](LICENSE) file. "Plex" is a trademark of Plex, Inc. This project is not affiliated with or endorsed by Plex, Inc.
