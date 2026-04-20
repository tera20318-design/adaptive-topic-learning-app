/**
 * Service Worker - network-first with cache fallback
 * Latest pages are preferred so mobile devices do not get stuck on old UI.
 */

const CACHE_NAME = 'quiz-app-v5';
const ASSETS = [
  './',
  './first-pdf.html',
  './index.html',
  './style.css',
  './app.js',
  './questions-first-pdf.json',
  './questions.json',
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => cache.addAll(ASSETS))
  );
  self.skipWaiting();
});

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(key => key !== CACHE_NAME).map(key => caches.delete(key)))
    )
  );
  self.clients.claim();
});

self.addEventListener('fetch', event => {
  if (event.request.method !== 'GET') return;
  if (!event.request.url.startsWith('http')) return;

  const request = event.request;
  const url = new URL(request.url);
  if (url.origin !== self.location.origin) return;

  event.respondWith(
    fetch(request)
      .then(response => {
        if (response && response.ok) {
          const clone = response.clone();
          caches.open(CACHE_NAME).then(cache => cache.put(request, clone));
        }
        return response;
      })
      .catch(async () => {
        const cached = await caches.match(request);
        if (cached) return cached;
        if (request.destination === 'document') {
          return caches.match('./index.html');
        }
        throw new Error('Network failed and no cached response was available');
      })
  );
});
