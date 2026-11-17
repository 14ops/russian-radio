"""Loader for the OpenRussian dictionary export.

Data: https://github.com/Badestrand/russian-dictionary (CC BY-SA 4.0), four tab-separated files.
Rows are ordered by word frequency, most common first. Stress is an apostrophe after the vowel.
"""
import csv
import os
import re

ACUTE = '́'
VOWELS = set('аеёиоуыэюя')
NOUN_SLOTS = ['sg_nom', 'sg_gen', 'sg_dat', 'sg_acc', 'sg_inst', 'sg_prep',
              'pl_nom', 'pl_gen', 'pl_dat', 'pl_acc', 'pl_inst', 'pl_prep']
VERB_SLOTS = ['imperative_sg', 'imperative_pl', 'past_m', 'past_f', 'past_n', 'past_pl',
              'presfut_sg1', 'presfut_sg2', 'presfut_sg3', 'presfut_pl1', 'presfut_pl2', 'presfut_pl3']
ADJ_SLOTS = ['comparative', 'short_m', 'short_f', 'short_n', 'short_pl'] + [
    'decl_%s_%s' % (g, c) for g in ('m', 'f', 'n', 'pl') for c in ('nom', 'gen', 'dat', 'acc', 'inst', 'prep')]
SLOTS = {'n': NOUN_SLOTS, 'v': VERB_SLOTS, 'a': ADJ_SLOTS, 'o': []}
FILES = [('n', 'nouns'), ('v', 'verbs'), ('a', 'adjectives'), ('o', 'others')]
WORD = re.compile(r"^[а-яё]+(?:'[а-яё]*)*(?:-[а-яё']+)*$")


def strip_marks(s):
    return s.replace("'", '').replace(ACUTE, '')


def key(s):
    """Lookup key: lower-case, no stress marks, ё folded into е."""
    return strip_marks(s).lower().replace('ё', 'е')


def vowel_count(s):
    return sum(1 for c in strip_marks(s).lower() if c in VOWELS)


def to_acute(s):
    return s.replace("'", ACUTE)


def variants(cell):
    """A form cell can hold several variants: "водо'й,  водо'ю" or "но'вы / новы'"."""
    out = []
    for part in re.split(r'[,/;]', cell or ''):
        w = part.strip().lower().replace(ACUTE, "'")
        if w and WORD.match(w) and w not in out:
            out.append(w)
    return out


def marked(form):
    """True when the stress of this form is known: one vowel, a ё, or an explicit mark."""
    return vowel_count(form) <= 1 or "'" in form or 'ё' in form


class Entry(object):
    __slots__ = ('pos', 'rank', 'bare', 'accented', 'en', 'info', 'forms')

    def __init__(self, pos, rank, bare, accented, en, info, forms):
        self.pos, self.rank, self.bare, self.accented, self.en, self.info, self.forms = pos, rank, bare, accented, en, info, forms


def load(folder):
    """Returns (entries, index). index maps key(form) to a list of (entry, slot name, form with apostrophe stress)."""
    csv.field_size_limit(10 ** 7)
    entries, index = [], {}
    for pos, name in FILES:
        with open(os.path.join(folder, name + '.csv'), encoding='utf-8', newline='') as f:
            rows = csv.reader(f, delimiter='\t', quoting=csv.QUOTE_NONE)
            head = next(rows)
            for rank, row in enumerate(rows):
                if len(row) < 3:
                    continue
                rec = dict(zip(head, row))
                lemma = variants(rec.get('accented', ''))
                if not lemma:
                    continue
                info = ''
                if pos == 'n':
                    info = (rec.get('gender') or '') + ('a' if rec.get('animate') == '1' else '')
                elif pos == 'v':
                    info = {'imperfective': 'i', 'perfective': 'p'}.get(rec.get('aspect') or '', '')
                forms = {}
                for slot in SLOTS[pos]:
                    v = variants(rec.get(slot, ''))
                    if v:
                        forms[slot] = v
                e = Entry(pos, rank, rec['bare'].strip().lower(), lemma[0], (rec.get('translations_en') or '').strip(), info, forms)
                entries.append(e)
                seen = set()
                for slot, form in [('lemma', lemma[0])] + [(s, f) for s, fs in forms.items() for f in fs]:
                    if (slot, form) in seen:
                        continue
                    seen.add((slot, form))
                    index.setdefault(key(form), []).append((e, slot, form))
    return entries, index


def stress_options(index, word):
    """All known stress patterns for a word, as apostrophe-marked lower-case forms. Exact ё spelling wins."""
    w = strip_marks(word).lower()
    hits = [f for (_, _, f) in index.get(key(w), []) if marked(f)]
    exact = [f for f in hits if strip_marks(f) == w]
    pool = exact or hits
    out = []
    for f in pool:
        if f not in out:
            out.append(f)
    return out
