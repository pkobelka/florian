# Florián – stav práce a co dál

_Poslední aktualizace: 10. 9. 2026 · verze aplikace **1.215**._
_Pracovní větev: `claude/vodojem-vodovod-assignment-ir9o9s`._

Tenhle soubor slouží jako paměť mezi sezeními – kde jsme skončili a čím pokračovat.

## 🆕 Hotovo v této větvi (čeká na merge do `main`)

**Export do GISu: „Název" = holé číslo H** (v1.215)
   - Nález při zkušebním importu jednoho hydrantu (HN25 Staré Město 111, OBJECTID 3765): do sloupce
     `Název` se psalo `cisloLabel(h)`, tedy **`HN25`** i s předponou podle typu. V GISu je ale v tom
     sloupci holé číslo (u tohoto H `15`), takže by import zapsal jinak formátovanou hodnotu.
   - Nově `cisloOf(h)` → `25`. Předpona **HN/HP zůstává jen v aplikaci** (chip v kartě, klad listů) –
     je to zobrazení, ne data.
   - Zbytek exportu beze změny: 44 sloupců v pořadí `Hydrant_vod_info`, `;`, BOM, CRLF; sloupce, které
     aplikace nevlastní (výšky, TBFID, GLOBALID, Vytvořeno/editace…), jdou prázdné a **při importu se
     nemají mapovat**, párování přes OBJECTID / IČME.

**Vodojem Staré Město + dopočet statického tlaku u hydrantů** (v1.213, poloha v1.214)
   - Nová data `vodojemy.json` (inline v `index.html` jako `VODOJEMY`) z exportu GISu VHOS
     (OBJECTID 69): objem **150 m³**, **2 komory**, hladina **436,6–439,1 m n. m.**, zemní/zásobní,
     rok 1966, IČME, vlastník, poznámka (železobetonová konstrukce).
   - **Dopočet statického tlaku** hydrantu z hladiny ve VDJ a jeho nadmořské výšky:
     `p [MPa] = (hladina VDJ − výška hydrantu) × 0,00981` (1 m vodního sloupce ≈ 9,81 kPa).
     V kartě H (požární i kandidát) přibyl řádek **„Statický tlak z VDJ"** hned za nadmořskou výškou
     a pod dlaždicí hydrostatického tlaku drobný řádek `≈ 0,45 z VDJ`. Do tisku karty jde řádek
     s oběma hladinami (max. i min.).
   - **Zdroj pravdy zůstává měření.** Dopočet je vždy s „≈", nevstupuje do hodnocení ČSN ani do
     exportu pro GIS. Když je hydrant naměřený, ukáže se i rozdíl (`naměřeno 0,52 (−0,07)`) – slouží
     jako kontrola dat.
   - Výška hydrantu se bere z GISu/doměření (`vyskaPovrchu`), jinak z výškopisu (v1.207) – pak je
     dopočet označený „výška z výškopisu". Než výškopis dorazí, je v řádku „čeká na nadmořskou výšku";
     doplní se sám (`wireVyska` teď překresluje i tlak z VDJ).
   - **Přiřazení hydrantu k VDJ** je přes katastr (`ku` v datech VDJ) = jedno tlakové pásmo:
     **754480 Staré Město, 754471 Radišov, 626074 Dětřichov** – přesně to, co pokrývá vrstva vodovodu
     (52 hydrantů). Kunčina (677141) přiřazená **není**, v exportu vodovodu jsou z ní jen 4 úseky.
   - Ověřeno proti měření: výšky odvozené z naměřených statických tlaků vycházejí 375–413 m n. m.,
     což pro Staré Město/Dětřichov/Radišov sedí. Např. H 2 Staré Město 81 – výškopis 376 m →
     dopočet 0,62 MPa = naměřeno 0,62 MPa.
   - **Poloha doplněna (v1.214)** – první export byl čistě atributový (41 sloupců, X/Y ani geometrie
     v něm nebyly), druhý už má `S_JTSK_X = -587178,47`, `S_JTSK_Y = -1094923,91`. Přepočteno
     z EPSG:5514 na WGS84 → **49,79422 / 16,661389**; v datech zůstávají i zdrojové `xJtsk`/`yJtsk`.
   - Kontrola zákresu proti síti: bod padl **0,9 m** od konce tří krátkých řadů (49 / 11 / 33 m –
     přítok, odtok, přepad) a **6,1 m** od konce hlavního řadu PVC 100 (1986). Nejbližší hydranty
     H33 a H32 (429 a 519 m) mají zároveň nejnižší naměřený statický tlak v obci (0,28 MPa), tedy
     leží nejvýš – to k poloze vodojemu sedí.
   - Na mapě je ve vrstvě 🚰 Vodovod značka **VDJ** s bublinou (objem, komory, hladiny, druh/funkce,
     rok, IČME, vlastník, provozovatel, poznámka).
   - Ověřeno v Chromiu (headless, localhost): dopočet z GISové i výškopisné výšky, hydrant bez měření,
     hydrant uměle nad max. hladinou (→ 0 MPa a poznámka), hydrant mimo pásmo (řádek se nezobrazí),
     značka + bublina VDJ po dosazení souřadnic, legenda. Bez chyb v konzoli.

