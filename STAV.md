# Florián – stav práce a co dál

_Poslední aktualizace: 12. 8. 2026 · verze aplikace **1.205** (na `main`)._
_Pracovní větev: `claude/hy-card-dynamic-pressure-ogptzw` (celá sloučena do `main`)._

Tenhle soubor slouží jako paměť mezi sezeními – kde jsme skončili a čím pokračovat.

## ✅ Hotovo (nasazeno v main)

1. **Karta H – hydrodynamický tlak** (v1.203)
   - Řada dlaždic: průtok m³/h · průtok l/s · **hydrostatický tlak** · **hydrodynamický tlak** (MPa).
   - Přidáno i do editace (pole „Hydrodynamický tlak [MPa]"), do tisku karty a do hromadného importu.
   - Ukládání editace i **Enterem** (už fungovalo dřív).

2. **Jednotné číslování hydrantů po obcích** (v1.203–1.204)
   - Jedna společná číselná řada **1…N na obec**, pořadí **od kraje obce** (nejvzdálenější H od těžiště → řetěz nejbližších sousedů). Písmeno HN/HP se odvozuje z typu.
   - Přečíslovány obce s HN/HP zvlášť (14), doplněny obce úplně bez čísel (39), opraveny obce s částečným číslováním a duplicitami (7).
   - Stav: **0 obcí s duplicitou, 0 obcí s částečným číslováním.** Data v `nazev` (v `hydranty.json` i ve vestavěném poli `HYDRANTY` v `index.html`).

3. **Tisk pro obec → 🗺️ Mapa (klad listů)** (v1.205)
   - Tlačítko „🖨️ Tisk pro obec" má dvě akce: **📋 Seznam H** (tabulka) a **🗺️ Mapa** (klad listů, právě 1 obec).
   - Mapa: A4 na šířku, pouliční podklad (OSM dlaždice), u hydrantů jejich čísla, měrka, legenda typů; **přehledka** s očíslovanými, lehce se překrývajícími A4 listy (jen když jsou ≥2 listy).
   - Adaptivní měřítko: nejmíň listů, dokud se čísla nepřekrývají; prázdné listy se netisknou; strop **12** neprázdných listů/obec.
   - Implementace: statické OSM dlaždice v novém okně (spolehlivý tisk).

## ⏳ Rozpracované / čeká na rozhodnutí

1. **Porovnání tlaků (semafor u hydrodynamického tlaku)** — ČEKÁ NA TEBE.
   - Zatím se hydrodynamický tlak jen zobrazuje (bez hodnocení vyhovuje/nevyhovuje).
   - ČSN 73 0873: 0,2 MPa je vlastně kritérium pro **hydrodynamický** tlak při odběru (u hydrantů pro přímé hašení); u plnění cisteren rozhoduje průtok. V appce je 0,2 MPa zatím navázáno na **statický** tlak.
   - Rozhodnout, jak porovnávat → pak případně přidat semafor a **doplnit sloupce tlaků do protokolu o revizi**.

2. **Klad listů – zpětná vazba z ostrého tisku** — user vyzkouší naživo.
   - Ověřit načtení OSM dlaždic (v sandboxu se nestahují), povolená vyskakovací okna.
   - Doladit měřítko/hustotu listů (strop 12/obec) dle reálného tisku vesnice i většího města.
   - Volitelně: přidat na listy **vodovodní řady** (`vodovod.geojson`), číslo listu do rohu, popř. orientaci na výšku pro protáhlé obce.

3. **Ruční čísla H zadaná v appce** (`domereni[id].cislo`, Firebase) mají přednost před daty (`nazev`).
   - Kdyby po reloadu někde zůstala stará duplicita/číslo, je to tenhle případ → nabídnout „čistící" tlačítko, které u obce srovná ruční čísla s novou řadou.

## 🔑 Kde v kódu (index.html) hledat

- Číslo H: `cisloOf`, `cisloLabel` (prefix HN/HP dle typu), `_cisloNum`, `nextCisloForObec`, `usedCislaInObec`. Čísla uložená v poli `nazev`.
- Klad listů: `generateKladMapa`, pomocné `_kladWorldPx` / `_kladTiles` / `_kladPins` / `_kladScale`. Panel: `buildSeznamPanel` (tlačítka `szGen` = Seznam H, `szMap` = Mapa).
- Tisk seznamu/protokolu: `generateSeznam`, `seznamPageHtml`, `protokolSectionHtml`.
- Karta H + dlaždice tlaků: `tlakStatTile`, `tlakDynTile`; editace `openEditForm` (pole `edTlakD`).
- Verze: `APP_VERSION` (nahoře, ~ř. 1337). Nasazení: GitHub Pages z `main`.

## Postup vydání
Vyvíjí se na `claude/hy-card-dynamic-pressure-ogptzw`, po odsouhlasení merge do `main` (příloha se nasadí). Při každé změně zvednout `APP_VERSION` a datum.
