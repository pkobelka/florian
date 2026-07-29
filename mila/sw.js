/* Service worker pro appku Míla – jednoduchý offline režim.
   Po každé změně obsahu zvyš číslo verze v CACHE. */
const CACHE = 'mila-v2';
const ASSETS = [
  './',
  './index.html',
  './manifest.json',
  './icon-192.png',
  './icon-512.png',
  './icon-180.png'
];

self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(ASSETS)));
  self.skipWaiting();
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)))
    )
  );
  self.clients.claim();
});

self.addEventListener('fetch', e => {
  if (e.request.method !== 'GET') return;
  e.respondWith(
    caches.match(e.request).then(hit => {
      if (hit) return hit;
      return fetch(e.request).catch(() => {
        // při výpadku sítě vrať pro navigaci hlavní stránku
        if (e.request.mode === 'navigate') return caches.match('./index.html');
      });
    })
  );
});
