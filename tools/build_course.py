"""Builds data/course.js from tools/course/*.txt.

Usage:  python3 tools/build_course.py <folder with the OpenRussian CSV files>
        (get them with: git clone https://github.com/Badestrand/russian-dictionary)

Every Russian word of two or more syllables gets its stress mark from the OpenRussian data.
A word with more than one possible stress, or one the data does not know, must carry its stress
in the source text: an apostrophe after the stressed vowel, for example  до'ма  or  Ма'ша.
Names and other words missing from the data can also go into tools/course/extra.txt.

Source format, one block per unit:
  == 1 | A1 | Привет! | Greetings and names      number | level | Russian title | English topic
  recap: one English sentence                     what happens, for the writer AI and the unit list
  grammar: one English sentence                   optional, shown in the unit list
  N: Привет! | Hi!                                host N or T, Russian | English
  T*: Привет! | Hi!                               * marks a line the listener repeats
  N> An English tip.                              > marks an English-only line
  words: привет = hi; пока = bye                  new words
  quiz: Question? | right answer | wrong | wrong  the first option is the right one
"""
import glob
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import openrussian as oru  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, 'course')
OUT = os.path.join(HERE, '..', 'data', 'course.js')
TOKEN = re.compile(r"[А-Яа-яЁё]+(?:'[А-Яа-яЁё]*)*")
problems, notes = [], []


def load_extra():
    """extra.txt: words with apostrophe stress. A capitalised word only matches a capitalised token."""
    table = {}
    path = os.path.join(SRC, 'extra.txt')
    if os.path.exists(path):
        for line in open(path, encoding='utf-8'):
            for w in line.split('#')[0].split():
                table[oru.strip_marks(w)] = w
    return table


def place(token, pattern):
    """Copies the stress positions of pattern (lower-case, apostrophes) onto token (any case)."""
    out, i = [], 0
    for ch in pattern:
        if ch == "'":
            out.append(oru.ACUTE)
        else:
            out.append(token[i])
            i += 1
    return ''.join(out)


def stress(token, index, extra, where):
    if "'" in token:
        plain = token.replace("'", '')
        for m in re.finditer("'", token):
            if m.start() == 0 or token[m.start() - 1].lower() not in oru.VOWELS:
                problems.append('%s: the mark in "%s" does not follow a vowel' % (where, token))
        opts = oru.stress_options(index, plain)
        if opts and token.lower() not in opts and oru.strip_marks(plain) not in extra:
            notes.append('%s: "%s" differs from the data: %s' % (where, token, ', '.join(opts)))
        return token.replace("'", oru.ACUTE)
    if oru.vowel_count(token) <= 1 or 'ё' in token.lower():
        return token
    if token in extra:
        return place(token, extra[token].replace(oru.ACUTE, "'"))
    if token.lower() in extra:  # a lower-case entry also covers the capitalised word
        return place(token, extra[token.lower()].replace(oru.ACUTE, "'"))
    opts = oru.stress_options(index, token)
    if not opts:
        problems.append('%s: no stress known for "%s". Mark it in the text or add it to extra.txt' % (where, token))
        return token
    if len(opts) > 1:
        problems.append('%s: "%s" has several stresses: %s. Mark it in the text' % (where, token, ', '.join(opts)))
        return token
    return place(token, opts[0])


def russian(text, index, extra, where):
    return TOKEN.sub(lambda m: stress(m.group(0), index, extra, where), text.strip())


