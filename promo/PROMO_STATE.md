# Promo Florián 2.0 — stav projektu (pro pokračování)

Krátký přehled, ať se dá příště rychle navázat. Poslední aktualizace: 29. 9. 2026 (v2 – nové značky hydrantů, scéna Pro hasiče).

## Co je hotovo a nasazeno
- **Promo video** (70 s, 1280×720, H.264+AAC, jen hudba, bez mluveného slova):
  `promo/florian-promo.mp4`
- **Přehrávač** (soběstačné HTML, hudba vložená jako MP3, before/after pokrytí):
  `promo/florian-promo.html`
- **Scénář / VO texty / postup**: `promo/scenar.md`
- **Živé veřejné odkazy** (GitHub Pages, bez přihlášení):
  - Video: https://pkobelka.github.io/florian/promo/florian-promo.mp4
  - Přehrávač: https://pkobelka.github.io/florian/promo/florian-promo.html
- **Stránka s videem pro mobil + sdílení**: `promo/video.html` – nativní `<video>` s MP4
  (přehraje se i na výšku), tlačítka Sdílet (Web Share API: na mobilu pošle rovnou soubor,
  jinak odkaz), WhatsApp, Facebook, Kopírovat odkaz, Stáhnout; OG tagy pro náhled odkazu.
  Animace `florian-promo.html` je jen pro PC – v portrétu je z 16:9 scény nečitelný proužek.
  - Stránka: https://pkobelka.github.io/florian/promo/video.html
- **V appce**: tlačítko **🎬 Promo video** vedle „📤 Sdílet appku“ (admin-only,
  `promoBtn` v `index.html`, řízeno `flApplyAdminUI`) – otevírá `promo/video.html`.

## Scény promo (8) – verze 2 (29. 9. 2026)
1. Hook — foto hydrantu, „Když hoří, počítá se každá minuta.“ (7 s)
2. Přehled — mapa regionu s clustery, nová legenda nadz./podz. (9 s), 775 hydrantů.
3. Pokrytí (hero) — **Biskupice** před/po (bez pokrytí → kruhy 200 m); vybráno z dat tak,
   aby kruhy nesplývaly do jednoho fleku (medián vzdálenosti sousedů ~190 m). (10,5 s)
4. Detail — karta Jevíčko HN6 s fotkou, štítek „1189 l/min · 71,3 m³/h“. (9 s)
5. Protokol — reálný protokol VHOS, „↓ .doc“ + Word. (8 s)
6. Hodnota — „Aplikace zdarma · Bez instalace · Mobil, tablet i PC“. (7 s)
7. **Pro hasiče** — „Při zásahu. Nejbližší hydrant za pár vteřin.“ Telefon střídá 4 obrazovky
   (seznam nejbližších → okno HN1 → trasa Mapy.com → navigace), 12 s = 5 taktů hudby.
8. Závěr — „Vaše hydranty pod kontrolou.“, „…pro obce, svazky i jednotky hasičů“.
- Všechny screenshoty v2 jsou z mobilu uživatele (nové kruhové značky dle normy).
- Pořadí dle uživatele: provoz → majitel → hasiči → závěr.

## Jak se promo staví (pipeline, vše v scratchpadu session)
**v2 (29. 9. 2026):** skripty `build.py` (nahradí data-URI obrázků/zvuku v HTML v1 + přidá scénu
a texty), `record.js` (Playwright recordVideo `?auto=1`). Nahrávka z headless Chromia běží ~13 %
pomaleji než reálný čas → časování srovnáno po úsecích (`setpts` s kotvami na přechodech scén,
detekce přechodů z rozdílu snímků). Hudba = zvuk z v1 MP4 prodloužený o 12 s smyčkou z detailové
scény (G), střihy **na dobách** (mřížka 0,3 s, takt 2,4 s, fáze x.09) a prolnutí qsin 1,2 s –
střihy mimo dobu „sekaly“. Scéna vložená do hudby musí mít délku násobku 2,4 s.
**Hudba v2 = nově generovaná** (`promo/music_v2.py`, numpy → WAV): stříhání hudby v1 vždy
zanechalo slyšitelné přeskoky (každá scéna v1 má vlastní frázi a doznění). v2: souvislé arpeggio
(krok 0,3 s, takt 2,4 s), pad + basa, akord na scénu (Em, C, G, D, Em, C, D, G), hranice scén v `B`
(čas videa, scény od 1,05 s). Závěrečný akord a doznění jen v závěru. Hlasitost ≈ v1 (−15 LUFS).
Při změně délek scén upravit `B` a znovu vygenerovat. Do HTML přehrávače jde stopa od 1,05 s
(tam hudba startuje s první scénou).

