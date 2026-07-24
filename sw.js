// Florián – samostatný service worker pro /florian/
// Účel: vlastní scope (oddělení od dalších PWA) a instalace na plochu.
const CACHE = 'florian-v114';
const ASSETS = [
  './',
  './index.html',
  './manifest.json',
  './icon-16.png',
  './icon-32.png',
  './icon-180.png',
  './icon-192.png',
  './icon-512.png',
  './kandidati.json'
];

self.addEventListener('install', (e) => {
  self.skipWaiting();
  e.waitUntil(caches.open(CACHE).then((c) => c.addAll(ASSETS).catch(() => {})));
});

self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys().then((ks) => Promise.all(ks.filter((k) => k !== CACHE).map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

// Network-first, fallback do cache (pro offline náhled)
self.addEventListener('fetch', (e) => {
  if (e.request.method !== 'GET') return;
  e.respondWith(
    fetch(e.request)
      .then((r) => {
        const copy = r.clone();
        caches.open(CACHE).then((c) => c.put(e.request, copy)).catch(() => {});
        return r;
      })
      .catch(() => caches.match(e.request))
  );
});
