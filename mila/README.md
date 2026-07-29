# Míla – Historická klikačka

Jednoduchá vědomostní hra o historii **12.–18. století** pro Mílu.
Celá appka je v jednom souboru `index.html` (inline CSS + JS + otázky) – běží
zdarma na GitHub Pages, bez serveru a bez buildu. Stejný princip jako Florián.

## Jak se hraje
- Vybereš délku hry (8 / 12 / všechny otázky).
- U každé otázky jsou **4 odpovědi**. Klikneš na jednu.
- Hned vidíš, zda ses trefila, i **správnou odpověď** a krátkou zajímavost.
- Za správné odpovědi přijde pochvala 🙂; na konci je skóre a medaile.
- Ovládat lze i klávesami **1–4** a **Enter** (další otázka).

## Okruhy otázek
👑 Panovníci · 💍 Sňatky · 🗡️ Vraždy a intriky · 📖 Spisovatelé · 🎨 Umění a věda

Odpovědi se u každé otázky **náhodně zamíchají**, takže správná není pořád na
stejném místě a hra se dá hrát opakovaně.

## Přidání / úprava otázek
V `index.html` najdi pole `QUESTIONS`. Každá otázka je objekt:

```js
{ cat:"Panovníci",
  q:"Otázka?",
  a:["Správná odpověď","Špatná 1","Špatná 2","Špatná 3"],
  e:"Zajímavé vysvětlení, které se ukáže po odpovědi." }
```

- `a[0]` je vždy **správná** odpověď (pořadí se v ní pak zamíchá samo).
- `cat` je okruh (klidně vymysli nový).
- `e` je zajímavost, která se zobrazí po kliknutí.

## Instalace na telefon (Android)
Appka je **PWA** – jde přidat na plochu a spouštět jako běžnou aplikaci
(na celou obrazovku, funguje i offline):

1. Otevři adresu appky v **Chrome** na Androidu.
2. Menu (⋮ vpravo nahoře) → **Přidat na plochu / Nainstalovat aplikaci**.
3. Potvrď – na ploše přibude ikona 👑 „Míla". Spouští se pak jako appka.

Po první návštěvě (s připojením) funguje i bez internetu.

## Kam dál
- **Další úrovně / okruhy** (těžší otázky, jiná období, obrázky).
- Výběr okruhu na úvodní obrazovce.
- Případně ukládání nejlepšího skóre.

## Soubory
| soubor | účel |
|---|---|
| `index.html` | celá hra (otázky + logika + vzhled) |
| `manifest.json` | PWA manifest (název, ikony, barvy) |
| `sw.js` | service worker (offline režim; po změně zvyš `CACHE`) |
| `icon-*.png` | ikony appky (zlatá koruna na vínovém poli) |
| `README.md` | tento popis |
