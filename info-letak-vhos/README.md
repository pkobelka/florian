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

| Soubor              | Popis                                                     |
|---------------------|-----------------------------------------------------------|
| `index.html`        | Webová verze letáku (2× A5, k tisku i online)             |
| `style.css`         | Styly (firemní modrá + červený akcent)                   |
| `manifest.json`     | PWA manifest (název, barvy)                              |
| `VHOS-letak-A5.docx`| **Editovatelná Word verze** (2× A5) s rámečky na screeny |
| `vhos-letak-A5.pdf` | PDF náhled webové verze                                  |
| `logo-vhos.png`     | Logo VHOS a.s. vyrenderované z SVG                        |
| `build_docx.js`     | Skript, který generuje Word (`node build_docx.js`)       |
| `logo_render.html`  | Předloha pro vyrenderování loga do PNG                    |
| `README.md`         | Tento popis                                              |

### Word verze – vkládání vlastních screenů

V dokumentu `VHOS-letak-A5.docx` jsou dva modré čárkované rámečky s textem
„SEM VLOŽTE SCREEN". Klikněte do rámečku a přes **Vložit → Obrázek** vložte svůj
screenshot webu (strana 1 = MOJE OBEC / vyhledávač obce, strana 2 = MŮJ ÚČET).
Texty i čísla lze libovolně přepsat.

> Pozn.: `build_docx.js` vyžaduje balíček `docx` (`npm install docx`). PDF náhled
> Wordu se v tomto prostředí nepodařilo vyrenderovat (LibreOffice zde nefunguje),
> samotný `.docx` je však platný a otevře se ve Wordu správně.

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
