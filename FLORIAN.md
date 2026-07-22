# Florián II — poznámky k projektu (stav pro pokračování)

PWA mapa **požárních hydrantů** VHOS, a.s. Sesterská appka k AquaCtrl.
Vše v jednom `index.html` (inline CSS+JS+data+Leaflet). Hostováno na **GitHub Pages**:
https://pkobelka.github.io/florian/ · repo `pkobelka/florian`, větev `main`.

## Aktuální verze
- `APP_VERSION` v `index.html` a `CACHE` v `sw.js` — **při každém nasazení obojí zvýšit**.
- Nyní: **v1.79**, cache `florian-v86`. (Nasazuje se přes merge dev větve do `main`.)

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

## Fáze 2 (plán, zatím neuděláno)
- Přihlášení + role: provozovatel vidí semafor a úkoly; majitel/starosta vidí jen svoje
  hydranty (skutečný stav, ne falešné OK).
- Zamknout Firebase pravidla na přihlášené uživatele.
- **Push notifikace (PC i mobil) – TODO, chce uživatel:** při založení úkolu poslat
  push vedoucímu/pracovišti (jako v AquaCtrl). Florián zatím push NEMÁ (žádné FCM).
  Postup: zkopírovat mechaniku z **AquaCtrl** (běží na stejném Firebase `moje-budky`,
  má `aquactrl_push_tokens` / `push_broadcast`) → přidat `firebase-messaging-sw.js`,
  registraci FCM tokenu + odesílání (Cloud Function / stávající backend AquaCtrl).
- Automatický e-mail/push před vypršením revize.

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
