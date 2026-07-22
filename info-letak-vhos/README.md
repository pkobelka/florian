# Info-leták VHOS a.s.

Statická webová stránka (leták) pro zákazníky **VHOS a.s.** Shrnuje na jednom
místě to nejdůležitější:

- 🚨 **Nahlášení havárie** – havarijní linka **722 659 171** (NONSTOP 24/7)
- 🏘️ **MOJE OBEC** – informace o vodě ve vaší obci (havárie, odstávky, kvalita
  vody, ceny, kontakty, dokumenty)
- 👤 **MŮJ ÚČET** – zákaznická zóna k odběrnému místu (faktury, zálohy, platby,
  historie spotřeby, požadavky, aktuality)
- 🏗️ **Vyjadřovací portál** – pro stavbu / rekonstrukci
- ☎️ Kontakty – Zákaznické centrum **461 357 154**, Zákaznická linka
  **461 357 111** (Po–Pá 7:00–15:00), web **www.vhos.cz**

## Soubory

| Soubor          | Popis                                    |
|-----------------|------------------------------------------|
| `index.html`    | Hlavní stránka letáku                    |
| `style.css`     | Styly (firemní modrá + červený akcent)   |
| `manifest.json` | PWA manifest (název, barvy)              |
| `README.md`     | Tento popis                              |

## Poznámky

- Odkazy „Otevřít / Přihlásit se" míří na `www.vhos.cz`. Až budou známé přesné
  URL podstránek (MOJE OBEC, MŮJ ÚČET, Vyjadřovací portál, přihlášení k odběru),
  stačí je doplnit do `href` v `index.html`.
- Původní tištěné letáky obsahovaly QR kód pro přihlášení k odběru upozornění na
  havárie a odstávky. Zde je nahrazen tlačítkem/odkazem na web; pokud chceš QR
  kód zachovat i tady, dodej cílovou URL a doplním jej.

## Spuštění

Čistě statický web – stačí otevřít `index.html` v prohlížeči, nebo nasadit na
libovolný hosting (např. GitHub Pages).

```bash
# lokální náhled (volitelně)
python3 -m http.server 8000
# → http://localhost:8000/info-letak-vhos/
```
