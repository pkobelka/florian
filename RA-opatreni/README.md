# RA-opatření

Nástroj, který z **rizikové analýzy vodovodu** (`.docx`) vytáhne všechna
**navržená opatření** a zapíše je do **evidenčního Excelu** (`.xlsx`) ve stejném
formátu, jaký se používá pro sledování plnění úkolů.

## Co to dělá

Riziková analýza (RA) má ustálenou strukturu. V kapitole **NAVRŽENÁ OPATŘENÍ**
jsou tabulky **PROVOZNÍ OPATŘENÍ** a **INVESTIČNÍ OPATŘENÍ**. Skript z nich
přečte jednotlivá opatření a pro každý vodovod vyplní jeden list Excelu:

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
- `--add "SOUBOR.docx::Název listu"` – jedna RA a list, kam se zapíše. Lze
  uvést vícekrát. Pokud list v šabloně neexistuje, vytvoří se nový.

Rychlá kontrola jedné RA bez zápisu do Excelu:

```bash
python ra_extract.py "Posouzeni_Mladejov.docx"
```

## Poznámky a omezení

- **Kalkulační jednice** (kód `VF…`) v RA není, doplňuje se ručně mimo analýzu.
- **Název objektu** je best-effort z nadpisů v RA – občas je vhodné ho zkrátit.
- Formát tabulek se mezi RA mírně liší (název sloupce „Navržená opatření" ×
  „Provozní/Investiční opatření", číslování `1a.2` × `1.1.`); skript oba zvládá.
  U nové, výrazně odlišné RA je dobré výsledek zkontrolovat.

## Soubory

| soubor | účel |
|---|---|
| `ra_extract.py` | čtení opatření z jedné RA `.docx` (knihovna + rychlý výpis) |
| `ra_to_excel.py` | CLI: vyplní opatření do evidenčního Excelu |
| `requirements.txt` | závislosti (python-docx, openpyxl) |