def parse(path, index, extra):
    units, cur = [], None
    for ln, raw in enumerate(open(path, encoding='utf-8'), 1):
        line = raw.strip()
        where = '%s:%d' % (os.path.basename(path), ln)
        if not line or line.startswith('#'):
            continue
        fix = lambda s: russian(s, index, extra, where)  # noqa: E731
        if line.startswith('=='):
            n, level, title, topic = [p.strip() for p in line[2:].split('|')]
            cur = {'n': int(n), 'level': level, 'title': fix("Уро'к %s. %s" % (n, title)), 'topic': topic,
                   'recap': '', 'grammar': '', 'words': [], 'lines': [], 'quiz': []}
            units.append(cur)
            continue
        if cur is None:
            problems.append('%s: text before the first unit header' % where)
            continue
        m = re.match(r'^(recap|grammar|words|quiz):\s*(.*)$', line)
        if m:
            kind, body = m.group(1), m.group(2)
            if kind in ('recap', 'grammar'):
                cur[kind] = fix(body)
            elif kind == 'words':
                for pair in body.split(';'):
                    if '=' not in pair:
                        problems.append('%s: word without a meaning: "%s"' % (where, pair.strip()))
                        continue
                    ru, en = pair.split('=', 1)
                    cur['words'].append([fix(ru), en.strip()])
            else:
                parts = [fix(p) for p in body.split('|')]
                if len(parts) < 3 or len(set(parts[1:])) != len(parts) - 1:
                    problems.append('%s: a quiz line needs a question and 2 or more different options' % where)
                cur['quiz'].append([parts[0], parts[1:], 0])
            continue
        m = re.match(r'^([NT])(\*?)([:>])\s*(.*)$', line)
        if not m:
            problems.append('%s: cannot read this line: %s' % (where, line[:60]))
            continue
        who, rep, sep, body = m.groups()
        if sep == '>':
            cur['lines'].append([who, '', fix(body), 2])
            continue
        if ' | ' not in body:
            problems.append('%s: a Russian line needs " | " and its English meaning' % where)
            continue
        ru, en = body.split(' | ', 1)
        entry = [who, fix(ru), fix(en)]
        if rep:
            entry.append(1)
            if len(ru) > 90:
                problems.append('%s: a repeat line has to stay under 90 characters' % where)
        cur['lines'].append(entry)
    return units


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    _, index = oru.load(sys.argv[1])
    extra = load_extra()
    units = []
    for path in sorted(glob.glob(os.path.join(SRC, 'units-*.txt'))):
        units += parse(path, index, extra)
    units.sort(key=lambda u: u['n'])
    for i, u in enumerate(units, 1):
        if u['n'] != i and not os.environ.get('PARTIAL'):
            problems.append('unit numbers have a gap or a repeat near unit %d' % u['n'])
            break
        reps = sum(1 for l in u['lines'] if len(l) > 3 and l[3] == 1)
        if len(u["lines"]) < 10 or reps < 2 or len(u['quiz']) != 3 or len(u['words']) < 5 or not u['recap']:
            problems.append('unit %d is incomplete: %d lines, %d repeat lines, %d quiz questions, %d words' % (
                u['n'], len(u['lines']), reps, len(u['quiz']), len(u['words'])))
    for n in notes:
        print('note:', n)
    if problems:
        for p in problems:
            print('PROBLEM:', p)
        sys.exit('%d problems. Nothing written.' % len(problems))
    dump = lambda v: json.dumps(v, ensure_ascii=False, separators=(',', ':'))  # noqa: E731
    out = ['/* Povtori FM course: %d units, A1 to A2. Generated by tools/build_course.py from tools/course/units-*.txt.' % len(units),
           '   Stress marks come from the OpenRussian data (openrussian.org). Edit the .txt sources, then rebuild.',
           '   Line format: [host, Russian, English, flag]. Flag 1 = the listener repeats it, 2 = English-only tip. */',
           'window.POVTORI_COURSE = [']
    for u in units:
        out.append('{n:%d,level:%s,title:%s,topic:%s,' % (u['n'], dump(u['level']), dump(u['title']), dump(u['topic'])))
        out.append(' recap:%s,grammar:%s,' % (dump(u['recap']), dump(u['grammar'])))
        out.append(' words:%s,' % dump(u['words']))
        out.append(' lines:[\n  ' + ',\n  '.join(dump(l) for l in u['lines']) + '],')
        out.append(' quiz:[\n  ' + ',\n  '.join(dump(q) for q in u['quiz']) + ']},')
    out.append('];')
    with open(OUT, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(out) + '\n')
    lines = sum(len(u['lines']) for u in units)
    print('wrote %s: %d units, %d lines, %d words, %d quiz questions' % (
        os.path.relpath(OUT), len(units), lines, sum(len(u['words']) for u in units), sum(len(u['quiz']) for u in units)))


if __name__ == '__main__':
    main()
