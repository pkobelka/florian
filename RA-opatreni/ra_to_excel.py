#!/usr/bin/env python3
"""
Vyplní evidenční Excel opatřeními vytaženými z rizikových analýz (.docx).

Každou RA zapíše do zvoleného listu (sloupce A–K):
  A Kalkulační jednice | B Typ objektu | C Název objektu | D Rok |
  E Druh opatření | F Číslo opatření | G Navržené opatření | H Zodpovídá |
  I Datum provedení | J Provedl | K Poznámka
Sloupce A a I–K nechává prázdné (doplňuje se ručně při plnění úkolů).

Příklad:
  python ra_to_excel.py \
      --template "Opatření_RA_MT.xlsx" \
      --out "Opatření_RA_MT_vyplneno.xlsx" \
      --add "Posouzeni_Mladejov.docx::Mladějov- Rychnov" \
      --add "Posouzeni_Trebarov.docx::Třebařov- Koruna"

Pokud list v šabloně neexistuje, vytvoří se nový s hlavičkou.
"""
import argparse
import openpyxl
from openpyxl.styles import Alignment, Font
from ra_extract import extract

HEADER = ['Kalkulační jednice', 'Typ objektu', 'Název objektu', 'Rok',
          'Druh opatření', 'Číslo opatření', 'Navržené opatření', 'Zodpovídá',
          'Datum provedení', 'Provedl', 'Poznámka']
WIDTHS = {'A': 14, 'B': 12, 'C': 22, 'D': 7, 'E': 12, 'F': 11,
          'G': 60, 'H': 22, 'I': 12, 'J': 12, 'K': 22}


def fill_sheet(ws, measures):
    # hlavička, pokud list prázdný
    if ws.max_row == 1 and all(c.value is None for c in ws[1]):
        for i, h in enumerate(HEADER, start=1):
            c = ws.cell(row=1, column=i, value=h)
            c.font = Font(bold=True)
    r = 2
    for m in measures:
        vals = ['', m['typ'], m['nazev'], m['year'], m['druh'],
                m['num'], m['measure'], m['resp'], '', '', '']
        for ci, v in enumerate(vals, start=1):
            c = ws.cell(row=r, column=ci, value=(v if v != '' else None))
            c.alignment = Alignment(wrap_text=True, vertical='top')
        r += 1
    for col, w in WIDTHS.items():
        ws.column_dimensions[col].width = w


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--template', help='vstupní .xlsx šablona (nepovinné)')
    ap.add_argument('--out', required=True, help='výstupní .xlsx')
    ap.add_argument('--add', action='append', default=[], metavar='DOCX::LIST',
                    help='RA soubor a název listu, oddělené "::" (lze víckrát)')
    args = ap.parse_args()

    wb = openpyxl.load_workbook(args.template) if args.template else openpyxl.Workbook()
    if not args.template:
        wb.remove(wb.active)

    print(f"{'List':30} {'celkem':>7} {'prov':>5} {'inv':>5}")
    for spec in args.add:
        if '::' not in spec:
            raise SystemExit(f"Chybný --add (chybí '::'): {spec}")
        docx_path, sheet = spec.split('::', 1)
        ms = extract(docx_path)
        ws = wb[sheet] if sheet in wb.sheetnames else wb.create_sheet(sheet)
        fill_sheet(ws, ms)
        pr = sum(1 for m in ms if m['druh'] == 'provozní')
        inv = sum(1 for m in ms if m['druh'] == 'investiční')
        print(f"{sheet:30} {len(ms):7} {pr:5} {inv:5}")

    wb.save(args.out)
    print(f"\nUloženo: {args.out}")


if __name__ == '__main__':
    main()
