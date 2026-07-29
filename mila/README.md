# Míla – Historická klikačka

Jednoduchá vědomostní hra o historii **12.–18. století** pro Mílu.
Celá appka je v jednom souboru `index.html` (inline CSS + JS + otázky) – běží
zdarma na GitHub Pages, bez serveru a bez buildu. Stejný princip jako Florián.

## Jak se hraje
- Vybereš **zaměření**: 🇨🇿 jen česká historie / 🌍 celý svět.
- U české historie si můžeš zvolit **level (období)** – nebo všechna období.
- Vybereš délku hry (8 / 12 / všechny otázky).
- U každé otázky jsou **4 odpovědi**. Klikneš na jednu.
- Hned vidíš, zda ses trefila, i **správnou odpověď** a krátkou zajímavost.
- Za správné odpovědi přijde pochvala 🙂; na konci je skóre a medaile.
- Ovládat lze i klávesami **1–4** a **Enter** (další otázka).

## Levely (období české historie)
1. **Přemyslovci** (12.–13. století)
2. **Lucemburkové** (14. století)
3. **Husitství** (15. století)
4. **Habsburkové a Rudolf II.** (1526–1620)
5. **Baroko a osvícenství** (1620–1800)

Celkem **66 otázek** (z toho 42 českých). Otázky i odpovědi se **náhodně
zamíchají**, takže hra se dá hrát opakovaně.

## Okruhy otázek
👑 Panovníci · ⚔️ Bitvy a války · 💍 Sňatky · 🗡️ Vraždy a intriky ·
🕊️ Světci a osobnosti · 📖 Spisovatelé · 🎨 Umění a věda

## Přidání / úprava otázek
V `index.html` najdi pole `QUESTIONS`. Každá otázka je objekt:

```js
{ cat:"Panovníci",
  cz:true,               // je to česká historie? (jinak vynech)
  period:"husitstvi",    // level (jen u českých): premyslovci / lucemburkove /
                         //   husitstvi / habsburkove / baroko
  q:"Otázka?",
  a:["Správná odpověď","Špatná 1","Špatná 2","Špatná 3"],
  e:"Zajímavé vysvětlení, které se ukáže po odpovědi." }
```

- `a[0]` je vždy **správná** odpověď (pořadí se v ní pak zamíchá samo).
- `cat` je okruh (klidně vymysli nový), `cz`/`period` řídí zaměření a level.
- `e` je zajímavost, která se zobrazí po kliknutí.

## Instalace na telefon (Android)
Appka je **PWA** – jde přidat na plochu a spouštět jako běžnou aplikaci
(na celou obrazovku, funguje i offline):

1. Otevři adresu appky v **Chrome** na Androidu.
2. Menu (⋮ vpravo nahoře) → **Přidat na plochu / Nainstalovat aplikaci**.
3. Potvrď – na ploše přibude ikona 👑 „Míla". Spouští se pak jako appka.

Po první návštěvě (s připojením) funguje i bez internetu.

## Kam dál
- Další otázky do jednotlivých levelů (obohatit období).
- Stupně obtížnosti (lehká / těžká) nebo obrázkové otázky.
- Ukládání nejlepšího skóre a odemykání levelů.

## Soubory
| soubor | účel |
|---|---|
| `index.html` | celá hra (otázky + logika + vzhled) |
| `manifest.json` | PWA manifest (název, ikony, barvy) |
| `sw.js` | service worker (offline režim; po změně zvyš `CACHE`) |
| `icon-*.png` | ikony appky (zlatá koruna na vínovém poli) |
| `README.md` | tento popis |
