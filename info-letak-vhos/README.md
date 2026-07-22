# Info-leták VHOS

Statický informační web (leták) pro zákazníky VHOS. Vysvětluje, **jak se
orientovat na našem webu** a **jak nahlásit havárii**.

## Soubory

| Soubor          | Popis                                             |
|-----------------|---------------------------------------------------|
| `index.html`    | Hlavní stránka letáku                             |
| `style.css`     | Styly                                             |
| `manifest.json` | PWA manifest (název, barvy)                        |
| `README.md`     | Tento popis                                        |

## Co je potřeba doplnit

Na stránce jsou označená místa `[DOPLŇTE …]`, která je nutné vyplnit
skutečnými údaji. Konkrétní čísla a odkazy nejsou vymyšlené záměrně –
aby zákazníci nedostali chybnou informaci. Doplňte prosím:

- **Havarijní telefonní číslo** (`index.html` – sekce „Havárii hlaste ihned"
  a krok 2 postupu; upravte i `href="tel:..."`).
- **Názvy sekcí / odkazy** v kartách (faktury, odečty, odstávky, přepis, kvalita vody).
- **Odkaz na online formulář** pro nahlášení poruchy.
- **Kontakty v patičce** (telefon a e-mail zákaznického centra).

## Spuštění

Jde o čistě statický web – stačí otevřít `index.html` v prohlížeči,
nebo nasadit na libovolný hosting (např. GitHub Pages).

```bash
# lokální náhled (volitelně)
python3 -m http.server 8000
# → http://localhost:8000/info-letak-vhos/
```
