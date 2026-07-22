const fs = require('fs');
const {
  Document, Packer, Paragraph, TextRun, ImageRun, AlignmentType,
  BorderStyle, ShadingType, Table, TableRow, TableCell, WidthType,
  VerticalAlign, HeightRule
} = require('docx');

const MM = 56.6929; // DXA per mm
const PAGE_W = Math.round(148 * MM);   // 8390
const PAGE_H = Math.round(210 * MM);   // 11905
const MARGIN = Math.round(10 * MM);    // ~567
const CONTENT_W = PAGE_W - 2 * MARGIN; // ~7256

const BLUE = '0072BC', BLUE_DARK = '005A96', RED = 'D6001C', RED_DARK = 'A80016';
const INK = '1B2733', SOFT = '5A6674', BLUESOFT = 'E9F3FB', REDSOFT = 'FDECEE', LINE = 'DBE4EC';

const logo = fs.readFileSync('logo-vhos.png');

// ---------- pomocné funkce ----------
const gap = (pts) => new Paragraph({ spacing: { after: pts * 20 }, children: [] });

function logoPara() {
  return new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after: 120 },
    children: [ new ImageRun({ type: 'png', data: logo, transformation: { width: 150, height: 45 } }) ],
  });
}

function rule() {
  return new Paragraph({
    spacing: { before: 120, after: 160 },
    border: { bottom: { color: LINE, style: BorderStyle.SINGLE, size: 6, space: 1 } },
    children: [],
  });
}

// rámeček na screen (jednobuňková tabulka s popiskem)
function screenBox(lines) {
  return new Table({
    width: { size: CONTENT_W, type: WidthType.DXA },
    columnWidths: [CONTENT_W],
    borders: {
      top:    { style: BorderStyle.DASHED, size: 8, color: BLUE },
      bottom: { style: BorderStyle.DASHED, size: 8, color: BLUE },
      left:   { style: BorderStyle.DASHED, size: 8, color: BLUE },
      right:  { style: BorderStyle.DASHED, size: 8, color: BLUE },
    },
    rows: [ new TableRow({
      height: { value: Math.round(52 * MM), rule: HeightRule.ATLEAST },
      children: [ new TableCell({
        width: { size: CONTENT_W, type: WidthType.DXA },
        shading: { type: ShadingType.CLEAR, fill: BLUESOFT },
        verticalAlign: VerticalAlign.CENTER,
        margins: { top: 200, bottom: 200, left: 200, right: 200 },
        children: lines.map((l, i) => new Paragraph({
          alignment: AlignmentType.CENTER,
          spacing: { after: i === lines.length - 1 ? 0 : 60 },
          children: [ new TextRun({ text: l.t, bold: !!l.b, italics: !!l.i, color: l.c || SOFT, size: l.s || 18 }) ],
        })),
      }) ],
    }) ],
  });
}

// kontaktní karta
function contactCard(label, num, note, urgent) {
  return new TableCell({
    width: { size: Math.round(CONTENT_W / 3), type: WidthType.DXA },
    shading: urgent ? { type: ShadingType.CLEAR, fill: REDSOFT } : undefined,
    borders: {
      top:    { style: BorderStyle.SINGLE, size: 6, color: urgent ? RED : LINE },
      bottom: { style: BorderStyle.SINGLE, size: 6, color: urgent ? RED : LINE },
      left:   { style: BorderStyle.SINGLE, size: 6, color: urgent ? RED : LINE },
      right:  { style: BorderStyle.SINGLE, size: 6, color: urgent ? RED : LINE },
    },
    margins: { top: 120, bottom: 120, left: 140, right: 140 },
    children: [
      new Paragraph({ spacing: { after: 30 }, children: [ new TextRun({ text: label, size: 15, color: SOFT, bold: true }) ] }),
      new Paragraph({ spacing: { after: 20 }, children: [ new TextRun({ text: num, size: 26, bold: true, color: urgent ? RED_DARK : BLUE_DARK }) ] }),
      new Paragraph({ children: [ new TextRun({ text: note || ' ', size: 14, color: SOFT }) ] }),
    ],
  });
}

