const assets = [
    "/",
    "/static/css/style.css",
    "/static/js/app.js",
    "/static/images/favicon.png",
    "/static/icons/icon-128x128.png",
    "/static/icons/icon-192x192.png",
    "/static/icons/icon-384x384.png",
    "/static/icons/icon-512x512.png"
];

const CATALOGUE_ASSETS = "catalogue-assets-v2";

self.addEventListener("install", (installEvent) => {
    installEvent.waitUntil(
        caches.open(CATALOGUE_ASSETS)
            .then((cache) => cache.addAll(assets))
            .then(() => self.skipWaiting())
    );
});

self.addEventListener("activate", (event) => {
    event.waitUntil(
        caches.keys().then((keyList) =>
            Promise.all(
                keyList.map((key) => {
                    if (key !== CATALOGUE_ASSETS) {
                        return caches.delete(key);
                    }
                })
            )
        ).then(() => self.clients.claim())
    );
});

self.addEventListener("fetch", (event) => {
    event.respondWith(
        fetch(event.request).catch(() => caches.match(event.request))
    );
});