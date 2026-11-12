"""Swap product photos for their transparent cutouts (brands/dmp_cutouts.json: original asset path -> cutout path).
Deep-replaces any string that equals a mapped path, anywhere in the built content."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
MAP = json.load(open(os.path.join(HERE, "dmp_cutouts.json")))


def _walk(o):
    if isinstance(o, str):
        return MAP.get(o, o)
    if isinstance(o, list):
        return [_walk(x) for x in o]
    if isinstance(o, dict):
        return {k: (v if str(k).lower().startswith(('og', 'twitter', 'image_og')) else _walk(v)) for k, v in o.items()}
    return o


def apply(data):
    # keep Open Graph images as the originals (social crawlers prefer opaque JPG/PNG); everything else gets the cutout
    return _walk(data)