// ---------- STRANA 1 ----------
const page1 = [
  logoPara(),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 40 },
    children: [ new TextRun({ text: 'Potřebujete nahlásit havárii?', bold: true, size: 30, color: RED_DARK }) ] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 60 },
    children: [ new TextRun({ text: 'Volejte ', size: 46, bold: true, color: INK }),
                new TextRun({ text: '722 659 171', size: 46, bold: true, color: RED_DARK }) ] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 120 },
    shading: { type: ShadingType.CLEAR, fill: RED },
    children: [ new TextRun({ text: '  NONSTOP 24/7  ', bold: true, color: 'FFFFFF', size: 22 }) ] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 40 },
    children: [ new TextRun({ text: 'Prasklé potrubí, únik vody, zápach nebo přerušená dodávka? Havarijní linka je vám k dispozici dnem i nocí.', size: 19, color: SOFT }) ] }),
  rule(),
  new Paragraph({ spacing: { after: 20 },
    children: [ new TextRun({ text: '🏘️  MOJE OBEC', bold: true, size: 32, color: BLUE_DARK }) ] }),
  new Paragraph({ spacing: { after: 120 },
    children: [ new TextRun({ text: 'Informace o vodě ve vaší obci', bold: true, size: 19, color: SOFT }) ] }),
  new Paragraph({ spacing: { after: 140 },
    children: [ new TextRun({ text: 'Na ', size: 21 }), new TextRun({ text: 'www.vhos.cz', size: 21, bold: true }),
                new TextRun({ text: ' napište název své obce (např. ', size: 21 }),
                new TextRun({ text: 'Polička – Město', size: 21, bold: true }),
                new TextRun({ text: ') a hned uvidíte vše důležité:', size: 21 }) ] }),
  screenBox([
    { t: '🖼  SEM VLOŽTE SCREEN', b: true, c: BLUE_DARK, s: 22 },
    { t: 'MOJE OBEC – vyhledávač obce (Polička…)', b: true, c: INK, s: 19 },
    { t: 'Klikněte sem → Vložit → Obrázek a nahraďte tento rámeček', i: true, s: 16 },
  ]),
  gap(6),
  new Paragraph({ spacing: { after: 120 },
    children: [ new TextRun({ text: 'Havárie   ·   Odstávky   ·   Kvalita vody   ·   Ceny   ·   Kontakty   ·   Dokumenty', bold: true, size: 19, color: BLUE_DARK }) ] }),
  new Paragraph({
    shading: { type: ShadingType.CLEAR, fill: BLUESOFT },
    border: { left: { style: BorderStyle.SINGLE, size: 18, color: BLUE, space: 6 } },
    spacing: { before: 40, after: 40 }, indent: { left: 120 },
    children: [ new TextRun({ text: '🔔  Chcete být upozorněni na havárie a plánované odstávky? Přihlaste se k odběru zpráv přímo na webu.', size: 18, color: INK }) ] }),
];

// ---------- STRANA 2 ----------
const tick = (t) => new Paragraph({ spacing: { after: 50 },
  children: [ new TextRun({ text: '✓  ', bold: true, color: BLUE }), new TextRun({ text: t, size: 21 }) ] });

