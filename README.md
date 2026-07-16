# Florián

PWA pro **mapu požárních hydrantů**. Sesterská appka k [AquaCtrl](https://github.com/pkobelka/aquactrl) – vše v jednom souboru `index.html` (inline CSS + JS + data + knihovna mapy), běží zdarma na GitHub Pages, bez serveru a bez buildu.

## Stav: Fáze 1 (zkušební, jen pro čtení)

- Mapa hydrantů jednoho vlastníka: **Skupinový vodovod Moravskotřebovska** (199 hydrantů).
- Data převzata z CSV VHOS, souřadnice přepočteny ze **S‑JTSK (EPSG:5514) na GPS (WGS84)**.
- **Data jsou napevno v `index.html`** (read‑only). Bez přihlášení, fotky se zatím neukládají do cloudu.

### Co umí
- Hydranty na mapě jako **symboly** (🔴 nadzemní / ⚫ podzemní) nad podkladem OpenStreetMap.
- **Shlukování** (clustering) – při oddálení se body slučují do kolečka s počtem, při přiblížení se rozpadají.
- **Vrstva pokrytí** – přepínač „Pokrytí 200 m" vykreslí kolem každého hydrantu kruh o poloměru 200 m (dle ČSN 73 0873). Překryv = pokryto, mezera = díra.
- **Karta hydrantu** (klik na bod): všechny údaje z tabulky, zvýrazněné hodnoty (průtok, tlaky), soulad s ČSN, **výřez mapy s kružnicí a okolními hydranty**, přidání fotografie (vyfotit / z galerie), **stažení (PDF přes tisk)** a **tisk (A4)**.

## Kam dál (Fáze 2)
- Přihlášení podle vlastníka (každý vidí jen svoje hydranty) – všech 19 vlastníků.
- Ukládání fotek do cloudu (Firebase Storage) a úpravy údajů.
- Skutečné ikony/symboly dle předloh (nadzemní hydrant, poklop, favicon).

## Soubory
| soubor | účel |
|---|---|
| `index.html` | celá appka (mapa Leaflet + shlukování + data + karty + tisk) |
| `hydranty.json` | zdrojová data (199 hydrantů) – jinak už jsou vložená v `index.html` |
| `manifest.json` | PWA manifest |
| `sw.js` | service worker (scope `/florian/`) |
| `icon-*.png` | ikony (modrý hydrant – prozatímní, dle faviconu) |

## Vývoj
Data se generují z CSV skriptem (přepočet S‑JTSK→GPS, filtr vlastníka) a vkládají do `index.html`. Po každé změně bumpni `CACHE` v `sw.js`.