Zdroje jsou v session scratchpadu (ne v repu): `build.py` (generuje HTML z `assets.json`),
`record.js` (nahraje HTML `?auto=1` přes Playwright → webm), `music_only.py` (hudba),
`build_audio.py` (verze s VO – nepoužitá). ffmpeg = imageio-ffmpeg (libx264/aac).
Postup: uprav `build.py` → `python3 build.py` → `node record.js` → zjisti začátek (bílý flash)
→ ffmpeg mux (`-ss <start> -t 58.6` + `music_only.wav`, fade in/out) → `promo/florian-promo.mp4`.
HTML má vloženou stopu `html_audio.mp3` (data-URI) přes placeholder `__AUDIO__`.
Assety (obrázky, logo, VHOS, protokol, audio) jsou base64 v `assets.json`.
> Pozn.: scratchpad je dočasný. Pro plnou reprodukci případně znovu vytvořit z těchto poznámek.

## Promo „Florián pro hasiče“ (30. 9. 2026)
- **Video** 53 s (s úvodním titulkem 4,8 s), 1920×1080 (16:9 – hasiči mají tablet na šířku), jen hudba: `promo/florian-hasici.mp4`
- **Přehrávač** (soběstačné HTML, hudba vložená): `promo/florian-hasici.html`
- **Stránka pro sdílení**: `promo/video-hasici.html` (kopie `video.html` s texty pro hasiče)
- Scény: Hook „Kde je nejbližší hydrant?“ (4,8) → Nejbližší hydranty na tabletu (9,6) → rychlá karta HN6
  (7,2) → celá karta (7,2) → navigace (9,6) → závěr + odkaz `?rezim=H` (9,6). Délky = násobky taktu 2,4 s.
- Screenshoty: tablet v režimu H (Jevíčko, HN6); navigace zatím z mobilu (Mapy.com). Připraveno i na
  tabletové screeny `t4` (trasa Mapy.com), `t5` (satelit + „Vést sem“) a `t6` (Foto na satelitu) –
  `build.py` je použije, když jsou v `assets/`, a přidá scénu „Poznáte ho i v noci“.
- **Pipeline (nová, deterministická)**: zdroje v `promo/src-hasici/` (šablona `hasici_src.html`,
  `build.py`, `render.js`). Animace řídí JS funkce `render(t)` (žádné CSS animace) → `render.js`
  vykreslí snímek po snímku (30 fps) přes Playwright a pošle do ffmpeg – žádné dorovnávání časování.
  Hudba `promo/music_hasici.py <délky scén>` (odvozeno z music_v2.py). Přehrávač bere čas ze zvukové stopy.
  Postup: assety (a10 logo, a12 VHOS, a08/a09 navigace z v1 HTML, t1–t3 screeny, hydrant.jpg) do
  `assets/` → `python3 build.py` → `python3 music_hasici.py $(cat durs.txt)` → wav → mp3 `html_audio.mp3`
  → `python3 build.py` → `node render.js video_noaudio.mp4 <ffmpeg>` → mux s wav (crf 24, fade out).

## Prostředí / omezení
- Proxy blokuje externí web (OSM dlaždice, HuggingFace, mojebudky.cz, github.io → 403 zevnitř).
  Proto: reálné mapy = screeny z mobilu; neuronové TTS nedostupné (jen offline espeak/MBROLA → zahozeno).
- Povolené jen balíčkové servery (pip/npm). ffmpeg přes `pip install imageio-ffmpeg`.
- Deploy: GitHub Pages servíruje z větve `main`. Vývoj na `claude/florian-promo-video-yqc5qt`,
  pak merge do `main` (a `git fetch`/reset před merge, main se hýbe kvůli jiné práci).

## Otevřené / na rozmyšlenou
- **Soukromí protokolu**: ve scéně 5 je reálné jméno „Miroslav Novotný“ a podpis (Radišov).
  Pro veřejnou reklamu zvážit anonymizovaný vzor.
- Volitelně: tlačítko „Promo video“ zpřístupnit všem (teď jen admin) / odkaz vést na MP4 místo přehrávače.
- Volitelně: verze **9:16** na mobil; verze s **namluveným slovem** (lidský hlas / cloud TTS mimo toto prostředí).
- **Další projekt**: promo pro **mojebudky.cz** ve stejném stylu — čeká na podklady
  (screeny, popis, logo/barvy, slogan) od uživatele.