const page2 = [
  logoPara(),
  new Paragraph({ spacing: { after: 20 },
    children: [ new TextRun({ text: '👤  MŮJ ÚČET', bold: true, size: 32, color: BLUE_DARK }) ] }),
  new Paragraph({ spacing: { after: 120 },
    children: [ new TextRun({ text: 'Zákaznická zóna k vašemu odběrnému místu', bold: true, size: 19, color: SOFT }) ] }),
  new Paragraph({ spacing: { after: 140 },
    children: [ new TextRun({ text: 'Po přihlášení do zákaznického servisu na ', size: 21 }),
                new TextRun({ text: 'www.vhos.cz', size: 21, bold: true }),
                new TextRun({ text: ' máte vše přehledně na jednom místě:', size: 21 }) ] }),
  screenBox([
    { t: '🖼  SEM VLOŽTE SCREEN', b: true, c: BLUE_DARK, s: 22 },
    { t: 'MŮJ ÚČET – zákaznická zóna / přihlášení', b: true, c: INK, s: 19 },
    { t: 'Klikněte sem → Vložit → Obrázek a nahraďte tento rámeček', i: true, s: 16 },
  ]),
  gap(6),
  new Table({
    width: { size: CONTENT_W, type: WidthType.DXA },
    columnWidths: [Math.round(CONTENT_W / 2), Math.round(CONTENT_W / 2)],
    borders: { top: { style: BorderStyle.NONE }, bottom: { style: BorderStyle.NONE }, left: { style: BorderStyle.NONE }, right: { style: BorderStyle.NONE }, insideHorizontal: { style: BorderStyle.NONE }, insideVertical: { style: BorderStyle.NONE } },
    rows: [ new TableRow({ children: [
      new TableCell({ width: { size: Math.round(CONTENT_W / 2), type: WidthType.DXA }, children: [ tick('Odběrná místa'), tick('Faktury'), tick('Zálohy'), tick('Platby') ] }),
      new TableCell({ width: { size: Math.round(CONTENT_W / 2), type: WidthType.DXA }, children: [ tick('Historie spotřeby'), tick('Požadavky'), tick('Aktuality') ] }),
    ] }) ],
  }),
  gap(6),
  new Paragraph({
    shading: { type: ShadingType.CLEAR, fill: BLUE },
    spacing: { before: 60, after: 20 }, indent: { left: 120, right: 120 },
    children: [ new TextRun({ text: '🏗️  Stavíte nebo rekonstruujete?', bold: true, color: 'FFFFFF', size: 21 }) ] }),
  new Paragraph({
    shading: { type: ShadingType.CLEAR, fill: BLUE },
    spacing: { after: 120 }, indent: { left: 120, right: 120 },
    children: [ new TextRun({ text: 'Vyjádření k existenci vodohospodářských sítí zařídíte online přes Vyjadřovací portál na www.vhos.cz.', color: 'FFFFFF', size: 17 }) ] }),
  rule(),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 120 },
    children: [ new TextRun({ text: 'Spojte se s námi', bold: true, size: 26, color: INK }) ] }),
  new Table({
    width: { size: CONTENT_W, type: WidthType.DXA },
    columnWidths: [Math.round(CONTENT_W/3), Math.round(CONTENT_W/3), Math.round(CONTENT_W/3)],
    borders: { insideVertical: { style: BorderStyle.NONE, size: 0, color: 'FFFFFF' } },
    rows: [ new TableRow({ children: [
      contactCard('🚨 Havarijní linka', '722 659 171', 'NONSTOP 24/7', true),
      contactCard('🏢 Zákaznické centrum', '461 357 154', ' ', false),
      contactCard('☎️ Zákaznická linka', '461 357 111', 'Po–Pá 7:00–15:00', false),
    ] }) ],
  }),
];

// ---------- DOKUMENT ----------
const doc = new Document({
  sections: [{
    properties: { page: {
      size: { width: PAGE_W, height: PAGE_H },
      margin: { top: MARGIN, bottom: MARGIN, left: MARGIN, right: MARGIN },
    } },
    children: [
      ...page1,
      new Paragraph({ children: [ new (require('docx').PageBreak)() ] }),
      ...page2,
    ],
  }],
});

Packer.toBuffer(doc).then(buf => {
  fs.writeFileSync('VHOS-letak-A5.docx', buf);
  console.log('OK VHOS-letak-A5.docx', buf.length, 'bytes');
});
