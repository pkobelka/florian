# Florián 2.0 — poznámky k projektu (stav pro pokračování)

PWA mapa **požárních hydrantů** VHOS, a.s. Sesterská appka k AquaCtrl.
Vše v jednom `index.html` (inline CSS+JS+data+Leaflet). Hostováno na **GitHub Pages**:
https://pkobelka.github.io/florian/ · repo `pkobelka/florian`, větev `main`.

## Aktuální verze
- `APP_VERSION` v `index.html` a `CACHE` v `sw.js` — **při každém nasazení obojí zvýšit**.
- Nyní: **v1.126**, cache `florian-v133`. (Nasazuje se přes merge dev větve do `main`.)

## Hotovo v1.126 (tato session) — umístění/poznámka do podtitulku karty (na klik)
- **Číslo H „na klik" (v kartě)** — chip 🏷️ H<č> už je v hlavičce od v1.124; stálý odznak
  na mapě zatím NEděláme (uživatel preferuje jen v kartě). Návrh odznaku hotov (scratchpad),
  parkuje.
- **Umístění/poznámka z Excelu v podtitulku karty — bez řádku navíc.** Nové zdrojové pole
  `umisteniText`; podtitulek karty (`.sub`) ukazuje `candVal(h,'umisteniText')||txt(h.umisteni)`
  → místo „na řadu" ukáže třeba „u č.p. 45" (Radišov) nebo „mezi čp 6 a 8 · v komunikaci"
  (Bílá Studně). Doplněno 7 bodům (Radišov 4 + Bílá Studně 3). Řeší obavu „řádek navíc".
- GIS: číslo/poznámka nemají v GIS exportu vlastní sloupec (viz CSV schéma) → do GISu půjde
  vše do `Poznámka` (jediné volné pole), formát doladit se správcem GIS. Export CSV lze
  srovnat na přesné hlavičky GIS (`Hydrant_vod_info.csv`).

## Hotovo v1.125 (tato session) — oficiální data Bílá Studně + oprava průtoku (m³/h→l/s)
- **Bílá Studně (3 body) doplněna ze seznamu** (párování dle č.p. + typu): id 3785=H1
  (Bílá Studně 2, nadz), 2228=H2 (6, podz), 2229=H3 (12, podz). Doplněno `cislo` (1–3),
  `dnPotrubi` (80), `tlakStat` beze změny (0,58/0,42/0,38 — Excel už v MPa).
- **DŮLEŽITÉ — oprava průtoku:** app měla u těchto 3 uložené **m³/h omylem jako l/s**
  (39,1 / 15,6 / 16,6). Opraveno na správné l/s (**10,9 / 4,3 / 4,6**). Ovlivňuje i
  auto-vyhodnocení ČSN (≥4 l/s). Pozor: tenhle unit-bug může být i u dalších obcí —
  ověřovat proti seznamům (l/s vs m³/h = ×3,6).
- Rozdíl mezi seznamy: **Radišov měl tlak v barech** (÷10), **Bílá Studně už v MPa**.
  Umístění „měkčí" (mezi čp 6 a 8), ale číslo popisné + typ na spárování stačí.
- Rozpracováno (viz níže): číselný odznak H na mapě (návrh hotov, čeká na schválení),
  editovatelné pole „Číslo H", umístění text (počká na správce GIS).

## Hotovo v1.124 (tato session) — oficiální čísla H + DN potrubí z Excelu (Radišov)
- **Doplněna oficiální data z „Seznam PH" (Excel starostů/VHOS) pro Radišov** přímo do
  zdrojových dat `HYDRANTY` (4 body). Párování **podle čísla popisného**: app `upresneni`
  „Radišov 45" ↔ Excel „umístění" „u č.p. 45". Mapa: id 2148=H1(45), 2147=H2(5), 840=H3(42),
  837=H4(32). Doplněno/aktualizováno: `cislo` (1–4), `dnPotrubi` (80/80/100/80), `prutok`
  (zaokr. na 1 desetinu: 9,9/13,8/9,5/11,7), `tlakStat` (Excel „Mpa" byly bary → ÷10:
  0,4/0,5/0,36/0,52). Měření z 15.7.2025.
- **Nový chip v kartě „🏷️ H<č>"** (`cisloHChip`, čte `candVal(h,'cislo')`) v hlavičce vedle
  „📏 nejbližší H". DN potrubí se ukazuje přes existující řádek (v1.105), `dnPotrubi` je i v
  `FL_EXPORT_FIELDS`.
- **Postup pro další obce (až přijdou seznamy):** stejný styl — najít hydrant podle textu
  umístění (č.p.) ↔ `upresneni`, zapsat do zdrojových `HYDRANTY`: `cislo`, `dnPotrubi`,
  `prutok` (1 des.), `tlakStat` (bar→MPa). Skript na patch objektů viz commit v1.124.
  Pozor: tlak v Excelu bývá v barech i když hlavička říká „Mpa" (÷10).

## Hotovo v1.123 (tato session) — zrušeno pracovní číslo H u bodů k doměření
- **Globální pořadové číslo „H1, H2…" u vybraných bodů zrušeno** (bylo arbitrární, plete se
  s oficiálním číslem hydrantu). Vybraný bod = zelený puntík s **✓** (`candIcon` badge),
  karta „✓ Vybráno k doměření", tlačítko „✓ Vybráno — zrušit".
- **Seznam „Změřit" se řadí podle obce** (`_domTown`, `localeCompare cs`), ne podle pořadí
  kliku; položky vedou obcí místo čísla (todo i historie).
- **Nová čísla se nepřidělují** (odebrán back-fill IIFE + `idx` z `markCand`). `flSeq/flNextNum/
  cislujDomereni` ponechány (nevolají se), stará uložená čísla se nemažou, jen nezobrazují → vratné.
