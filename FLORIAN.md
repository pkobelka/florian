# Florián II — poznámky k projektu (stav pro pokračování)

PWA mapa **požárních hydrantů** VHOS, a.s. Sesterská appka k AquaCtrl.
Vše v jednom `index.html` (inline CSS+JS+data+Leaflet). Hostováno na **GitHub Pages**:
https://pkobelka.github.io/florian/ · repo `pkobelka/florian`, větev `main`.

## Aktuální verze
- `APP_VERSION` v `index.html` a `CACHE` v `sw.js` — **při každém nasazení obojí zvýšit**.
- Nyní: **v1.61**, cache `florian-v68`. (Nasazuje se přes merge dev větve do `main`.)

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
- **Semafor + editovaná revize (Smolná 17):** uživatel zadal revizi 6/2026, ale semafor ji „nenajde".
  Podezření: `hydStatus(h)` čte **raw `h.datumRevize`**, ne editovanou hodnotu (edity regulárních
  hydrantů jsou v `localStorage florian_edits`, možná se do `h` nepromítnou před výpočtem stavu).
  → ověřit, jak se edity aplikují a jestli semafor/`hydStatus` bere editovaný datum revize. **Nedořešeno.**
- **Úkol „Zkouška"** (bez pracoviště, neviditelný) — uživatel měl smazat konzolí na PC
  (`_FDB.ref('florian_ukoly')…` snippet). Ověřit, že je pryč.
- Storage pravidla pro `florian/…` zpřísnit na `auth != null` (ruční, Firebase konzole) — stále TODO.
- Doplnit tým (Halva, Krombholz, Milan Horník=Vedoucí pracoviště) — přidává si uživatel sám v appce.

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
