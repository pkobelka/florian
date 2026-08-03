# Promo Florián 2.0 — stav projektu (pro pokračování)

Krátký přehled, ať se dá příště rychle navázat. Poslední aktualizace: srpen 2026.

## Co je hotovo a nasazeno
- **Promo video** (~59 s, 1280×720, H.264+AAC, jen hudba, bez mluveného slova):
  `promo/florian-promo.mp4`
- **Přehrávač** (soběstačné HTML, hudba vložená jako MP3, before/after pokrytí):
  `promo/florian-promo.html`
- **Scénář / VO texty / postup**: `promo/scenar.md`
- **Živé veřejné odkazy** (GitHub Pages, bez přihlášení):
  - Video: https://pkobelka.github.io/florian/promo/florian-promo.mp4
  - Přehrávač: https://pkobelka.github.io/florian/promo/florian-promo.html
- **V appce**: tlačítko **🎬 Promo video** vedle „📤 Sdílet appku“ (admin-only,
  `promoBtn` v `index.html`, řízeno `flApplyAdminUI`). App verze **1.172**, sw `florian-v179`.

## Scény promo (7)
1. Hook — foto hydrantu, „Když hoří, počítá se každá minuta.“
2. Přehled — reálná mapa regionu s clustery (screen z mobilu).
3. Pokrytí (hero) — Staré Město **before/after** (bez pokrytí → s kruhy 200 m), ČSN 73 0873.
4. Detail — reálná karta hydrantu Linhartice se skutečnou fotkou.
5. Protokol — **reálný úřední protokol VHOS** (PDF vzor od uživatele), štítek „↓ .doc“ + Word.
6. Hodnota — „Aplikace zdarma · Bez instalace · Mobil, tablet i PC“.
7. Závěr — „Vaše hydranty pod kontrolou.“, odkaz, „…sesterská appka k AQUACtrl“.
- Trvalý branding v každé scéně: logo **Florián + VHOS** (vlevo nahoře), na úvodu „APLIKACE OD [VHOS]“.

## Jak se promo staví (pipeline, vše v scratchpadu session)
Zdroje jsou v session scratchpadu (ne v repu): `build.py` (generuje HTML z `assets.json`),
`record.js` (nahraje HTML `?auto=1` přes Playwright → webm), `music_only.py` (hudba),
`build_audio.py` (verze s VO – nepoužitá). ffmpeg = imageio-ffmpeg (libx264/aac).
Postup: uprav `build.py` → `python3 build.py` → `node record.js` → zjisti začátek (bílý flash)
→ ffmpeg mux (`-ss <start> -t 58.6` + `music_only.wav`, fade in/out) → `promo/florian-promo.mp4`.
HTML má vloženou stopu `html_audio.mp3` (data-URI) přes placeholder `__AUDIO__`.
Assety (obrázky, logo, VHOS, protokol, audio) jsou base64 v `assets.json`.
> Pozn.: scratchpad je dočasný. Pro plnou reprodukci případně znovu vytvořit z těchto poznámek.

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