**Tisk zahazoval barvy pozadí – značky vyjely bílé** (v1.212)
   - Nález z Křenova: hydranty se na tištěné mapě kreslily jako **prázdné bílé ovály** a v legendě
     chyběly barevné tečky. Prohlížeč má ve výchozím stavu `print-color-adjust: economy`, což mu
     dovoluje při tisku **zahodit barvy pozadí** (šetření inkoustem). Výplň značky i tečky v legendě
     jsou `background`, takže zmizely; zůstaly jen rámečky a `box-shadow`.
   - Ověřeno na skutečném tiskovém PDF (Background graphics vypnuto): zelená výplň podzemního
     hydrantu v PDF **chyběla**, po přidání `print-color-adjust:exact` tam je. Modrá tam byla jen
     proto, že ji kreslí i rámeček `.krect`.
   - Opraveno ve **všech čtyřech** tiskových sestavách (`@page` bloky na ř. ~2578 protokol,
     ~2674 seznam H, ~2789 klad listů, ~2947 aktualizace) — všechny na barvách pozadí stály a
     žádná to neměla. Vedlejší efekt: v seznamu H se konečně vytisknou **zvýrazněné řádky se
     změnou**, které dosud vyjely bílé.
   - ⚠️ Není to regrese z v1.211 — pozadí se netisklo odjakživa. Ovály z v1.211 byly na papíře
     vidět (tvar je rozměr, ne barva), ale bez výplně.

**Klad listů: značky rozlišené tvarem + přehledka bez hydrantů** (v1.211)
   - **Nález:** na tištěné mapě se nadzemní a podzemní lišily **jen barvou** (`#1565c0` vs `#00897b`),
     tvar byl stejný. Na černobílé tiskárně = k nerozeznání. Legenda v záhlaví navíc ukazovala
     kolečko a čtvereček, což **neodpovídalo** tomu, co se vykreslilo.
   - Nově tvar: **nadzemní = ovál na stojato** (15×20 px), **podzemní = ovál na ležato** (21×14 px),
     `big` varianta 21×27 / 29×19. Barvy zůstávají jako druhý (redundantní) signál. Legenda `.d`
     zmenšena na 8×11 / 11×8, aby seděla s mapou.
   - **Přehledka bez hydrantů** – v jejím měřítku jsou stejně nečitelné a přehledka má ukázat jen
     rozdělení na listy. Legenda symbolů z jejího záhlaví taky odebrána (nemá tam co popisovat).
     Data to neušetří (piny se nestahují), je to čistě čitelnost.
   - Zamítnuto: **HN/HP v bublině**. Změřeno – bublina „12" je 3,9 mm, „HN12" 7,8 mm, přičemž
     nejtěsnější dvojice hydrantů v datech je 4,8 mm → čísla by se překrývala. A aby se nepřekrývala,
     algoritmus by přiblížil mapu → víc listů → víc dlaždic → pomalejší tisk.
   - Zamítnuto: **přehledka bez podkladové mapy**. Změřeno – ušetří 17,3 % dlaždic napříč obcemi,
     ale jen **5,9 % u největší obce**, kde čekání bolí. A bez podkladu nepoznáš, kterou část
     vesnice list pokrývá.

