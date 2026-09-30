// Snímek po snímku: render(t) → screenshot → ffmpeg (deterministické, bez časových posunů)
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const { spawn } = require('child_process');
const FPS = 30, out = process.argv[2] || 'video_noaudio.mp4', ff = process.argv[3];
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  await p.goto('file:///home/user/florian/promo/florian-hasici.html?rec=1');
  await p.waitForTimeout(800);
  const T = await p.evaluate(() => window.TOTAL);
  const n = Math.round(T * FPS);
  const f = spawn(ff, ['-y', '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'mjpeg', '-i', '-',
    '-c:v', 'libx264', '-preset', 'slow', '-crf', '20', '-pix_fmt', 'yuv420p', out], { stdio: ['pipe', 'ignore', 'inherit'] });
  for (let i = 0; i < n; i++) {
    await p.evaluate(t => window.render(t), i / FPS);
    const buf = await p.screenshot({ type: 'jpeg', quality: 93 });
    if (!f.stdin.write(buf)) await new Promise(r => f.stdin.once('drain', r));
    if (i % 150 === 0) console.log(i, '/', n);
  }
  f.stdin.end(); await new Promise(r => f.on('close', r)); await b.close(); console.log('done', T);
})();
