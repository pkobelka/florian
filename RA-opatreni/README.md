# RA-opatření

Nástroj, který z **rizikové analýzy vodovodu** (`.docx`) vytáhne všechna
**navržená opatření** a zapíše je do **evidenčního Excelu** (`.xlsx`) ve stejném
formátu, jaký se používá pro sledování plnění úkolů.

## Co to dělá

Opatření umí přečíst ze dvou zdrojů:

- **Word RA (`.docx`)** – kapitola **NAVRŽENÁ OPATŘENÍ** s tabulkami
  **PROVOZNÍ** a **INVESTIČNÍ OPATŘENÍ**.
- **PDF příloha (`.pdf`)** – samostatná tabulka opatření jednoho druhu (některé
  RA mají opatření jen v přílohách, ne v těle dokumentu).

Skript z nich přečte jednotlivá opatření a pro každý vodovod vyplní jeden list
Excelu:

| Sloupec | Obsah | Odkud |
|---|---|---|
| A Kalkulační jednice | *(prázdné)* | doplní se ručně (v RA není) |
| B Typ objektu | zdroj / OP / vodojem / síť … | nadpis skupiny v RA |
| C Název objektu | např. „vrt HV-3" | nadpis skupiny v RA |
| D Rok | rok plnění | „Časové plnění" |
| E Druh opatření | provozní / investiční | podle sekce |
| F Číslo opatření | např. `1a.2` | „Číslo" |
| G Navržené opatření | text opatření | „Navržená opatření" |
| H Zodpovídá | kdo | poslední sloupec tabulky |
| I Datum provedení | *(prázdné)* | doplňuje se při plnění |
| J Provedl | *(prázdné)* | doplňuje se při plnění |
| K Poznámka | *(prázdné)* | doplňuje se při plnění |

Vypisují se **všechna** opatření (i průběžná bez roku). Co sledovat nechcete,
smažete ručně.

## Instalace

```bash
pip install -r requirements.txt
```

## Použití

```bash
python ra_to_excel.py \
    --template "Opatření_RA_MT.xlsx" \
    --out "Opatření_RA_MT_vyplneno.xlsx" \
    --add "Posouzeni_Mladejov.docx::Mladějov- Rychnov" \
    --add "Posouzeni_Trebarov.docx::Třebařov- Koruna"
```

- `--template` – existující Excel se správnou hlavičkou (nepovinné; bez něj se
  založí nový sešit).
- `--out` – výstupní soubor.
- `--add "SOUBOR.docx::Název listu"` – Word RA a list, kam se zapíše.
- `--pdf "SOUBOR.pdf::Název listu::druh"` – PDF příloha a list; `druh` je
  `provozní` nebo `investiční` (PDF obsahuje opatření jednoho druhu).

Oba přepínače lze uvést vícekrát a ke stejnému listu přiřadit víc zdrojů
(např. provozní + investiční PDF). Pokud list v šabloně neexistuje, vytvoří se
nový.

Příklad s PDF přílohami:

```bash
python ra_to_excel.py --template "Opatření_RA_PO.xlsx" --out "PO_vyplneno.xlsx" \
    --pdf "RA_Policsko_provozni.pdf::SV Polička::provozní" \
    --pdf "RA_Policsko_investicni.pdf::SV Polička::investiční"
```

Rychlá kontrola jednoho zdroje bez zápisu do Excelu:

```bash
python ra_extract.py "Posouzeni_Mladejov.docx"       # Word
python pdf_extract.py "RA_Policsko_provozni.pdf" provozní   # PDF
```

## Poznámky a omezení

- **Kalkulační jednice** (kód `VF…`) v RA není, doplňuje se ručně mimo analýzu.
- **Název objektu** je best-effort z nadpisů v RA – občas je vhodné ho zkrátit.
- Formát tabulek se mezi RA mírně liší (název sloupce „Navržená opatření" ×
  „Provozní/Investiční opatření", číslování `1a.2` × `1.1.`); skript oba zvládá.
  U nové, výrazně odlišné RA je dobré výsledek zkontrolovat.
- **PDF přílohy nemají sloupec „Zodpovídá"** → sloupec H u nich zůstane prázdný.
- V některých PDF je u pár buněk **přeházený textový layer** (artefakt revizí
  v původním dokumentu); text opatření je pak zkomolený. Řádky s PDF zdrojem je
  vhodné namátkově zkontrolovat.

## Soubory

| soubor | účel |
|---|---|
| `ra_extract.py` | čtení opatření z jedné RA `.docx` (knihovna + rychlý výpis) |
| `ra_to_excel.py` | CLI: vyplní opatření do evidenčního Excelu |
| `requirements.txt` | závislosti (python-docx, openpyxl) |
