"""
Extrakce navržených opatření z rizikové analýzy vodovodu (.docx).

Riziková analýza (RA) má ustálenou strukturu. V kapitole "NAVRŽENÁ OPATŘENÍ"
jsou tabulky "PROVOZNÍ OPATŘENÍ" a "INVESTIČNÍ OPATŘENÍ". Z nich se tahají
jednotlivá opatření (úkoly) do evidenčního Excelu.

Použití jako knihovna:
    from ra_extract import extract
    for m in extract("RA.docx"):
        print(m["num"], m["measure"])
"""
import re
import docx
from docx.oxml.table import CT_Tbl
from docx.oxml.text.paragraph import CT_P
from docx.table import Table
from docx.text.paragraph import Paragraph

# Číslo opatření: 1a.2, 6.1a, 7.10b, 1.1. (Třebařov používá tečku na konci)
MEAS = re.compile(r'^\d+[a-z]?\.\d+[a-z]?\.?$')
YEAR = re.compile(r'\b(20\d\d)\b')

# Mapování názvu skupiny objektů na typ objektu (pořadí = priorita hledání)
TYP_MAP = [
    ('och', 'OP'),
    ('vodárensk', 'vodojem'),
    ('vodojem', 'vodojem'),
    ('distribu', 'síť'),
    ('rozvod', 'síť'),
    ('síť', 'síť'),
    ('zdroj', 'zdroj'),
    ('úpravn', 'úpravna'),
    ('čerpac', 'ČS'),
    ('organiz', 'organizace'),
    ('dispe', 'dispečink'),
]


def iter_block_items(parent):
    """Prochází odstavce a tabulky dokumentu v pořadí, v jakém jsou v těle."""
    body = parent.element.body
    for child in body.iterchildren():
        if isinstance(child, CT_P):
            yield ('p', Paragraph(child, parent))
        elif isinstance(child, CT_Tbl):
            yield ('t', Table(child, parent))


def _cell(c):
    return re.sub(r'\s+', ' ', c.text.replace('\xa0', ' ')).strip()


def row_distinct(row):
    """Buňky zleva doprava, bez prázdných, se sloučením sousedních duplicit
    (sloučené buňky python-docx opakuje)."""
    out = []
    for c in row.cells:
        t = _cell(c)
        if not t:
            continue
        if out and out[-1] == t:
            continue
        out.append(t)
    return out


def parse_group(text):
    """'1a Zdroj – Hartinkov-vrt HV-3' -> (typ, název)"""
    t = re.sub(r'\s+', ' ', text).strip()
    low = t.lower()
    typ = ''
    for k, v in TYP_MAP:
        if k in low:
            typ = v
            break
    nazev = ''
    parts = re.split(r'\s[–-]\s', t, maxsplit=1)
    if len(parts) == 2:
        nazev = parts[1].strip()
    return typ, nazev


def clean_nazev(nazev):
    """Zkrátí název objektu na tu podstatnou část."""
    if not nazev:
        return ''
    n = re.split(r'\s[–-]\s', nazev)[0]   # utne druhý pomlčkový popis
    n = re.split(r'\s*\(', n)[0]          # utne závorku
    return n.strip(' .')


def extract(path):
    """Vrátí seznam opatření (dict) z jedné RA .docx.

    Klíče: druh (provozní/investiční), num, event, measure, year, resp,
           group, typ, nazev
    """
    doc = docx.Document(path)
    measures = []
    cur_h1 = cur_h2 = cur_group = ''

    for kind, item in iter_block_items(doc):
        if kind == 'p':
            st = item.style.name if item.style else ''
            txt = item.text.strip()
            if not txt:
                continue
            if st.startswith('Heading 1') or st.startswith('Title'):
                cur_h1 = txt.upper()
                cur_group = ''
                if 'NAVRŽEN' not in cur_h1:
                    cur_h2 = ''
            elif st.startswith('Heading 2'):
                cur_h2 = txt.upper()
            continue

        # tabulka – jen v kapitole NAVRŽENÁ OPATŘENÍ
        if 'NAVRŽEN' not in cur_h1:
            continue
        if 'PROVOZNÍ' in cur_h2:
            druh = 'provozní'
        elif 'INVESTIČNÍ' in cur_h2:
            druh = 'investiční'
        else:
            continue  # monitorovací apod. přeskočit

        tbl = item
        htxt = ' '.join(_cell(c) for c in tbl.rows[0].cells).lower()
        if 'číslo' not in htxt:
            continue

        for row in tbl.rows:
            dist = row_distinct(row)
            if not dist:
                continue
            first = dist[0]
            if first.lower() == 'číslo':
                continue
            # nadpis skupiny objektů (jediná hodnota, není to číslo opatření)
            if len(dist) == 1 and not MEAS.match(first):
                cur_group = first
                continue
            if MEAS.match(first):
                num = first
                rest = dist[1:]
                year = ''
                for v in dist:
                    m = YEAR.search(v)
                    if m:
                        year = m.group(1)
                        break
                longs = [v for v in rest if len(v) > 14 and not YEAR.fullmatch(v)]
                event = longs[0] if len(longs) >= 1 else ''
                measure = longs[1] if len(longs) >= 2 else (longs[0] if longs else '')
                resp = dist[-1]
                if resp in (measure, event, year) or MEAS.match(resp):
                    resp = ''
                typ, nazev = parse_group(cur_group)
                measures.append(dict(
                    druh=druh, num=num, event=event, measure=measure,
                    year=year, resp=resp, group=cur_group,
                    typ=typ, nazev=clean_nazev(nazev),
                ))

    # deduplikace přesných duplicit
    seen, out = set(), []
    for m in measures:
        k = (m['druh'], m['num'], m['measure'], m['year'])
        if k in seen:
            continue
        seen.add(k)
        out.append(m)
    return out


if __name__ == '__main__':
    import sys
    for m in extract(sys.argv[1]):
        print(f"[{m['druh']:10} {m['num']:7} {m['year']:5}] "
              f"{m['typ']}/{m['nazev']} :: {m['measure'][:80]}")
