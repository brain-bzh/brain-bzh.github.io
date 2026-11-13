#!/usr/bin/env python3
"""Download BRAIN-affiliated HAL records and HAL's BibTeX export."""
import hashlib
import json
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUERY = 'structId_i:(1149551 OR 1251172)'
API = 'https://api.hal.science/search/'
PAGE_SIZE = 100

def request(**params):
    query = {'q': QUERY, 'sort': 'halId_s asc', **params}
    req = urllib.request.Request(API + '?' + urllib.parse.urlencode(query), headers={'User-Agent': 'brain-bzh-site/1.0 (HAL bibliography)'})
    with urllib.request.urlopen(req, timeout=60) as response:
        return response.read().decode('utf-8')

def load_venues():
    config = json.loads((ROOT / 'data' / 'featured-venues.json').read_text(encoding='utf-8'))
    exclusion = re.compile(config['conference_exclude'], re.IGNORECASE)
    venues = [(item['abbr'], item['type'], re.compile(item['pattern'], re.IGNORECASE)) for item in config['venues']]
    return exclusion, venues


def featured_venue(doc, rules):
    exclusion, venues = rules
    doc_type = doc.get('docType_s')
    field = 'conferenceTitle_s' if doc_type == 'COMM' else 'journalTitle_s' if doc_type == 'ART' else None
    if not field:
        return None
    name = doc.get(field, '').strip()
    if doc_type == 'COMM' and exclusion.search(name):
        return None
    return next((abbr for abbr, kind, pattern in venues if kind == doc_type and pattern.search(name)), None)


def venue_badge(doc, rules):
    """Return a compact label and stable color for a HAL conference or journal."""
    kind = doc.get('docType_s')
    field = {'COMM': 'conferenceTitle_s', 'ART': 'journalTitle_s'}.get(kind)
    if not field:
        return None
    name = ' '.join(doc.get(field, '').split())
    if not name:
        return None
    featured = featured_venue(doc, rules)
    # Normalize known HAL variants without promoting the venue to a highlight.
    is_eusipco = (kind == 'COMM' and not rules[0].search(name)
                   and re.search(r'\beusipco\b|\beuropean signal processing conference\b', name, re.I))
    label = featured or ('EUSIPCO' if is_eusipco else name)
    if not featured and not is_eusipco and kind == 'COMM' and ':' in label:
        prefix = label.split(':', 1)[0].strip()
        if 2 <= len(prefix) <= 34:
            label = prefix
    # Braces and backslashes have special meanings in BibTeX.
    label = re.sub(r'[{}\\]', '', label)
    label = label if len(label) <= 34 else label[:31].rstrip() + '…'
    # Normalize year variants so recurring venues tend to keep their color.
    key = re.sub(r'\b(?:19|20)\d{2}\b', '', label.casefold()).strip()
    palette = ['#dcecfb', '#dbeee6', '#f9e8cd', '#f0e2f6', '#f7e0e3', '#d8eef0', '#e6ead2', '#ece5df']
    color = palette[int(hashlib.sha256(key.encode('utf-8')).hexdigest()[:8], 16) % len(palette)]
    return label, color


def arxiv_id(doc, overrides):
    """Prefer HAL's arXiv identifier; allow verified manual additions."""
    value = doc.get('arxivId_s') or overrides.get(doc['halId_s'], '')
    if value and not re.fullmatch(r'(?:\d{4}\.\d{4,5}|[a-z-]+(?:\.[A-Za-z]{2})?/\d{7})(?:v\d+)?', value):
        raise ValueError('Invalid arXiv ID; existing output preserved')
    return value


def annotate_bibtex(bib, docs, rules, overrides=None):
    """Add al-folio fields by HAL ID, not by relying on export ordering."""
    overrides = overrides or {}
    by_id = {doc['halId_s']: doc for doc in docs}
    entries = re.split(r'(?=^@\w+\s*\{)', bib.strip(), flags=re.M)
    annotated, found = [], set()
    for entry in filter(str.strip, entries):
        match = re.search(r'^\s*HAL_ID\s*=\s*\{([^}]+)\}', entry, re.M | re.I)
        if not match or match.group(1) not in by_id or match.group(1) in found:
            raise ValueError('HAL JSON and BibTeX IDs do not agree; existing output preserved')
        hal_id = match.group(1)
        found.add(hal_id)
        entry = re.sub(r'^(  URL = \{(https?://[^}]+)\},)$', r'\1\n  HTML = {\2},', entry, flags=re.M)
        doc_type = by_id[hal_id].get('docType_s', '')
        if not re.fullmatch(r'[A-Z_]*', doc_type):
            raise ValueError('Unexpected HAL document type; existing output preserved')
        venue = featured_venue(by_id[hal_id], rules)
        badge = venue_badge(by_id[hal_id], rules)
        fields = f'\n  HALTYPE = {{{doc_type}}},'
        identifier = arxiv_id(by_id[hal_id], overrides)
        if identifier:
            fields += f'\n  ARXIV = {{{identifier}}},'
        if badge:
            label, color = badge
            fields += f'\n  ABBR = {{{label}}},\n  VENUECOLOR = {{{color}}},'
        if venue:
            fields += '\n  FEATURED = {true},'
        entry = re.sub(r'\s*}\s*$', lambda _: fields + '\n}', entry)
        annotated.append(entry.strip())
    if found != set(by_id):
        raise ValueError('HAL JSON and BibTeX IDs do not agree; existing output preserved')
    return '\n\n'.join(annotated)


def main():
    first = json.loads(request(wt='json', rows=0))['response']
    total = first['numFound']
    if not total or total > 10000:
        raise ValueError(f'Unexpected HAL result count: {total}; existing output preserved')
    docs, chunks = [], []
    rules = load_venues()
    overrides = json.loads((ROOT / 'data' / 'arxiv-overrides.json').read_text(encoding='utf-8'))
    for start in range(0, total, PAGE_SIZE):
        count = min(PAGE_SIZE, total - start)
        result = json.loads(request(wt='json', rows=count, start=start, fl='halId_s,title_s,authFullName_s,producedDateY_i,docType_s,uri_s,conferenceTitle_s,journalTitle_s,doiId_s,arxivId_s'))['response']
        if result['numFound'] != total or len(result['docs']) != count:
            raise ValueError('HAL result count changed or page incomplete; existing output preserved')
        bib = request(wt='bibtex', rows=count, start=start)
        if len(re.findall(r'^@\w+\s*\{', bib, re.M)) != count:
            raise ValueError('HAL BibTeX page incomplete; existing output preserved')
        docs.extend(result['docs'])
        chunks.append(annotate_bibtex(bib, result['docs'], rules, overrides))
    ids = [d.get('halId_s') for d in docs]
    if None in ids or len(set(ids)) != total:
        raise ValueError('Duplicate or missing HAL IDs; existing output preserved')
    output = ROOT / 'data'
    output.mkdir(exist_ok=True)
    (output / 'hal-publications.json').write_text(json.dumps(docs, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    (ROOT / '_bibliography').mkdir(exist_ok=True)
    (ROOT / '_bibliography' / 'papers.bib').write_text('\n\n'.join(chunks) + '\n', encoding='utf-8')
    print(f'Downloaded {total} BRAIN-affiliated HAL records; featured {sum(bool(featured_venue(doc, rules)) for doc in docs)} matching venues.')

if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        sys.exit(f'HAL update failed: {exc}')
