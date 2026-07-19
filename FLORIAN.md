# Florián II — poznámky k projektu (stav pro pokračování)

PWA mapa **požárních hydrantů** VHOS, a.s. Sesterská appka k AquaCtrl.
Vše v jednom `index.html` (inline CSS+JS+data+Leaflet). Hostováno na **GitHub Pages**:
https://pkobelka.github.io/florian/ · repo `pkobelka/florian`, větev `main`.

## Aktuální verze
- `APP_VERSION` v `index.html` a `CACHE` v `sw.js` — **při každém nasazení obojí zvýšit**.
- Nyní: **v1.41**, cache `florian-v48`.

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
