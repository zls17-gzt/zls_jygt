const CACHE_NAME = 'jiayuan-v12'
const ASSETS = ['./', './index.html', './manifest.json',
                './icon-192.png', './icon-512.png',
                './icons/mascot.png', './icons/eat.png', './icons/work.png',
                './icons/sport.png', './icons/briefcase.png', './icons/flower.png',
                './icons/drink.png', './icons/rest.png', './icons/card.png']
// 安装：逐个缓存，单个失败不拖垮整体
self.addEventListener('install', (e) => {
  e.waitUntil(
    caches.open(CACHE_NAME).then(cache =>
      Promise.allSettled(ASSETS.map(url => cache.add(url)))
    ).then(() => self.skipWaiting())
  )
})
// 激活：清理旧版本缓存（改代码后必须升级v1→v2，用户才能拿到新版）
self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k)))
    ).then(() => self.clients.claim())
  )
})
// 拦截请求：缓存优先，缓存没有才上网（离线可用的关键）
self.addEventListener('fetch', (e) => {
  if (e.request.method !== 'GET') return
  e.respondWith(
    caches.match(e.request).then(hit =>
      hit || fetch(e.request).then(res => {
        const copy = res.clone()
        caches.open(CACHE_NAME).then(c => c.put(e.request, copy))
        return res
      }).catch(() => caches.match('./index.html'))
    )
  )
})