**Tisk pro obec: nic není předvybrané** (v1.210)
   - `buildSeznamPanel` startovalo se zaškrtnutými obcemi (`isPre` = vybrané filtrem, jinak všechny
     viditelné v mapě). Snadno se tím omylem spustil tisk celého pracoviště. Nově prázdné;
     „Vše / nic" vybere všechno jedním klikem (a `allOn=false` teď sedí s výchozím stavem).
   - Protokol o revizi a Aktualizace údajů předvýběr **záměrně ponechány** – tam nikdo netiskl omylem.
   - Opraven `preconnect` z v1.209: měl `crossorigin`, což předehřívá spojení pro CORS požadavky,
     ale dlaždice se načítají bez CORS → hřálo se špatné spojení. Atribut odstraněn.

**Varianta „B" (míň listů = míň dlaždic) NEVYPLATILA SE – neimplementováno**
   - Změřeno přes všechny obce (skript logika = `generateKladMapa`):

     | varianta | stránek | unikátních dlaždic | nejhorší obec | měřítko | min. rozestup H |
     |---|---|---|---|---|---|
     | nyní (MAXP 12, gap 6 mm) | 137 | 2046 | 140 | 1:12000 | 4,8 mm |
     | MAXP 6 | 121 | – | 175 img | 1:12000 | **2,4 mm** |
     | gap 4 mm | 130 | – | 202 img | 1:12000 | 4,1 mm |
     | MAXP 6 + zoom od 14 | 111 | – | 112 img | **1:24000** | **2,4 mm** |

   - Zisk ~11 % dlaždic za cenu rozestupu čísel H **2,4 mm**, přičemž bublina s číslem je sama
     ~4 mm široká → čísla by se překrývala. Varianta s polovičním počtem dlaždic dá 1:24000,
     což je pro terén nepoužitelné.
   - Zkoušeno i **zarovnání listů na mřížku dlaždic** (nezarovnaný list protne 5×4=20 dlaždic
     místo 4×3=12, režie 67 %). Nepomůže: zarovnání vyžaduje větší překryv → víc listů →
     unikátních dlaždic je nakonec **víc** (2046 → 2326).
   - Závěr: počet dlaždic je daný plochou obce při daném měřítku a je prakticky nestlačitelný.
     Jediná reálná páka je zoom = měřítko mapy. Kdyby se to přesto chtělo, stačí v
     `generateKladMapa` snížit konstantu `MAXP` (nyní 12).
   - Pozn.: `MAXP` cap dnes obchází pravidlo 6 mm – u velkých obcí už teď spadne na 4,8 mm.

