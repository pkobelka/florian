# Florián 2.0 — promo / upoutávka pro starosty

Krátká promo upoutávka (~55 s) pro aplikaci **Florián 2.0** (mapa požárních
hydrantů VHOS, a.s.). Cílovka: **starostové obcí a svazků** — proto je řeč
o jejich obci, o pokrytí dle normy a o výstupech, které se hodí na úřad.

Hotové promo je **jeden soběstačný HTML soubor**: [`florian-promo.html`](florian-promo.html).
Otevře se v prohlížeči, tlačítkem **▶ Přehrát promo** se spustí:
- kinematografické scény se **skutečnými obrazovkami appky** (přehled svazku,
  vrstva pokrytí 200 m, karta hydrantu),
- **titulky = mluvené slovo** (viz níže),
- **podkres** — jemná ambientní hudba přes Web Audio (tlačítko 🔇 ztlumí),
- vpravý dolní roh: ztlumit / přehrát znovu.

Bez internetu, bez instalace, bez cookies — vše je vložené v souboru
(obrázky jako data-URI, hudba generovaná v prohlížeči).

---

## Slovo (voiceover) — scénář po scénách

Titulky v promu jsou zkrácené. Tady je i **plná verze pro namluvení**
(hlas dabéra nebo TTS). Tón: klidný, věcný, důvěryhodný — ne reklamní křik.

| # | Scéna (obraz) | Titulek na plátně | Mluvené slovo (VO) |
|---|---|---|---|
| 1 | **Hook** — foto hydrantu, červený nádech (~7 s) | „Když hoří, počítá se každá **minuta**." | „Když hoří, počítá se každá minuta. A každý hydrant. Ví vaše obec, kde jsou, jestli mají tlak — a kdy měly poslední revizi?" |
| 2 | **Přehled** — telefon, mapa celého svazku (~9 s) | „Celý svazek. **Na jedné mapě**." | „Florián dvě nula ukáže všechny požární hydranty vaší obce i celého svazku na jediné mapě. V telefonu, kdykoli a kdekoli." |
| 3 | **Pokrytí** (hlavní) — kruhy 200 m (~10 s) | „Pokrytí dle **ČSN 73 0873**. Na první pohled." | „Kolem každého hydrantu kruh dvě stě metrů — podle normy. Kde se kruhy překrývají, je chráněno. Kde zůstane mezera, hned víte, kde hydrant chybí." |
| 4 | **Detail** — karta hydrantu (~9 s) | „Vše o hydrantu. **Na jedno ťuknutí**." | „U každého hydrantu najdete průtok, statický i dynamický tlak, datum revize, GPS i fotku z terénu. Přehledně a srozumitelně." |
| 5 | **Výstupy** — dokument do Wordu (~8 s) | „Protokol o revizi. **Rovnou do Wordu**." | „Potřebujete protokol o revizi nebo aktualizaci údajů? Vyberete obce a stáhnete hotový dokument ve Wordu — připravený k doplnění a podpisu." |
| 6 | **Hodnota** — zdarma / bez instalace / v telefonu (~7 s) | „Žádný server. Žádné náklady. **Žádné starosti**." | „Běží v prohlížeči i jako aplikace v telefonu. Bez serveru, bez nákladů, bez starostí." |
| 7 | **Závěr / CTA** — logo + odkaz (~9 s) | „Vaše hydranty **pod kontrolou**." | „Florián dvě nula. Vaše hydranty pod kontrolou." |

**Celková stopáž:** ~55 s. Odkaz v závěru: `pkobelka.github.io/florian`.

---

## Podkres (hudba)

V HTML promu hraje **generovaná ambientní hudba** (Web Audio) — klidný pad,
který u každé scény přejde do jiného akordu (Am → C → F → G → C → F → Cadd9),
lehké echo, na začátku scény jemný „ping". V závěru se ztiší.

Je to **placeholder / podkres pro náhled**. Pro finální video doporučuji
podložit licencovanou stopou v podobném duchu:
- žánr: *cinematic ambient / corporate hopeful*, tempo klidné (~70–90 BPM),
- nálada: důvěra, bezpečí, lehké napětí na začátku → uvolnění v závěru,
- zdroje bez starostí s licencí: YouTube Audio Library, Pixabay Music,
  Uppbeat, Epidemic Sound.

---

## Hotové video (MP4)

V repu je **hotové video** [`florian-promo.mp4`](florian-promo.mp4) —
1280×720, ~59 s, H.264 + AAC. Zvuk je **jen hudební podkres** (svižnější,
optimistický) — **bez mluveného slova**.

- Mluvené slovo (VO) bylo z videa vyřazeno (syntetický hlas zněl roboticky).
  **Text komentáře k namluvení zůstává v tabulce výše** — pro finální verzi
  stačí nahrát lidským hlasem (dabér) nebo prémiovým cloud TTS a podložit ho
  pod titulky/scény.
- **Podkres** je vlastní generovaná stopa; lze nahradit licencovanou hudbou.

Vzniklo z `florian-promo.html` (režim `?auto=1` = čistá úvodní karta bez
tlačítka, samospuštění) nahráním obrazovky + složením s podkresem (ffmpeg).
Stejná hudba je vložená i do HTML verze, takže sdílený odkaz zní stejně.

## Jak si video vyrobit znovu / upravit

Promo je připravené tak, aby se dalo **nahrát obrazovkou**:

1. **Nejjednodušší:** otevřít `florian-promo.html` v prohlížeči přes celou
   obrazovku (F11), spustit záznam obrazovky (Win+G / QuickTime / OBS),
   kliknout ▶ a nechat doběhnout. Zvuk z proma se nahraje s videem.
2. **Profi verze:** obraz z bodu 1 (nebo jednotlivé scény jako podklad)
   sestříhat v editoru, přidat **namluvené slovo** dle tabulky výše a
   **licencovanou hudbu** místo generovaného podkresu.
3. Formát pro rozeslání starostům: **16:9, 1080p, MP4**, do ~60 s;
   varianta na výšku (9:16) pro mobil/„stories" lze doplnit.

---

## Použité materiály

- **Reálné screeny z mobilu** (s mapovým podkladem OpenStreetMap):
  - Přehled: clustery nad celým regionem (Svitavsko / Moravskotřebovsko).
  - Pokrytí: Staré Město **bez pokrytí → s pokrytím 200 m** (before/after,
    ve scéně se obrázky střídají – ukazuje, co přepínač „🎯 Pokrytí" udělá).
  - Detail: karta hydrantu Linhartice se **skutečnou fotkou z terénu**.
  (Mapové dlaždice OSM jsou z tohoto prostředí blokované proxy, proto se
  reálné mapy braly ze screenů z telefonu.)
- Úvodní foto hydrantu: `podklady/foto-nadzemni.png`. Logo: `icon-512.png`.
- K dispozici (zatím nepoužité, na požádání doplním): protokol o revizi
  (Radišov, ČSN tabulka), pokrytí Radišov s poznámkami, foto-miniatury
  u bodů na mapě (Moravská Třebová).
- Data: 774 hydrantů, 19 vlastníků (dle `hydranty.json`).

> Poznámka: číselné údaje ve scéně „Detail" a v ukázkovém protokolu jsou
> ilustrativní hodnoty z ostrých dat jedné obce. Před veřejným nasazením
> videa doporučuji čísla přebrat, ať sedí na aktuální stav.
