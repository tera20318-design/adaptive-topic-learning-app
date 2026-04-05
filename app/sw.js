/**
 * Service Worker - オフライン対応 & キャッシュ
 */

const CACHE_NAME = 'quiz-app-v1';
const ASSETS = [
  './',
  './index.html',
  './style.css',
  './app.js',
  './questions.json',
];

// インストール時にキャッシュ
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => {
      return cache.addAll(ASSETS).catch(err => {
        console.warn('キャッシュ追加失敗 (一部ファイルが存在しない可能性):', err);
      });
    })
  );
  self.skipWaiting();
});

// 古いキャッシュを削除
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(
        keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k))
      )
    )
  );
  self.clients.claim();
});

// フェッチ: キャッシュファースト、なければネットワーク
self.addEventListener('fetch', event => {
  // chrome-extension などは無視
  if (!event.request.url.startsWith('http')) return;

  event.respondWith(
    caches.match(event.request).then(cached => {
      if (cached) return cached;
      return fetch(event.request).then(response => {
        // 成功したレスポンスはキャッシュに追加
        if (response && response.status === 200) {
          const clone = response.clone();
          caches.open(CACHE_NAME).then(cache => cache.put(event.request, clone));
        }
        return response;
      }).catch(() => {
        // オフライン時
        if (event.request.destination === 'document') {
          return caches.match('./index.html');
        }
      });
    })
  );
});