- Pozn.: oficiální per-obec číslování H (ze seznamu starostů v Excelu) je samostatná věc —
  plánuje se doplnit do karty z nahraných tabulek (viz níže „Rozdělané").

## Hotovo v1.122 (tato session) — tip „foťte na šířku" u fotky
- **Decentní nápověda u tlačítek fotky** v obou kartách (`.ptip` pod `.pbtns`):
  „💡 Nejlépe foťte na šířku (naležato)". Orientaci systémového foťáku z webu vynutit
  nejde (`<input capture>`), tak aspoň doporučí — fotky se v kartě i clusteru zobrazují
  na ležato, takže landscape sedí líp (a míň se pak musí otáčet přes 🔄).

## Hotovo v1.121 (tato session) — plné názvy v mřížce + sjednocená mezera
- **Zkratky v mřížce nahrazeny plnými názvy:** 🔵 Požární / 🟢 Vybrané / 🟣 Ostatní
  (dřív Pož./Vybr./Ost.) — místa je dost (mřížka je široká jako panel).
- **Sjednocená mezera pod mřížkou:** `.cov-matrix` mělo `margin-bottom:8px`, který se
  sčítal s `gap:8px` ve `.ctrl` (flex column) → dole dvojnásobná mezera. Margin odebrán,
  teď mezera stejná jako mezi ostatními tlačítky hamburgeru.

## Hotovo v1.120 (tato session) — oprava „Nepokryto" nezhasínalo + mezera v „Do GISu"
- **Oprava: „Nepokryto" (`gapToggle`) po vypnutí nezhasínalo body.** Zapnutí „Nepokryto"
  si samo zapne vrstvu Ostatní (aby bylo co zvýraznit), ale vypnutí dřív jen zrušilo
  oranžové zvýraznění a vrstvu nechalo zapnutou → body zůstaly na mapě. Nově příznak
  `gapTurnedCand`: když vrstvu zapnulo „Nepokryto", při vypnutí ji zase zhasne
  (`candToggle.click()`); když si ji zapnul uživatel sám, nechá ji a zruší jen zvýraznění.
  Po přepnutí volá `buildCovPanel()` (sync mřížky – Ostatní „vidět").
- **Oprava mezery v „🔼 Do GISu".** Prázdný `<span id="gisCount">` byl samostatná flex
  položka tlačítka (`.btn-toggle{gap:7px}`) → zbytečná mezera + text utíkal od středu.
  Text i počet nově v jednom obalovém `<span>` (žádná flex mezera uvnitř), počet dostává
  vlastní mezeru jen když je (`' ('+n+')'`). Tlačítko je čistě vycentrované.

## Hotovo v1.119 (tato session) — dvojice tlačítek + Poznámky bez přepínače
- **Nepokryto + Poznámky do jedné dvojice** (`.ctrl-row`): „💡 Nepokrytá oblast" zkráceno
  na **„💡 Nepokryto"**, vedle „📝 Poznámky".
- **Tisk mapy + Do GISu do dvojice** (`.ctrl-row`): „🔼 Nahrání do GISu" zkráceno na
  **„🔼 Do GISu"**. Na mobilu je `#printMapBtn` skrytý → „Do GISu" se roztáhne na celou
  šířku (flex, jako u ostatních dvojic).
- **Poznámky: zrušen posuvník `.sw`**, místo něj se tlačítko **zabarví, když je zapnuté**
  (`#poznToggle.on` = modré, jako ostatní přepínače). Sjednodušší a konzistentní.
- Ušetřeny 2 řádky v hamburgeru.

## Hotovo v1.118 (tato session) — poloměr 200 m napevno, poznámka v titulku mřížky
- **Selektor poloměru (100/150/200 m) v mřížce zrušen** — poloměr je napevno `COVERAGE_RADIUS`
  = 200 m (default). Ušetřen celý řádek. Místo něj **poznámka v titulku**:
  „🎯 Zobrazení a pokrytí · poloměr 200 m" (`.cm-r`, decentní menší text). `setCoverageRadius`
  zůstává v kódu (nevolá se), COVERAGE_RADIUS dál 200. (Kdyby bylo někdy potřeba měnit,
  vrátit chipy.)

## Hotovo v1.117 (tato session) — mřížka „Zobrazení a pokrytí" (3 druhy H × vidět/pokrytí)
- **Sloučené tlačítko „🎯 Pokrytí a zobrazení" (rozbalovací panel) nahrazeno kompaktní
  mřížkou přímo v hamburgeru** (`#covMatrix`, inline v `.ctrl`, žádné rozklikávání).
  Tři řádky = tři druhy H (**🔵 Pož. / 🟢 Vybr. / 🟣 Ost.**), dva sloupce = **👁 vidět**
  (vrstva na mapě) a **🎯 pokrytí** (kruhy v barvě druhu). Pod tím výběr poloměru.
- **Třetí kategorie přejmenována na „Vybrané"** (dřív „K doměření" v tomto ovládání;
  v mřížce zkratka „Vybr."). Feature/panel „Změřit" zůstává.
- **Nové přepínače viditelnosti vrstev:** `fireLayerOn` (🔵 vidět → add/removeLayer
  `cluster`) a `markedShownOn` (🟢 vidět → guard v `renderMarked`). Oba default `true`.
  🟣 vidět reuse existující `candToggle` (vrstva Ostatní hydranty). Pokrytí beze změny:
  `coverageOn`/`domCovOn`/`othersCovOn`. „Vše" (`allBtn`) resetuje i viditelnost na true.
- `buildCovPanel()` teď kreslí mřížku do `#covMatrix` a napojuje `.cm-c` buňky na
  `setFireLayer`/`setCov('fire')`/`setMarkedShown`/`setCov('dom')`/candToggle/`setCov('oth')`.
  `updateCovBtn` zredukováno na `flHeaderSub` (tlačítko `covBtn` + panel `covPanel` zrušeny,
  stejně tak IIFE handler; init render přes `buildCovPanel()`). Tisk-restore respektuje `fireLayerOn`.

## Hotovo v1.116 (tato session) — delší tlačítko Pracoviště + otočení fotky
- **Tlačítko „Pracoviště" delší, „Vše" zúžené.** `#allBtn` dostal `flex:0 0 auto`
  (přes id, aby přebilo `.ctrl-row>button{flex:1}`) → „Vše" se smrskne na obsah a
  „Pracoviště" (flex:1) zabere zbytek řádku. Jmenovka `#stredLbl` má vlastní
  `max-width:240px` (dřív sdílených 150px) → vejde se celý název pracoviště.
- **Otočení fotky v kartě.** Nové tlačítko **🔄** v `.pbtns` (u Vyfotit/Galerie/🗑️,
  jen když fotka je) v obou kartách (požární i kandidát). `rotatePhoto(h)` **nemění
  pixely** — jen uloží **příznak úhlu** 0/90/180/270° (klik = +90° po směru hodin):
  do `photoRot` + localStorage `florian_photo_rot` a do Firebase
  `florian_foto/<id>.rot` (`.update`, `cloudRot` z listeneru, cloud vyhrává jako
  u url). Zobrazení otočí přes **CSS `transform:rotate`** — miniatura `.pimg`
  (u r90/r270 přepnuto na `object-fit:contain`), zoom `#photoZoom img`
  (r90/r270 mají `max-width:94vh/max-height:94vw`, ať se vejdou) i tisk `.pphoto`.
  Třída se sází přes `rotCls(id)` v markupu, `flZoomPhoto(src,deg)`. **Funguje i pro
  fotku od kolegy jen v cloudu** (nečte se obraz → žádný CORS problém) a otočení
  se **propíše všem** (uloženo u fotky). `deletePhoto` maže i rotaci. Řeší
  „Rozstání 91: foto naležato, focené nastojato".

## Hotovo v1.115 (tato session) — tlačítko „Vše" u Pracoviště + roletky se zavírají po výběru
- **Nové tlačítko „Vše"** ve dvojici s „Pracoviště" (`.ctrl-row`) — zruší filtry a ukáže všechny
  požární H (přesunut sem `allBtn`, zviditelněn, přejmenován). Odebráno z panelu Pokrytí
  („🎯 Všechny požární H" v sekci Zobrazení) i skryté tlačítko z lišty. `#stredLbl` dostal ellipsis.
- **Roletky filtrů se po výběru zavřou:** výběr pracoviště / svazku / obce (`onchange`
  checkboxu) nově zavře příslušný panel (`panel.classList.remove('open')`). Multi-výběr jde
  dál přes znovuotevření.

## Hotovo v1.114 (tato session) — shrnutí pokrytí přesunuto do horního řádku
- Shrnutí vybraného pokrytí je nově **v podtitulku modré hlavičky** (`flHeaderSub`), vedle
  vybraného pracoviště/obce: „Požární hydranty · 🏭 Jevíčko · 🏘️ Chornice · 🎯 🔵🟣 200 m · ➕ Ostatní H".
  `updateCovBtn` volá `flHeaderSub`, takže se to obnoví při změně pokrytí i filtrů.
- **Zrušen samostatný řádek `#covSum` pod tlačítkem** (z v1.113) + jeho CSS/`updateCovSummary` —
  ať to není dvakrát.

## Hotovo v1.113 (tato session) — řádek shrnutí v liště pod tlačítkem Pokrytí (přesunuto v1.114)
- (Zavedeno `#covSum` pod tlačítkem; v1.114 přesunuto do horní hlavičky.)

## Hotovo v1.112 (tato session) — tlačítko Pokrytí ukazuje, co je vybráno
- Tlačítko přejmenováno na **„🎯 Pokrytí a zobrazení"** (sladěno s hlavičkou panelu).
- `updateCovBtn` nově **rozsvítí aktivní volby**: barevné tečky zapnutých kategorií
  (🔵 Požární / 🟢 K doměření / 🟣 Ostatní) + poloměr, `➕` když je vrstva Ostatní hydranty.
  Když je něco zapnuté, tlačítko se zvýrazní (`#covBtn.on` modrý rámeček/text). Volá se
  i z `buildCovPanel`, takže popisek drží aktuální stav.

## Hotovo v1.111 (tato session) — „Ostatní H" a „Všechny požární H" do panelu Pokrytí
- Panel přejmenován na **„🎯 Pokrytí a zobrazení"**; přibyla sekce **Zobrazení**:
  - **➕ Ostatní hydranty** (přepínač, zrcadlí `candOn`) — ovládá skrytý `candToggle`.
  - **🎯 Všechny požární H** (akce) — spouští skrytý `allBtn` (reset filtrů).
- Tlačítka `candToggle` a `allBtn` **skryta z lišty** (`display:none`, zůstávají v DOM →
  vazba `gapToggle→candToggle` funguje). Lišta kratší o 2 tlačítka.
- **Zapnutí „🟣 Ostatní" pokrytí rovnou zapne vrstvu** Ostatní hydranty (`setCov` → `candToggle.click()`),
  ať se fialové kruhy hned ukážou.

## Hotovo v1.110 (tato session) — oprava: tlačítko polohy překrývalo panel
- `.locate` mělo `z-index:900` stejně jako `.ctrl`, a bylo v DOM později → kreslilo se
  nad rozbaleným panelem (Pokrytí ap.). Sníženo na **`z-index:899`** (pod lištu, stále nad
  mapou) → panel je teď nad tlačítkem polohy.

## Hotovo v1.109 (tato session) — pokrytí sjednoceno do jednoho panelu
- **Tři tlačítka pokrytí** (Pokrytí+selektor, Pokrytí doměřovaných, Pokrytí ostatních)
  sloučena do **jednoho „🎯 Pokrytí ▾"** (`covBtn` → panel `covPanel`, `buildCovPanel`).
  Lišta/hamburger se tím zkrátí (3 tlačítka → 1).
- Panel: **poloměr** (chipy 100/150/200 m, přes `setCoverageRadius`) + tři kategorie
  s přepínačem a barvou: 🔵 Požární, 🟢 K doměření, 🟣 Ostatní. Popisek tlačítka drží
  aktuální poloměr. Hinty u „Ostatní" (zapni vrstvu / zúži na obec) jsou v panelu.
- Logika kreslení kruhů beze změny (jen přesunuté ovládání); `setCov()` + `applyCovLayers()`.

## Hotovo v1.108 (tato session) — pokrytí i pro „Ostatní" (neoznačené kandidáty)
- **Nový přepínač „🟣 Pokrytí ostatních"** (`othersCovToggle`, `othersCovOn`) vedle „Pokrytí"
  a „Pokrytí doměřovaných". Kreslí **fialové** kruhy (`#8e24aa`) u neoznačených kandidátů —
  vizuálně odlišené od modrých (požární) a zelených (k doměření).
- **Výkon:** kreslí se jen po **zúžení na obec/středisko** (`visibleObecSet()`), a max **800**
  kruhů. Bez filtru / při zapnutí bez vrstvy „Ostatní hydranty" appka jednou napoví.
- Poloměr sdílí se všemi vrstvami (selektor 100/150/200 m u tlačítka Pokrytí, už z v1.97).

## Hotovo v1.107 (tato session) — GIS nahrávání do jednoho panelu (Požádat/Stáhnout + historie)
- **Sjednoceno do jednoho tlačítka „🔼 Nahrání do GISu (N)"** (`gisBtn`) → panel `gisPanel`
  (`buildGisPanel`). Zrušena samostatná tlačítka Export + Poprosit + řádek historie.
- Panel: stav „Ke stažení: N změn od posledního nahrání", **akce dle role** — GIS/Admin
  „📤 Stáhnout změny (CSV)", ostatní „🔼 Požádat o nahrání" (přejmenováno z „Poprosit").
  Pod tím **historie žádostí a nahrání** (`_gisReqList` z `florian_gis_requests`, 🔼 žádost /
  ✅ nahráno + čas). `flApplyRoleUI` už jen aktualizuje počet + přestaví panel. `gisBtn` vidí všichni.

## Hotovo v1.106 (tato session) — Tisk mapy skrytý na mobilu/landscape
- `#printMapBtn{display:none}` v `@media (max-width:640px),(max-height:480px)` — tisk mapy je
  desktopová věc; na telefonu i landscape se skryje, na tabletu/desktopu zůstává.

## Hotovo v1.105 (tato session) — pole „Osazen na potrubí DN" v kartě
- **Nový údaj `dnPotrubi`** (DN potrubí, na kterém je hydrant osazen — jiné než DN hydrantu).
  V edit formuláři `#edDnPot` = select (— / 80 / 100 / 150). Ukládá se do `domereni.dnPotrubi`.
  Zobrazeno v detailech karty („Osazen na potrubí DN", za „DN hydrantu"). Přidáno do
  `FL_EXPORT_FIELDS` → jde i do CSV pro GIS.

## Hotovo v1.104 (tato session) — historie žádostí o nahrání do GISu + další dvojice
- **Historie žádostí/nahrání do GISu** (`#gisReqHist`, viditelná všem — ať se neprosí 2×).
  „Poprosit" zapíše do `florian_gis_requests` (`{type:'req',by,pid,n,ts}`), export zapíše
  `{type:'done',by,ts}`. Listener `limitToLast(30)` → `flRenderGisReq` (poslední nahoře jako
  hlavička „🕘 …", rozklik ukáže 10 posledních). `fmtDateTime`. **Vyžaduje DB pravidlo
  `florian_gis_requests` (auth!=null)** — přidáno v `mojebudky/database.rules.json` (auto-deploy).
  Komu žádost chodí: role **GIS + Admin** (`flGisTargets`) — admin/Petr ji tedy dostává.
- **Dvojice K doměření + Úkoly** vedle sebe; „K doměření" tlačítko přejmenováno na **„Změřit"**
  (kratší). (Panel/feature interně dál „k doměření".)

## Hotovo v1.103 (tato session) — kratší hamburger · landscape · poprosit i pro vedení · oprava nejbližší H
- **Kratší hamburger:** dvojice tlačítek vedle sebe přes `.ctrl-row` (flex) — **Svazek+Obce**
  a **Tým+Oznámení**. Skrytý člen dvojice (např. Tým u nadmina) nechá druhého roztáhnout na
  celou šířku. Panely (`.town-panel`) přesunuty za řádek; pozicování drží (`offsetTop` je vůči
  `.ctrl`, `.ctrl-row` je static).
- **Otočení na šířku:** `manifest.json` `orientation` `portrait`→`any` (odemkne PWA). Mobilní
  layout (hamburger + spodní panely + rolovací `.ctrl`) se pouští i při nízké výšce:
  `@media (max-width:640px), (max-height:480px)` → landscape na telefonu se nerozbije.
- **„Poprosit o nahrání" i pro vedení a admina:** `flApplyRoleUI` — export vidí GIS+admin,
  poprosit vidí kdokoli KROMĚ GIS (tj. i vedoucí, i admin). Jen GIS člověk reálně nahrává.
- **Oprava chipu „nejbližší H":** zeleně nově při **vzdálenost ≤ 2× poloměr pokrytí** (kruhy se
  překrývají = rozestup OK), ne ≤ poloměr. Při poloměru 150 m = právě 300 m dle ČSN.

## Hotovo v1.102 (tato session) — GIS část A: poprosit o nahrání + počítadlo změn + export
- **Koordinace nahrávání změn do GISu.** Tlačítka podle role (hamburger neroste — každý vidí
  jen jedno): technik → **🔼 Poprosit o nahrání do GISu (N)**, GIS/Admin → **📤 Export změn (N)**.
- **Počítadlo (N)** = změny požárních H od posledního exportu (`flPendingCount`: `domereni` s
  `ts > florian_last_export`, porovnání proti `FL_EXPORT_FIELDS`, povýšení dle příznaku).
  Export uloží `florian_last_export=now` → počítadlo se vynuluje. Živě přes domereni listener.
- **Poprosit** (`flPoprositNahrani`) → push do `florian_outbox` cílený na role GIS+Admin
  (`flGisTargets`) → přes `florianNotify` dorazí správci GIS. Text: „Kdo prosí… · čeká N změn".
- Viditelnost řeší `flApplyRoleUI` (z `flApplyAdminUI`, `flSetMe`, lide listeneru). `exportBtn`
  už není admin-only (řídí ho role GIS/Admin). **Část B (import z GISu) parkuje — plán B2.**

## Hotovo v1.101 (tato session) — Revize: přepínač Termíny / ČSN v jednom tlačítku
- **Semafor Revize má dva rozměry** přepínané selektorem `#revDimSel` (Termíny/ČSN) přímo
  v tlačítku „🚦 Revize" (jako selektor metrů u Pokrytí — bez nového tlačítka, hamburger neroste).
  - **Termíny** = dosavadní datumový stav (`hydStatus`: Po termínu/Blíží se/Chybí/OK) + „⏰ Upozornit".
  - **ČSN** = stav hodnot (`csnStatus`: Nevyhovuje/Neměřeno/Vyhovuje) z `tlakDynStav`+`prutokStav`.
- Generalizace přes `revDim` + `dimStatus/dimColor/dimOrder/dimLabel` — napojeno v `iconForItem`
  (barva markeru), cluster (nejhorší stav), `applyFilter` (filtr stavu), `renderLegend` (počty/
  barvy/popisky + „Upozornit" jen u Termínů), `flRevList`, `flVisibleFireCount`. Konstanty
  `CSN_COLOR/LABEL/ORDER`. Přepnutí selektoru resetuje `revStatusFilter` a překreslí.

## Hotovo v1.100 (tato session) — role „GIS" + online jako počet s rozklikem
- **Nová role „GIS"** (`ROLE_LIST`, odznak `.r-gis` tyrkys). GIS **vidí všechna pracoviště**
  (přidán do `flIsVedeni` — jen náhled, ne admin práva). Určeno pro správce GIS, který bude
  nahrávat změny do GISu (Daniel Polák; přidán do `florian_lide` + `florian_login_email`
  přes seed workflow v `mojebudky`).
- **Online presence = počet + jména na rozklik:** horní lišta ukazuje „🟢 Online: N ▾",
  klik na `#flOnlWrap` rozbalí jména (`.onl-names`, třída `.expanded`). `flRenderOnline`
  plní počet `#flOnlCount` + jména; drží `_flOnlineList`. (Presence píše jen self-identifikované
  uživatele — kdo si nevybral „kdo jsem", se nepočítá.)
- Pozn.: rozpracováno dál (zaparkováno) — GIS „část A" (poprosit o nahrání + počítadlo +
  export), a přepínač Revize Termíny/ČSN do jednoho tlačítka (bez nafouknutí hamburgeru).

## Hotovo v1.99 (tato session) — auto-vyhodnocení průtoku dle ČSN (≥ 4 l/s)
- **Průtok se vyhodnocuje automaticky dle hodnoty** (jako tlak). Práh `PRUTOK_MIN = 4` l/s
  (ČSN 73 0873, rodinné domy / objekty do 120 m², v=0,8 m/s). `prutokStav(val)` →
  `'ok'`/`'bad'`/`''`. (ČSN je tabulka dle kategorie: RD 4 · 120–1000 m² 6 · 1000–2500 m² 9,5 ·
  >2500 m² 14 l/s při v=0,8; zvolen práh 4.)
- **Edit formulář:** ruční select „Splňuje průtok dle ČSN" → živý readout `#edCsnPauto`
  (oninput z `edProtok`), pole zčervená (`.ed-bad`). Při uložení `splnujeProtok` auto.
- **Karta:** dlaždice průtoku (`prutokTile`) zčervená + „min 4 l/s ✗" při nesplnění; pod
  hodnotou zůstává m³/h. ČSN chip v `openCard` bere i průtok z hodnoty (`_flowFail`).

## Hotovo v1.98 (tato session) — Mistr do cílení úkolů · poznámky v tisku · poznámky jen z domereni
- **Poznámky JEN z `domereni`** (uživatelské): `poznText`/`hasPozn` už neberou zdrojové
  `h.poznamka` — to je balast (64× jen číslo „35"/„58"… + pár nesmyslů „HYP"), NEjsou to
  poznámky. Radišovské poznámky jsou ve Firebase `domereni` → zobrazí se správně. **Opravuje
  chybu z v1.95**, kde se 72 zdrojových „poznámek" ukazovalo jako odznaky/štítky.
- **Poznámky v tisku mapy:** markery v `printGroup` dostanou trvalý štítek `.pozn-tip`
  (permanent tooltip) pro hydranty s poznámkou → v tisku vidět stejně jako na displeji.
- **Mistr do cílení úkolů (klient `ukolTargets`):** explicitně zařazen k „Vedoucí pracoviště"
  (úkoly za své pracoviště). Serverová část (denní přehled revizí) přidána v `mojebudky`
  (`florianRevizeCheck`, role Mistr = jako Vedoucí pracoviště) — nasazeno přes GitHub Actions.

## Hotovo v1.97 (tato session) — selektor poloměru zúžen na ČSN hodnoty 100/150/200 m
- Nabídka `#covRadius` změněna z 150/200/250/300 na **100/150/200** (default 200) — jen
  hodnoty odpovídající ČSN „vzdálenost od objektu". (Mezi hydranty = 2×: 200/300/400 m.)

## Hotovo v1.96 (tato session) — volitelný poloměr pokrytí (nyní 100/150/200 m)
- **`COVERAGE_RADIUS` je nově `let`** (dřív const) + inline `<select id="covRadius">`
  (150/200/250/300) v tlačítku „Pokrytí … m". `setCoverageRadius(r)`: `it.c.setRadius(r)` na
  hlavní kruhy + `renderMarked`/`renderCand`/`rebuildMarkersBadges` (ostatní kruhy se
  překreslují). Selektor má `stopPropagation` (klik nezapne/nevypne vrstvu). nearestHChip
  práh sladěn na `COVERAGE_RADIUS`. **Pozn.: kruh je POLOMĚR** (r), ne průměr.
  ČSN 73 0873: vzdálenost hydrantu od objektu = poloměr (100/150/200 m dle kategorie),
  mezi hydranty = dvojnásobek (200/300/400 m); běžně 150 m od objektu / 300 m mezi H, Q≥6 l/s.

## Hotovo v1.95 (tato session) — poznámky na mapě (odznak 📝 + hover + přepínač)
- **Hydranty s poznámkou** (`hasPozn(h)` = `candVal(h,'poznamka')` neprázdné — bere i živou
  editaci z `domereni` i `h.poznamka` z dat) mají **odznak 📝** (`.pozn-badge`, pravý horní
  roh, jantar; přidán do `iconForItem` do obou variant vč. revMode).
- **Hover tooltip** s textem poznámky na každém markeru s poznámkou (`applyPoznTooltips`,
  Leaflet `bindTooltip`, třída `.pozn-tip` – krémový štítek, `esc()` proti HTML injection).
- **Přepínač „📝 Poznámky"** v hamburgeru (`poznToggle`, `poznOn`) → přepne tooltipy na
  **trvalé štítky** (permanent) na mapě (viditelné po rozpadnutí clusteru / na mobilu bez hoveru).
  Rebind řeší `applyPoznTooltips()` volané i z `rebuildMarkersBadges` (živá editace poznámky).
- **Fix:** `candVal` je nově odolné vůči nenainicializovanému `domereni` (`applyPoznTooltips`
  se volá při loadu dřív, než se `domereni` naplní na ř. ~1980) — jinak skript spadl při startu.

## Hotovo v1.94 (tato session) — vzdálenost k nejbližšímu H v kartě
- **Chip „📏 nejbližší H · X m" v hlavičce karty** (vedle ČSN chipu, v požární i kandidátní).
  Vzdušná vzdálenost k nejbližšímu **požárnímu** hydrantu (přes existující `haversineM`).
  Nové `nearestFireH(h)` (min přes `HYDRANTY`, vynechá sebe), `fmtDist(m)` (m / „X,X km"),
  `nearestHChip(h)`. Barva: **≤200 m zeleně** (kruhy pokrytí 200 m se překrývají), jinak jantar.
  Pozn.: je to vzdušná čára, ne „po silnici" (ČSN doporučuje rozestup ~300 m po komunikaci).

## Hotovo v1.93 (tato session) — auto-vyhodnocení hydrodynamického tlaku (ČSN ≥0,2 MPa)
- **Hydrodynamický tlak se vyhodnocuje automaticky dle hodnoty**, ne ručním výběrem.
  Práh `TLAK_DYN_MIN = 0.2` MPa (ČSN 73 0873). Helpery `parseNum`, `tlakDynStav(val)`
  → `'ok'` (≥0,2), `'bad'` (naměřeno <0,2), `''` (neměřeno / „0" / prázdné).
- **Edit formulář:** ruční select „Splňuje tlak dle ČSN" nahrazen **živým readoutem**
  `#edCsnTauto` (aktualizuje se `oninput` z `edTlakD`): zeleně „✓ Vyhovuje (≥0,2 MPa)",
  červeně „✗ Nevyhovuje (<0,2 MPa)", pole `edTlakD` dostane `.ed-bad`. Při uložení se
  `splnujeTlak` nastaví automaticky (`'Ano'`/`'Ne'`/`''`). Průtok (`splnujeProtok`) zůstává ruční.
- **Karta:** dlaždice hydrodynamického tlaku zčervená (`.metric.bad`) + „min 0,2 MPa ✗"
  (`.mwarn`) při nesplnění (`tlakDynTile(h)`, obě karty). ČSN chip v `openCard` se řídí
  hodnotou (`_tlakFail`: naměřeno <0,2 = nevyhovuje; neměřeno = respektuj ruční `splnujeTlak`).
- **Enter u obce** nově po výběru **zavře roletku** (`panel.classList.remove('open')`).

## Hotovo v1.92 (tato session) — Enter u obce · výraznější legenda · Průtok m³/h v kartě
- **Enter potvrdí obec:** ve vyhledávání filtru obcí (`townSearch`) — když po vyfiltrování
  zbyde přesně jedna obec, Enter ji zaškrtne, aplikuje filtr a vyčistí hledání (můžeš hledat
  další). Handler `search.onkeydown` počítá viditelné `.tp-item` **jen v panelu obcí** (`panel.
  querySelectorAll`), ne globálně.
- **Legenda nadzemní/podzemní — výraznější rozlišení:** zapnutý stav modře podbarvený
  (`#dbeafe` + modrý rámeček `#1565c0`, tučné), vypnutý šedý/utlumený (`opacity:.55`,
  přeškrtnuto, grayscale symbolu). Rozdíl vidět okamžitě.
- **Karta H — průtok i v m³/h:** dlaždice průtoku ukazuje pod l/s ještě `X m³/h`
  (převod l/s × 3,6, český formát). Helper `prutokM3h()` + `m3hLine(h)`, CSS `.metric .m3h`
  (modrý podřádek s tečkovaným oddělovačem). Přidáno do požární i kandidátní karty.

## Hotovo v1.91 (tato session) — role „Mistr" + editovatelné jméno v týmu
- **Nová role „Mistr"** v `ROLE_LIST` (mezi „Vedoucí pracoviště" a „Technik"), odznak
  `.r-mistr` (růžový #fce4ec/#ad1457) v `roleCls`. Pro cílení se chová jako Technik
  (úkoly jen pro své pracoviště; **denní přehled revizí `florianRevizeCheck` na serveru
  Mistr NEDOSTÁVÁ** — kdyby měl, přidat 'Mistr' do větve „Vedoucí pracoviště" v
  `mojebudky/functions/index.js`).
- **Jméno člena týmu je nově editovatelné** přímo v panelu 👥 Tým (dřív statický text).
  `.ld-name` → flex, uvnitř `<input class="ld-name-in">`, uloží se na `change`/Enter přes
  `lideSet(pid,'jmeno',v)` (prázdné jméno se neuloží, vrátí se původní). Live listener
  `florian_lide.on('value')` panel překreslí. **Změna existujících dat (Bubák→Aleš Bubák,
  role Mistr Bubákovi i Halvovi) se dělá v appce** — Firebase data nejdou z repa.
- Seed v kódu (fallback při prázdném `florian_lide`) sladěn na `[['Aleš Bubák','Mistr'],
  ['Halva','Mistr']]` (platí jen pro čistou instalaci).

## Hotovo v1.90 (tato session) — legenda nadzemní/podzemní jsou klikací filtry typu
- **Symboly „nadzemní"/„podzemní" v legendě (vlevo dole) jsou teď přepínatelné pilulky**
  (třída `.symfilt`, stejný styl jako `.revfilt`). Klik na typ ho **skryje z mapy**, tlačítko
  zbledne (`.off` = `opacity:.42` + přeškrtnutí + `grayscale` symbolu) → poznat, že je filtr
  vyplý. Druhý klik zase zapne. Nové `typeOff={nad,pod}`; filtr přidán do `matches()`
  (`okType`, prázdný typ = podzemní jako u markeru) → propíše se i do horního počítadla,
  clusterů a fitBounds přes `applyFilter`. Reset „Všechny požární H" (`allBtn`) vrací
  `typeOff` na výchozí a překresluje legendu. Handlery se navěšují v `renderLegend`
  (`e.stopPropagation()`, pak `renderLegend()`+`applyFilter()`).

## Hotovo v1.89 (tato session) — počet „ostatních" v horním počítadle
- **Horní pill badge počítá i „ostatní hydranty"**, když je vrstva zapnutá:
  `640 hydrantů · +N ostatních`. Nové `flVisibleFireCount()` (požární dle filtrů+stavu),
  `candShownCount()` (kandidáti mimo `FIRE_IDS`, respektuje `visibleObecSet`) a
  `flRenderCount()` (skládá text). Volá se z `applyFilter`, konce `renderCand` a
  `hideCandLayers` → počet se osvěží při filtrech i zapnutí/vypnutí vrstvy.

## Hotovo v1.88 (tato session) — přejmenování „Florián II" → „Florián 2.0"
- **Brandový název všude přejmenován** na „Florián 2.0" (title, hlavička, kredit, sdílení,
  manifest `name`+`short_name`). Skloňované tvary ve větách („do Floriána", „Přihlášení do
  Floriána") ponechány — to je gramatika, ne brand. `<title>` = „Florián 2.0 – hydranty".

## Hotovo v1.87 (tato session) — nový favicon / ikony (hydrant + vlnka)
- **Vyměněny ikony** za nový design (bílý hydrant na modrém, červeno-bílá vlnka). Sada
  `icon-16/32/180/192/512.png` vygenerována ze zdroje 180×192 (192/512 lehce doostřené
  upscalem — pro ostřejší velké ikony příště dodat zdroj 512×512 / SVG). `?v=` zvednuto
  na **2** (index.html + manifest) → zlomí lepivý browser-cache faviconu v záložce.
  Ikona nainstalované PWA na ploše se u stávajících uživatelů projeví až přeinstalem.

## Hotovo v1.86 (tato session) — „k doměření" se shlukují (zelené kolečko) + cache-busting faviconu
- **„k doměření" body se teď shlukují do zeleného kolečka** (jako požární do modrého).
  `markedLayer` byl prostý `L.layerGroup` → nově `L.markerClusterGroup` s ikonou
  `.cluster.markcl` (zelená #16a34a) + odznak úkolu 🛠️ na clusteru (přes `_h` na markerech).
  Kruhy pokrytí přesunuty do samostatné `markedCovLayer` (cluster nesmí shlukovat kroužky).
  `rebuildMarkersBadges` volá `renderMarked()` i když je vrstva kandidátů vyplá (živý odznak).
- **Favicon cache-busting (příprava na výměnu ikon před rozesláním):**
  - `<link rel=icon>` má nově `icon-16/32.png?v=1`, apple-touch `icon-180.png?v=1`;
    manifest ikony `icon-192/512.png?v=1`. Do `sw.js` ASSETS přidány icon-16/32/180.
  - **Postup při výměně faviconu:** (1) nahradit PNG soubory, (2) **zvýšit `?v=` číslo**
    u všech odkazů (index.html + manifest.json), (3) bump `APP_VERSION` + `CACHE`.
    Query `?v=` zlomí lepivý browser-cache faviconu v záložce. **POZOR:** ikona už
    NAINSTALOVANÉ PWA na ploše se tím nepřekreslí — to jde jen přeinstalem (omezení PWA).

## Hotovo v1.85 (tato session) — pokrytí doměřovaných je defaultně vyplé (jen na klik)
- **Oprava:** `domCovOn` (🟢 Pokrytí doměřovaných) měl default `true`, takže se zelené
  kruhy pokrytí „k doměření" ukazovaly hned po každém načtení/aktualizaci. Default je teď
  `false` — pokrytí se zapne až kliknutím na přepínač, stejně jako „Pokrytí" u požárních.

## Hotovo v1.84 (tato session) — odznak úkolu 🛠️ i na sloučeném clusteru
- **Cluster (sloučené kolečko počtu) teď ukazuje červený odznak 🛠️**, když má aspoň
  jeden hydrant uvnitř otevřený úkol. V `iconCreateFunction` obou clusterů (požární
  `cluster` i kandidátní `candCluster`) se přes `c.getAllChildMarkers().some(m =>
  hasOpenUkol(m._h.id))` zjistí úkol a přidá `<span class="uk-badge">` (cluster div má
  nově `position:relative`, aby odznak seděl v rohu jako u jednotlivého bodu).
- Kandidátní markery v `renderCand` nově nesou `m._h=h` (dřív neměly), aby šlo v jejich
  clusteru úkol zjistit. Překreslení řeší `cluster.refreshClusters()` v `rebuildMarkersBadges`
  (volá se z `refreshUkolBadge` při změně úkolů).

## Hotovo v1.83 (tato session) — „k doměření" se filtruje jako požární H (obec i pracoviště)
- **Oprava:** vrstva označených „k doměření" (`renderMarked`) filtrovala jen podle
  pracoviště (`markInSel` → `markStred`, a i to měkce „neznámé se neschovává"), **filtr
  obce úplně ignorovala** → body svítily dál i po výběru obce. Naopak `renderCand`
  (zapnutá vrstva kandidátů) už filtroval správně přes množinu obcí viditelných požárních.
- **Sjednoceno na jeden zdroj pravdy `visibleObecSet()`** = obec-kódy požárních H, které
  projdou `matches()` (pracoviště+obec+vlastník); `null` = žádný filtr → vše. `markInSel(id,
  obecSet)` teď vrací, zda je `markObec(id)` v té množině (nová `markObec` = uložená obec →
  dohledání v KAND). Tedy „k doměření" bod se ukáže **jen když je v jeho obci vidět aspoň
  jeden požární H** — stejně jako `renderCand`.
- Použito i v `updDomCount` a `buildDomereniList` (počet i seznam „📋 K doměření"), takže
  seznam/počítadlo respektují i filtr obce. Pozor: `markInSel` se už NESMÍ předat přímo do
  `.filter(markInSel)` (index by přišel jako `obecSet`) — všude se volá `markInSel(id,_os)`.
- `markStred` ponechána (nevyužitá, ale neškodí; případně pro budoucí striktnější logiku).

## Hotovo v1.82 (tato session) — filtr stavu revize schová i „k doměření"
- **Oprava k v1.81:** filtr stavu semaforu (`revStatusFilter`) se aplikoval jen na požární
  vrstvu, ale zelené body „k doměření"/kandidáti (`renderMarked`/`renderCand`) svítily dál.
  Nově obě funkce při aktivním `revStatusFilter` vrstvu vyprázdní a nekreslí; `applyFilter`
  volá `renderMarked()` (s pojistkou na pořadí definice), takže se při přepnutí filtru
  překreslí. Po zrušení filtru se „k doměření" i kandidáti vrátí.

## Hotovo v1.81 (tato session) — klikací semafor + filtr stavu + „moje pracoviště"
- **Počty v semaforu jsou aktivní tlačítka.** V režimu 🚦 Revize se z počtů (Po termínu /
  Blíží se / Chybí / OK) staly pilulky `.revfilt`. Klik → `revStatusFilter` = daný stav →
  mapa ukáže **jen hydranty toho stavu** (v `applyFilter`: `matches(h) && hydStatus===filtr`),
  fitBounds na ně. Druhý klik / „Zavřít" filtr zruší. Počty se počítají z `matches()` (bez
  stavového filtru), takže jdou přepínat. Vypnutí semaforu filtr i seznam zruší.
- **Seznam H k danému stavu** (`flRevList` → panel `revListPanel`): nejhorší (nejvíc po termínu)
  první, každý řádek `📍 obec · Po termínu o X dní`, klik = skok na mapu + karta. Panel má „Zavřít".
- **„Moje pracoviště" podle přihlášení (měkké předvyplnění).** `flMyPracSet()` z vybraného
  jména v Týmu (`flMe`→`lide`): vedení (Admin/TŘ/PŘ) = vše; **vedoucí střediska = celé středisko
  vč. pracovišť pod ním** (přes `strediskoOf`: Vykydal MT → MT+Svitavy, Rada Polička →
  Polička+Litomyšl); ostatní = jen své pracoviště. `flApplyMyPracDefault()` (volá se po načtení
  `florian_lide` a při výběru sebe) **jednou za session** předvyplní `selectedStrediska`, pokud
  uživatel sám nefiltruje. Filtr jde kdykoli zrušit (Pracoviště→Vše nebo „Všechny požární H"),
  pak se znovu nenastaví (`flPracDefaulted`).
- Pozn.: „jen k doměření" — díky předvyplnění je seznam „📋 K doměření" i vrstva označených
  automaticky omezené na moje pracoviště (`markInSel`). Samostatný mapový přepínač „jen k
  doměření" (skrýt vše ostatní) zatím NENÍ — kandidát na příště.

## Hotovo v1.80 (tato session) — karta kandidáta v novém designu (jako požární)
- **`openCandCard` přestavěná do stejného „nového" layoutu jako `openCard`** (kompaktní
  grid `.cardgrid`/`.cg-main`/`.cg-side`): dlaždice metrik (průtok/tlaky), mřížka faktů
  `.facts`, foto + mini-mapa vedle sebe (`.media2`), úkoly ve vedlejším sloupci, akce dole.
  Zachovány kandidátní specifika: chipy (dosah/díra, k doměření, povýšeno), doměření jako
  metriky, akce Vybrat/Doměřit/Povýšit/Vrátit. Revizní pruh `.revbig` jen když má datum revize.
- **Kandidát má nově i foto** (Vyfotit/Galerie/smazat), stejně jako požární hydrant
  (`loadPhoto`/`deletePhoto`/`fbUploadFoto` jsou keyed přes `h.id`, funguje i pro kandidáty).
- **Foto funkce překreslují přes `reopenCard(h)` místo natvrdo `openCard(h)`** (`loadPhoto`,
  `deletePhoto`, cloud upload callback) — u kandidáta se tak po fotce nepřehodí na
  požární kartu; `reopenCard` vybere kartu dle `funkce`. `openCandCard` teď nastavuje `current`.
- Mini-mapa kandidáta = `buildCandMini` (oranžový přerušovaný kruh „díry" + ikona kandidáta),
  ne `buildMini` (ten kreslí modrý kruh pokrytí, což je pro kandidáta zavádějící).

## Hotovo v1.79 (tato session) — mapa omezená na oblast hydrantů (nejde odjet na Evropu)
- **Mapa se už nedá oddálit/odjet na celou Evropu.** Nová `flConstrainMap()` spočítá
  `FL_DATA_BOUNDS` = bounding box všech `HYDRANTY` rozšířený o 20 % a nastaví
  `map.setMaxBounds()` + `map.setMinZoom(getBoundsZoom(bounds))` (dál oddálit nejde).
  `L.map` má `maxBoundsViscosity:1.0` (tvrdý doraz při posunu). Přepočítá se na
  `resize` a `orientationchange` (getBoundsZoom závisí na rozměru mapy). Počáteční
  `fitBounds` je zjemnělejší (víc přiblížený) než minZoom, takže se nepere s omezením.

## Hotovo v1.78 (tato session) — klik na úkol u kandidáta konečně otevře kartu
- **Oprava: klik na úkol v seznamu „Otevřené úkoly" u „ostatního hydrantu" (kandidáta)
  nic nezobrazil.** Handler v `buildUkolyMenu` volal `_hById(hid)` a kartu otevřel jen
  `if(h)`. `_hById` hledá v `HYDRANTY` a pak v `KAND`, ale kandidáti (`kandidati.json`) se
  načítají líně (až po zapnutí vrstvy „Ostatní hydranty") → u úkolu na kandidátovi bylo
  `h==null` a panel se jen zavřel (typicky „Zkouška Tom…", „Zkouška 24.7. Jevíčko").
- **Nová `openUkolTarget(hid)`**: když bod není v `HYDRANTY` ani v načtených `KAND`,
  donačte kandidáty přes `ensureKand()` a zkusí `_hById` znovu; teprve pak `reopenCard`
  (ta sама pozná požární vs. kandidát). Když bod v datech opravdu není, srozumitelný alert.

## Hotovo v1.77 (tato session) — kruh povýšeného + reklasifikované body v mapě
- **Kruh pokrytí u povýšeného bodu už nesvítí natrvalo.** Kreslil se bezpodmínečně;
  nově se řídí přepínačem „Pokrytí" (`coverageOn`, default vyplý), stejně jako u
  ostatních požárních. `covToggle` navíc překresluje `renderMarked`/`renderCand`.
- **Reklasifikované body se nekreslí dvakrát.** Bod, který už je reálně požární v datech
  (v `HYDRANTY`), ale zůstal po něm starý `kandMarked`/`domereni.povyseno` stav (typicky
  2524 = „H7" v Chornicích po přesunu v PR #1), se ve `renderCand`/`renderMarked`
  přeskočí (`FIRE_IDS`) — kreslí ho jen hlavní vrstva. Konec duplicit, zeleného kruhu
  i „H7" odznaku. Nedestruktivní: starý stav se nemaže, jen nekreslí.
- Pozn. k exportu změn: bod už v `HYDRANTY` (reklasifikovaný v datech) není „čekající
  změna", takže v „Export změn (CSV pro GIS)" není záměrně. Povýšení kandidáta, který
  je JEŠTĚ v `kandidati.json`, se v exportu objeví (řádek „Klasifikace → požární").

## Hotovo v1.76 (tato session) — zvoneček pro všechny + oprava vykreslení povýšených
- **🔔 Oznámení – nové tlačítko v toolbaru dostupné VŠEM** (ne jen adminovi). Doteď byl
  jediný přepínač notifikací schovaný v panelu „👥 Tým", který `flApplyAdminUI()` skrývá
  ne-adminům — takže PŘ/technici neměli kde push zapnout. Nový panel `pushPanel`
  (`buildPushPanel`) nabízí „vyber sebe" + „Povolit notifikace" + „Zkušební push".
  `flPushStav()` teď píše do všech `.fl-push-stav` (funguje v obou panelech).
- **Oprava: povýšený kandidát se kreslil jako zelené „k doměření" s H-číslem.**
  `renderMarked()` (vždy viditelná vrstva) nekontrolovala `povyseno` → povýšený bod měl
  zelený symbol, zelený kruh a odznak „H7". Nově se povýšený kandidát v `renderMarked`
  kreslí jako **požární hydrant** (modrý symbol + modrý kruh, bez H-čísla), stejně jako
  v `renderCand`. `promoteCand`/`unpromoteCand` navíc překreslují i `renderMarked`.

## Hotovo v1.75 (tato session) — povýšení kandidáta jde do reportu změn
- **Povýšení kandidáta na požární se teď promítne do „📤 Export změn (CSV pro GIS)".**
  `promoteCand()` nově zapisuje `funkce='požární hydrant'`, původní klasifikaci
  (`funkcePuvodni`) a `by`/`ts`, aby povýšení mělo v reportu autora i datum.
- `flCollectExportRows()` už nebere jen požární z `HYDRANTY`, ale i **povýšené kandidáty**
  z `KAND` (`domereni[id].povyseno`). Do reportu přidá řádek
  `Klasifikace: <původní> → požární hydrant` (+ případné doměřené hodnoty prutok/tlak/…).
- `flExportZmenyCSV()` si přes `ensureKand()` dotáhne `kandidati.json`, aby povýšení
  byla v exportu i bez zapnuté vrstvy „Ostatní hydranty".
- Pozn.: appka je statická (GitHub Pages), do zdrojových `kandidati.json`/`hydranty.json`
  zapisovat neumí — „trvalá změna" = záznam v Firebase + export do GIS, odkud se
  reklasifikace přenese do zdrojových dat (jako u bodu 2524).

## Hotovo v1.74 (tato session) — reklasifikace bodu 2524
- **Přeřazen kandidát `id 2524` na požární hydrant.** Bod na `lat 49.670512 / lon 16.742473`
  (středisko Jevíčko, katastr 652725 Chornice) byl ve zdroji `kandidati.json` jako
  `funkce: "bez rozlišení"`, takže se v appce trvale tvářil jako „k doměření".
  In-app „povýšení" (`domereni[id].povyseno`) je jen runtime stav (localStorage/Firebase),
  do zdrojových dat ani do reportu změn nezasahuje — proto přeřazení muselo proběhnout
  přímo v datech: záznam odebrán z `kandidati.json` a přidán do `HYDRANTY` v `index.html`
  i do `hydranty.json` s `funkce: "požární hydrant"` (773 → 774 požárních).

## Hotovo v1.67 (tato session)
- Práh semaforu: když ho **admin** změní, uloží se i do Firebase `florian_config/rev_warn`
  (global práh pro denní notifikace). Server (florianRevizeCheck) ho odtud čte.

## Hotovo v1.66 (tato session) — KROK 1 notifikací revizí
- **Nahrání revizí do Firebase (admin):** tlačítko „☁️ Nahrát revize do cloudu"
  (`revUploadBtn`, gate `flApplyAdminUI`). `flUploadRevize()` zapíše uzel
  `florian_revize` = { id: {d:raw datum revize, s:středisko, o:obec, u:adresa, typ} }
  pro všechny hydranty. Server pak efektivní datum = `florian_domereni[id].datumRevize`
  || `florian_revize[id].d`. Podklad pro denní `florianRevizeCheck` (krok 2).
- Backend `pkobelka/mojebudky` přidán do session: `functions/index.js` má už
  `florianNotify` (push přes frontu `florian_outbox`) + scheduled `aquaUkolyCheck`
  (`every 15 minutes`) → šablona pro denní kontrolu revizí.

## Hotovo v1.65 (tato session)
- Práh semaforu: možnosti výběru **30/40/50 dní** (dřív 30/60/90/180), pojistka na
  povolené hodnoty při načtení. Sladěno s budoucími notifikacemi před koncem revize.

## Hotovo v1.64 (tato session)
- **Konkrétní dny místo „blíží se konec":** pruh revize ukazuje `revDaysText(h)` –
  „Zbývá X dní" / „Po termínu o X dní" / „Končí dnes" / „Chybí datum revize"
  (platnost revize = 365 dní). Status na vlastním řádku (nezalamuje se).
- **Nastavitelný práh v semaforu:** `REV_WARN_DAYS` je nyní `let`, uložený v
  localStorage `florian_rev_warn`. V legendě semaforu výběr 30/60/90/180 dní
  („⏰ Upozornit … dní před koncem") + dynamický popisek „Blíží se (do X dní)".

## Hotovo v1.63 (tato session)
- **Zvýrazněné datum revize:** výrazný barevný pruh `.revbig` nahoře v kartě, obarvený
  dle stavu revize (`revStatusOnly`): zelená OK, oranžová blíží se, červená po termínu,
  fialová chybí. Datum velké a tučné. Revize odebrána z chipů (aby nebyla dvakrát).

## Hotovo v1.62 (tato session)
- **Kompaktní karta hydrantu „vše v jednom okně" (bez rolování):** přestavěné
  `openCard()` do gridu `.cardgrid` (na PC dva sloupce vedle sebe, na mobilu pod
  sebou kompaktně). Podrobnosti jako sražená dvousloupcová mřížka `.facts`
  (label nad hodnotou). **Mini-mapa odstraněna** (GPS je textově; poloha je na
  hlavní mapě). **Malá fotka** (`.pimg` 96px) → klik = zvětšení přes celou obrazovku
  (`#photoZoom`, `flZoomPhoto`). Úkoly + „Přidat úkol" ve vedlejším sloupci.
  Karta `z-index` 960→1100, podložka 950→1050 (nad Leaflet ovládáním). Ověřeno
  renderem: mobil 390×844 i PC se vejdou bez rolování (malé telefony ~SE odrolují cca 94px).

## Hotovo v1.61 (tato session)
- **Hamburger 38→34 px** (ikona 16, radius 9), panel `.ctrl` posunut na `top +102`.
- **Přibližovací +/– se posadí pod hlavičku dynamicky:** `flPlaceZoom()` změří
  `.topbar` výšku a nastaví `.leaflet-top.leaflet-left` `margin-top = výška+12`.
  Volá se při načtení (rAF + 200/600/1400 ms), `resize`, `orientationchange` a při
  změně „Online" (`flRenderOnline`). Řeší přetrvávající překryv „+" přes den, i když
  se spodní lišta zalomí na víc řádků. CSS záloha zvýšena na `safe + 118px`.

## Hotovo v1.60 (tato session)
- **Oprava filtru obcí:** nová `filterTown(h)` = obec z adresy (`townKey`), jinak
  oficiální název dle kódu obce (`OBEC_NAME[h.obec]`). Použita v `matches()`,
  `buildTownFilter()`, `visibleFireTowns()`. Po sestavení `OBEC_NAME` se jednou
  překreslí filtr+mapa. Řeší **49 hydrantů bez adresy**, které dřív nešly ve filtru
  obce vybrat a jakýkoliv filtr obce je schoval (např. hydrant „mizel" při zapnuté
  obci). Ověřeno: +49 spárováno, 0 zůstalo bez obce, žádná obec ze seznamu nezmizela.

## Hotovo v1.59 (tato session)
- **Zoom „+/–" nepřekrývá hlavičku:** `.leaflet-top.leaflet-left` margin-top pevných
  88px → `calc(env(safe-area-inset-top) + 100px)` — počítá s výřezem (notch) a dvouřádkovou
  hlavičkou, takže „+" na mobilu neleze přes den/hodiny ve spodní liště.

## Hotovo v1.58 (tato session)
- **Menší hamburger** na mobilu: `.ctrl-burger` 46×46 → **38×38 px**, ikona 22→18,
  radius 12→10; panel `.ctrl` posunut `top` +116 → +106, `max-height` -180 → -170.

## Hotovo v1.57 (tato session)
- **Živé překreslení semaforu po úpravě:** po uložení editace (`edSave`) i po příchodu
  dat z Firebase (`florian_domereni` `.on`) se volá `rebuildMarkersBadges()`. Dřív se
  značka/semafor přebarvil až po reloadu appky (uživatel hlásil „hydrant nesvítil, zmizel,
  až po 3. načtení zelený").

## Hotovo v1.56 (tato session)
- **Semafor bere editované hodnoty:** `revDate()` i `hydStatus()` čtou revizi a tlaky
  přes `candVal()` (dřív četly raw `h.datumRevize`/`h.tlakStat` a editaci ignorovaly).
  → oprava „Smolná 17: zadaná revize 6/2026 se v semaforu neprojeví".
- **Export změn pro GIS (admin-only):** tlačítko „📤 Export změn (CSV pro GIS)" v panelu.
  Projde `domereni`, vybere jen **požární hydranty z GISu** (id ∈ `HYDRANTY`, kandidáti se
  vynechají) a jen ty, kde se hodnota **liší od originálu**. CSV (UTF-8 + BOM, oddělovač `;`):
  všechny identifikátory (ID, IČME, kód obce/katastru, adresa, GPS) + nové hodnoty
  editovaných polí + sloupec „Změny (staré → nové)" + kdo/kdy. `flExportZmenyCSV()`,
  `flCollectExportRows()`, `FL_EXPORT_FIELDS`. Gate přes `flApplyAdminUI` (`exportBtn`).
  Workflow: opravit ve Floriánovi → Export změn → naimportovat zpět do GISu.

## Hotovo v1.42–1.53 (poslední session)
- Značky: podzemní = modrý **ovál**; nadzemní = modrá **bublina s bílým H** (dřív červená kapka); štítek „Nadzemní" modrý.
- Odznak úkolu u hydrantu = **červené kolečko s bílým rámečkem + 🛠️** (sjednoceno s menu).
- Legenda: symbol se vejde do rámečku (`object-fit`), nepřekrývá text.
- Role rozšířeny: **Vedoucí střediska**, **Vedoucí pracoviště** (+ Admin/TŘ/PŘ/Technik). Barvy odznaků přes bezpečné třídy (`roleCls`).
- **Push hierarchie:** vedoucí střediska dostane push za celé středisko vč. podřízených pracovišť (`strediskoOf`, `ukolTargets`). Vedoucí pracoviště + technik jen své pracoviště.
- Push v popředí přes **service worker** (`flShowFgNotif` → `reg.showNotification`) — funguje i na mobilu.
- **K doměření filtr** dle vlastního `provozniStredisko` kandidáta (`markStred`/`markInSel`); body v neznámé obci se neschovávají.
- **Sync fix:** kandidáti+doměření přes `.on` (počká na přihlášení); jednorázově nahraje lokální body do cloudu (co v cloudu chybí). Vyřešilo „nula na mobilu / 8 na PC".
- Úkol bez pracoviště se v seznamu neschovává při zapnutém filtru.

## Otevřené / rozdělané (pro nový chat)
- **Notifikace před koncem revize — PŘIPRAVENO, NASADIT AŽ PŘÍŠTÍ ROK.**
  (Revize VHOS proběhnou na podzim, do té doby by funkce byla „tichá".)
  - **Hotovo a nasazené:** Firebase pravidla `florian_revize` + `florian_config`
    (zápis admin); appka (v1.66) má admin tlačítko „☁️ Nahrát revize do cloudu"
    (`flUploadRevize` → uzel `florian_revize` = {id:{d,s,o,u,typ}}); appka (v1.67)
    ukládá admin práh do `florian_config/rev_warn`. Práh **globální**, 30/40/50 dní.
  - **Napsáno, ZATÍM NENASAZENO:** denní funkce **`florianRevizeCheck`** je na větvi
    **`florian-revize-notifikace`** v `pkobelka/mojebudky` (`functions/index.js`).
    Denně 07:00, okno [0,práh], efektivní datum = `florian_domereni[id].datumRevize`
    || `florian_revize[id].d`, cílení jako úkoly (pracoviště/středisko+vedení), push
    přes `florian_outbox`→`florianNotify`, „jen jednou" přes `florian_config/rev_notified`.
  - **AKTIVACE (příští rok):** (1) admin klikne „Nahrát revize do cloudu" (až budou
    revize aktuální), (2) mergnout větev `florian-revize-notifikace` → `main` v
    `mojebudky` (Action `firebase-deploy.yml` nasadí funkci). (3) volitelně osobní
    práh / vlastní připomínka u hydrantu.
- **Export pro GIS (v1.56):** hotovo, uživatel testuje import v práci. Doladit sloupce
  dle GISu podle výsledku.
- **Úkol „Zkouška"** (bez pracoviště, neviditelný) — uživatel měl smazat konzolí na PC. Ověřit.
- Storage pravidla pro `florian/…` zpřísnit na `auth != null` (ruční, Firebase konzole) — stále TODO.
- Doplnit tým (Halva, Krombholz, Milan Horník=Vedoucí pracoviště) — přidává si uživatel sám v appce.

## Vyřešeno (dřívější otevřené body)
- ~~Smolná 17 semafor + editovaná revize~~ → **hotovo v1.56** (`revDate`/`hydStatus` přes
  `candVal`, edity jsou v `florian_domereni`, ne `florian_edits`).

## Co appka umí
- Hydranty na mapě (🔴 nadzemní / 🔵 podzemní), clustering, pokrytí 200 m (ČSN 73 0873).
- Karta hydrantu se všemi údaji, mini-mapa, foto (vyfotit/galerie), tisk A4 + tisk mapy.
- **Editace údajů** (průtok, tlaky, revize, poznámka, ČSN).
- **Semafor revizí** (po termínu / blíží se / chybí údaj / OK) — viditelný pro všechny.
- Filtry: **skupina (vlastník)**, **obce**, **pracoviště** — provázané.
- **Kandidáti / „Ostatní hydranty"** (`kandidati.json`): hledání děr v pokrytí, označení
  „k doměření", doměření hodnot, povýšení na požární. Označené body jsou v mapě **vždy
  vidět** (vrstva `markedLayer`), i když je vrstva kandidátů vypnutá.
- **Úkoly u hydrantů** (pro pracoviště) s termínem, foto (Vyfotit/Z galerie), hlasovkou
  a komentáři/diskuzí. Lišta „Uložit" je v kartě sticky (vždy vidět i s klávesnicí).
- **Tým / lidé** (tlačítko 👥 Tým): editovatelný seznam lidí s **rolí** (Admin/TŘ/PŘ/Technik)
  a **pracovištěm**. Uloženo ve Firebase `florian_lide`. Základ pro cílení úkolů a push.
  Seed při prázdném uzlu: Bubák, Halva (role Technik). Provozovatel = p.kobelka (Admin+TŘ).

## Data a ukládání
- `HYDRANTY` — požární hydranty inline v `index.html` (generováno z CSV VHOS,
  souřadnice S-JTSK/EPSG:5514 → WGS84 přes pyproj).
- `kandidati.json` — ostatní hydranty (lazy-load při zapnutí vrstvy).
- **localStorage:** `florian_photos`, `florian_edits`, `florian_domereni`, `florian_kandidati`.
- **Firebase (projekt `moje-budky`, RTDB + Storage) = sdílení mezi kolegy:**
  - RTDB: `florian_kandidati`, `florian_domereni`, `florian_foto`, `florian_ukoly`, `florian_lide`.
  - Storage: `florian/foto/…`, `florian/ukol/…`, `florian/koment/…`.
  - **Pravidla musí povolovat tyto cesty** (RTDB i Storage), jinak `PERMISSION_DENIED`.
    Teď otevřená (`if true`) — jen interní fáze.

## Push notifikace — ✅ HOTOVO a NASAZENO (klient + server)
Kompletní a živé (auto-deploy přes GitHub Actions `firebase-deploy.yml` v repu
`pkobelka/mojebudky`, běhy 18.–21. 7. 2026 „success"). **Není co dodělávat, jen otestovat.**
- **Klient (index.html):** panel `🔔 Oznámení` (`buildPushPanel`) — výběr sebe + „Povolit
  notifikace" (`flEnablePush`: povolení → FCM token přes `FL_VAPID` → uloží do
  `florian_push_tokens/<devId>`) + „Zkušební push sobě" (`flTestPush`). Vznik úkolu →
  `flSendUkolPush` → zápis do fronty `florian_outbox` (cílení `ukolTargets` = pracoviště +
  vedení). Foreground `flShowFgNotif`, background `firebase-messaging-sw.js` (scope
  `/florian/fcm/`), auto-obnova tokenu `flPushAutoRenew`.
- **Server (`mojebudky/functions/index.js`):** `florianNotify` (trigger na `florian_outbox/{id}`
  → dohledá tokeny cílů → `admin.messaging().sendEach` → čistí neplatné tokeny → označí
  `status:sent`). `florianRevizeCheck` (plánovač „every day 07:00 Europe/Prague") = denní
  přehled blížících se / prošlých revizí → zase přes `florian_outbox`.
- **DB pravidla (`mojebudky/database.rules.json`):** `florian_outbox` / `florian_push_tokens`
  zápis `auth != null`; `florian_revize` / `florian_config` zápis jen admin. **Pozor:** klient
  musí být přihlášený (Firebase Auth), jinak zápis tokenu/fronty selže → push nedorazí.

## Fáze 2 (plán, zatím neuděláno)
- Přihlášení + role: provozovatel vidí semafor a úkoly; majitel/starosta vidí jen svoje
  hydranty (skutečný stav, ne falešné OK).
- Zamknout Firebase pravidla na přihlášené uživatele.

## Zabezpečení (rozpracováno, v1.41) — přihlášení jako AquaCtrl
- **Přihlašovací brána** v `index.html`: Firebase Auth e-mailovým odkazem (passwordless),
  gate `flAuthGate` + overlay `flLoginOverlay`. Admin = ověřený claim `auth.token.admin`;
  fallback povolení přes allowlist `florian_login_email`. Data se načtou (`flStartData`)
  až po přihlášení. Admin-only sekce „Přístup (e-maily)" v panelu Tým.
- **Firebase pravidla** = repo `pkobelka/mojebudky` → `database.rules.json` (deploy Action).
  - **PR #105 (A)**: přidán `florian_login_email` (read: přihlášení, write: admin) + seed
    (`seed_florian_login_email.py`, workflow). Bezpečné mergnout kdykoli.
  - **PR #106 (B)**: zámek `florian_*` dat na `auth != null`. **Mergnout AŽ NAKONEC.**
- Sdílený Firebase `moje-budky` → email-link provider i doména `pkobelka.github.io` už
  zapnuté z AquaCtrl; secret `FIREBASE_SERVICE_ACCOUNT` je v `mojebudky`. Admin claim je
  globální (kdo je admin v AquaCtrl přes stejný e-mail, je admin i ve Floriánovi).
- **TODO ruční:** zpřísnit Firebase **Storage** pravidla pro `florian/…` na `auth != null`
  (Storage se neřídí z repa, jen v konzoli). App Check je připravený (vypnutý, prázdný key).

## Vývoj / build
- Edituje se přímo `index.html` v repu (data už jsou inline).
- Šablona + build skript (inline Leaflet/markercluster + data) jsou v pracovním scratchpadu.
- Po změně: zvýšit `APP_VERSION` + `CACHE`, commit, push do `main`.
