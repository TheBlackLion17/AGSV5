import re

SERIES_PATTERN = re.compile(r"(?P<series>.+?)[\s\-_]S(?P<season>\d{1,2})E(?P<episode>\d{1,3})", re.IGNORECASE)

def parse_filename(name: str):
    """Try to parse filenames like 'Show.Name.S01E02.720p.HDRip'"""
    m = SERIES_PATTERN.search(name.replace('.', ' '))
    if m:
        return {
            'series': m.group('series').strip().replace(' ', ' '),
            'season': int(m.group('season')),
            'episode': int(m.group('episode'))
        }
    return {}


def split_tags(text: str):
    return [t.strip() for t in requirement.split('[,;|/\\]', text) if t.strip()]