**Klad listů: tisk čeká na dlaždice + ukazatel průběhu** (v1.209)
   - Čekací skript spouštěl `window.print()` **natvrdo po 8 s**. Změřeno: velká obec si vyžádá
     až **202 dlaždic** (578576, 12 stránek), průměr 38/obec – za 8 s se to nestihne, takže se
     tiskový dialog otevřel nad rozdělanou mapou a tisk vyjel s bílými dírami.
   - Nově: pruh nahoře s průběhem („Načítám mapové podklady… 87 / 202"), tisk se spustí **až po
     dotažení všech** dlaždic. Po 10 s se objeví tlačítko „Tisknout i tak", po 60 s se pruh přepne
     na varování, kolik dlaždic chybí. Pruh se netiskne (`@media print`).
   - Chyby dlaždic (404) se počítají jako dokončené – tisk nezamrzne.
   - Přidán `preconnect`/`dns-prefetch` na `tile.openstreetmap.org`.
   - Ověřeno v Chromiu: v 8 s netiskne, tlačítko naskočí v 10 s, tisk až po dotažení, klik na
     tlačítko tiskne hned, samé 404 nezamrznou, nula dlaždic tiskne hned.

**Klad listů: přehledka ukazovala listy useknuté** (v1.208)
   - Výřez přehledky se počítal jen z obálky hydrantů, ale mřížka listů je z principu větší
     (každý list je celá A4 a mřížka se na obálku centruje) → `.kmap {overflow:hidden}` ustřihl
     rámečky krajních listů.
   - Změřeno na datech: postiženo bylo **všech 18 obcí s víc než jedním listem**, přesah 0,3 % až
     30,1 % šířky výřezu. U Mor. Třebové jen 0,3 %, ale to stačilo na ustřižení 2px rámečku, takže
     vnější rám kladu chyběl úplně.
   - Oprava v `generateKladMapa`: výřez se počítá z **obálky listů** (`gx0/gy0/gx1/gy1`) plus 6 %
     vzduchu (`MARG`), overview zoom se vybírá proti téže obálce. Ověřeno: přesah 0 u všech 18 obcí,
     okraj 3 % ze všech stran, žádný hydrant nevypadl z výřezu.
   - Vedlejší efekt (zamýšlený): přehledka je oddálenější, obec je na ní menší – vejdou se celé listy.
   - ⚠️ **Neověřeno naživo:** dlaždice OSM sem proxy nepustí, ověřena jen geometrie (rámečky + piny).

**Nadmořská výška v kartě H** (v1.207)
   - GIS má sloupce `Výška povrchu [m.n.m.]` a `Výška podzemní [m.n.m.]`, ale **v exportu, který máme
     (`hydranty.json`, `kandidati.json`), hodnoty úplně chybí** – proto nové pole `vyskaPovrchu`.
   - Karta H (požární i kandidát): řádek **„Nadmořská výška"** hned za obcí. Hodnota z GISu/doměření
     má přednost; když chybí, dopočítá se orientačně z výškopisu podle GPS a ukáže se jako
     `≈ 411 m n. m. (výškopis)` (šedě). Cache v `localStorage` pod `florian_vyska`.
   - Editace: pole „Nadmořská výška [m n. m.]" v sekci *Údaje pro GIS*; výškopisná hodnota je jen
     v placeholderu, **nikdy se nepředvyplní** (ať se odhad nedostane omylem do GISu).
   - Export do GISu: sloupec `Výška povrchu [m.n.m.]` už není prázdný – plní se z `vyskaPovrchu`
     (jen skutečná hodnota, orientační výškopis se **neexportuje**). Pole je i ve `FL_EXPORT_FIELDS`
     (změna se počítá jako úprava k exportu) a v hromadném importu.
   - ⚠️ **Neověřeno naživo:** volání výškopisu jde na `api.open-meteo.com/v1/elevation` (Copernicus DEM,
     přesnost jednotky metrů); v sandboxu ho proxy nepustila. Vyzkoušet na GitHub Pages. Kdyby služba
     nevyhovovala, stačí přepsat konstantu `FL_DEM_API` (a tvar odpovědi `{"elevation":[…]}`).
   - 📌 **Až přijde nový export z GISu:** do generátoru `hydranty.json` doplnit mapování sloupce
     `Výška povrchu [m.n.m.]` → `vyskaPovrchu`, pak se hodnoty ukážou samy.

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
- Nadmořská výška: `vyskaGis` / `vyskaDem` / `vyskaHtml` / `vyskaText` / `vyskaFactHtml` / `wireVyska`,
  fetch `flFetchVyska` + konstanta `FL_DEM_API`. Editace: pole `edVyska`.
- Verze: `APP_VERSION` (nahoře, ~ř. 1338). Nasazení: GitHub Pages z `main`.

## Postup vydání
Vyvíjí se na `claude/floriana-reseni-gln63p`, po odsouhlasení merge do `main` (appka se nasadí). Při každé změně zvednout `APP_VERSION` a datum.
