"""Extrakce opatření z PDF příloh (Poličsko, Jedlová Tab.6/7).

Tabulky mají sloupce: číslo | Nebezpečná událost | Nápravná (provozní/investiční)
opatření | Míra rizika | Časové plnění | priorita | Splněno | Kontrola | poznámka
Text v buňkách se zalamuje, proto se rekonstruuje ze souřadnic slov.
"""
import re
import pdfplumber

MEAS = re.compile(r'^\d+[a-z]?\.\d+[a-z]?\.?$')
YEAR = re.compile(r'\b(20\d\d)\b')

TYP_MAP = [('pásm', 'OP'), ('och', 'OP'), ('vodojem', 'vodojem'), ('vdj', 'vodojem'),
           ('rozvod', 'síť'), ('distribu', 'síť'), ('síť', 'síť'), ('vrt', 'zdroj'),
           ('zdroj', 'zdroj'), ('pramen', 'zdroj'), ('studna', 'zdroj'),
           ('čerpac', 'ČS'), (' čs', 'ČS'), ('úpravn', 'úpravna'),
           ('organiz', 'organizace'), ('dispe', 'dispečink')]


def _cluster(vals, tol=6):
    vals = sorted(vals)
    out = []
    for v in vals:
        if out and v - out[-1] < tol:
            continue
        out.append(v)
    return out


def _col_bounds(page):
    xs = _cluster([e['x0'] for e in page.vertical_edges])
    return xs


def _typ_nazev(group):
    t = re.sub(r'\s+', ' ', group).strip()
    low = t.lower()
    typ = ''
    for k, v in TYP_MAP:
        if k in low:
            typ = v
            break
    # název = text po úvodním "1." / "1)" apod.
    nazev = re.sub(r'^\d+[a-z]?[\.\)]\s*', '', t)
    nazev = re.split(r'\s[–-]\s', nazev)[0]
    nazev = re.split(r'\s*\(', nazev)[0].strip(' .')
    return typ, nazev


def extract_pdf(path, druh):
    measures = []
    cur_group = ''
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            xb = _col_bounds(page)
            if len(xb) < 6:
                continue
            # hranice sloupců (potřebujeme 1=číslo,2=událost,3=opatření,5=čas.plnění)
            c = xb  # x-hranice zleva
            def col_range(i):
                return (c[i], c[i + 1]) if i + 1 < len(c) else (c[i], page.width)
            r_num = col_range(0)
            r_evt = col_range(1)
            r_meas = col_range(2)
            r_time = col_range(4)
            # řádkové pásy z vodorovných čar
            ys = _cluster([e['top'] for e in page.horizontal_edges], tol=3)
            words = page.extract_words()
            for a, b in zip(ys, ys[1:]):
                band = [w for w in words if a - 1 <= (w['top'] + w['bottom']) / 2 <= b + 1]
                if not band:
                    continue

                def cell(rng):
                    ws = [w for w in band if rng[0] <= (w['x0'] + w['x1']) / 2 < rng[1]]
                    ws.sort(key=lambda w: (round(w['top'] / 3), w['x0']))
                    return re.sub(r'\s+', ' ', ' '.join(w['text'] for w in ws)).strip()

                num = cell(r_num)
                if not num or num.lower().startswith('číslo'):
                    continue
                # nadpis skupiny? číslo buňka obsahuje název (ne jen X.Y.)
                if not MEAS.match(num):
                    # bere se jako skupina jen pokud vypadá jako "1. něco"
                    if re.match(r'^\d+[a-z]?[\.\)]\s+\S', num) or (r_evt and not cell(r_evt)):
                        cur_group = num
                    continue
                measure = cell(r_meas)
                event = cell(r_evt)
                timev = cell(r_time)
                ym = YEAR.search(timev)
                year = ym.group(1) if ym else ''
                if not measure and not event:
                    continue
                typ, nazev = _typ_nazev(cur_group)
                measures.append(dict(druh=druh, num=num, event=event, measure=measure,
                                     year=year, resp='', group=cur_group,
                                     typ=typ, nazev=nazev, time_raw=timev))
    # dedup
    seen, out = set(), []
    for m in measures:
        k = (m['num'], m['measure'], m['year'])
        if k in seen:
            continue
        seen.add(k)
        out.append(m)
    return out


if __name__ == '__main__':
    import sys
    ms = extract_pdf(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else 'provozní')
    print(f"Celkem: {len(ms)}")
    for m in ms[:30]:
        print(f"[{m['num']:7} {m['typ']:8}|{m['nazev'][:16]:16} rok={m['year']:5} čas='{m['time_raw'][:10]:10}'] {m['measure'][:75]}")
