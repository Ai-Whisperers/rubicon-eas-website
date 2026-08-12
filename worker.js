addEventListener("fetch", event => {
  event.respondWith(handle(event.request));
});

const FILES = {
    "index.html": "https://9eb1832f3e42a1dbd6ba854f8d6a1cb2.r2.cloudflarestorage.com/ai-whisperers-backups/rubicon-eas/index.html?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=ce41cee6154fcf0bf1f9be848dffcd20%2F20260810%2Fauto%2Fs3%2Faws4_request&X-Amz-Date=20260810T230746Z&X-Amz-Expires=604800&X-Amz-SignedHeaders=host&X-Amz-Signature=0c65c407a8ae993e1ccedb293c20ea6163e355e43e3d621d6a2fc3254dca8a71",
    "derecho-civil.html": "https://9eb1832f3e42a1dbd6ba854f8d6a1cb2.r2.cloudflarestorage.com/ai-whisperers-backups/rubicon-eas/derecho-civil.html?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=ce41cee6154fcf0bf1f9be848dffcd20%2F20260810%2Fauto%2Fs3%2Faws4_request&X-Amz-Date=20260810T230746Z&X-Amz-Expires=604800&X-Amz-SignedHeaders=host&X-Amz-Signature=d5fa8f276532eea5519977e540bcf53963d461de63968ba2f09ae6d726f2dbd7",
    "derecho-penal.html": "https://9eb1832f3e42a1dbd6ba854f8d6a1cb2.r2.cloudflarestorage.com/ai-whisperers-backups/rubicon-eas/derecho-penal.html?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=ce41cee6154fcf0bf1f9be848dffcd20%2F20260810%2Fauto%2Fs3%2Faws4_request&X-Amz-Date=20260810T230746Z&X-Amz-Expires=604800&X-Amz-SignedHeaders=host&X-Amz-Signature=2a20a62869c7c3648e44eea0c390b6dab41cb034b905034dd0b0a1c18409404f",
    "derecho-ambiental.html": "https://9eb1832f3e42a1dbd6ba854f8d6a1cb2.r2.cloudflarestorage.com/ai-whisperers-backups/rubicon-eas/derecho-ambiental.html?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=ce41cee6154fcf0bf1f9be848dffcd20%2F20260810%2Fauto%2Fs3%2Faws4_request&X-Amz-Date=20260810T230747Z&X-Amz-Expires=604800&X-Amz-SignedHeaders=host&X-Amz-Signature=ec50d5fb0168a0e0bf320448f162f3edc4b393857d1c41a75d154be8ba275dc9",
    "nosotros.html": "https://9eb1832f3e42a1dbd6ba854f8d6a1cb2.r2.cloudflarestorage.com/ai-whisperers-backups/rubicon-eas/nosotros.html?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=ce41cee6154fcf0bf1f9be848dffcd20%2F20260810%2Fauto%2Fs3%2Faws4_request&X-Amz-Date=20260810T230747Z&X-Amz-Expires=604800&X-Amz-SignedHeaders=host&X-Amz-Signature=c15da956ea9797d251a9f1f83d87b70a1cfb975698979366969cb0c48a214c7f",
    "casos.html": "https://9eb1832f3e42a1dbd6ba854f8d6a1cb2.r2.cloudflarestorage.com/ai-whisperers-backups/rubicon-eas/casos.html?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=ce41cee6154fcf0bf1f9be848dffcd20%2F20260810%2Fauto%2Fs3%2Faws4_request&X-Amz-Date=20260810T230747Z&X-Amz-Expires=604800&X-Amz-SignedHeaders=host&X-Amz-Signature=cf2dbf71fca2770b2b867fe049cf473d8dcbb6d84fa25c5b99ab2e47cf55a21a",
    "contacto.html": "https://9eb1832f3e42a1dbd6ba854f8d6a1cb2.r2.cloudflarestorage.com/ai-whisperers-backups/rubicon-eas/contacto.html?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=ce41cee6154fcf0bf1f9be848dffcd20%2F20260810%2Fauto%2Fs3%2Faws4_request&X-Amz-Date=20260810T230747Z&X-Amz-Expires=604800&X-Amz-SignedHeaders=host&X-Amz-Signature=413cf1904968a15d6070d57913b150251413f8293703b7c18fc59ed86cdafed3",
    "blog.html": "https://9eb1832f3e42a1dbd6ba854f8d6a1cb2.r2.cloudflarestorage.com/ai-whisperers-backups/rubicon-eas/blog.html?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=ce41cee6154fcf0bf1f9be848dffcd20%2F20260810%2Fauto%2Fs3%2Faws4_request&X-Amz-Date=20260810T230747Z&X-Amz-Expires=604800&X-Amz-SignedHeaders=host&X-Amz-Signature=d994d903c40ed178fed97770b64e5bc38576b840a85f50f54098dbf2324c358c",
    "assets/styles.css": "https://9eb1832f3e42a1dbd6ba854f8d6a1cb2.r2.cloudflarestorage.com/ai-whisperers-backups/rubicon-eas/assets/styles.css?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=ce41cee6154fcf0bf1f9be848dffcd20%2F20260810%2Fauto%2Fs3%2Faws4_request&X-Amz-Date=20260810T230748Z&X-Amz-Expires=604800&X-Amz-SignedHeaders=host&X-Amz-Signature=16976940b4c9cd2107e74ebb7a8c29ca12e40d8dc2efff14ce01a1ae042a4b59",
    "assets/main.js": "https://9eb1832f3e42a1dbd6ba854f8d6a1cb2.r2.cloudflarestorage.com/ai-whisperers-backups/rubicon-eas/assets/main.js?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=ce41cee6154fcf0bf1f9be848dffcd20%2F20260810%2Fauto%2Fs3%2Faws4_request&X-Amz-Date=20260810T230748Z&X-Amz-Expires=604800&X-Amz-SignedHeaders=host&X-Amz-Signature=418df2341d2caa6ae6938c89acd0d6bb5258ae5906d0daee3852e83c5866c1b7",
    "assets/content.es.json": "https://9eb1832f3e42a1dbd6ba854f8d6a1cb2.r2.cloudflarestorage.com/ai-whisperers-backups/rubicon-eas/assets/content.es.json?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=ce41cee6154fcf0bf1f9be848dffcd20%2F20260810%2Fauto%2Fs3%2Faws4_request&X-Amz-Date=20260810T230748Z&X-Amz-Expires=604800&X-Amz-SignedHeaders=host&X-Amz-Signature=1d96c6f7ca0ded4c4229048c39487888ebbb234a896906bf335e84264f674058",
    "admin.html": "https://9eb1832f3e42a1dbd6ba854f8d6a1cb2.r2.cloudflarestorage.com/ai-whisperers-backups/rubicon-eas/admin.html?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=ce41cee6154fcf0bf1f9be848dffcd20%2F20260810%2Fauto%2Fs3%2Faws4_request&X-Amz-Date=20260810T232448Z&X-Amz-Expires=604800&X-Amz-SignedHeaders=host&X-Amz-Signature=9c1cab8f262b57c31692c652653d621c958bd83398c4283f3301f2666aa18143",
    "assets/schema.js": "https://9eb1832f3e42a1dbd6ba854f8d6a1cb2.r2.cloudflarestorage.com/ai-whisperers-backups/rubicon-eas/assets/schema.js?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=ce41cee6154fcf0bf1f9be848dffcd20%2F20260810%2Fauto%2Fs3%2Faws4_request&X-Amz-Date=20260810T235657Z&X-Amz-Expires=604800&X-Amz-SignedHeaders=host&X-Amz-Signature=e2b034e9454c0aaf9da5284d7167cf44df8ae93417c550722afbd058ab28af63",
    "sitemap.xml": "https://9eb1832f3e42a1dbd6ba854f8d6a1cb2.r2.cloudflarestorage.com/ai-whisperers-backups/rubicon-eas/sitemap.xml?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=ce41cee6154fcf0bf1f9be848dffcd20%2F20260810%2Fauto%2Fs3%2Faws4_request&X-Amz-Date=20260810T235657Z&X-Amz-Expires=604800&X-Amz-SignedHeaders=host&X-Amz-Signature=b1a65d16da5a8ddeadbbbc8f67100df1a5c5598c78b833e2873039474228b34e",
    "robots.txt": "https://9eb1832f3e42a1dbd6ba854f8d6a1cb2.r2.cloudflarestorage.com/ai-whisperers-backups/rubicon-eas/robots.txt?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=ce41cee6154fcf0bf1f9be848dffcd20%2F20260810%2Fauto%2Fs3%2Faws4_request&X-Amz-Date=20260810T235657Z&X-Amz-Expires=604800&X-Amz-SignedHeaders=host&X-Amz-Signature=41e184b062f010bba0d6f801b8257d233e0fb600021d1b03ca893fbc01adf1f6",
    "red-colegas.html": "https://9eb1832f3e42a1dbd6ba854f8d6a1cb2.r2.cloudflarestorage.com/ai-whisperers-backups/rubicon-eas/red-colegas.html?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=ce41cee6154fcf0bf1f9be848dffcd20%2F20260812%2Fauto%2Fs3%2Faws4_request&X-Amz-Date=20260812T175704Z&X-Amz-Expires=604800&X-Amz-SignedHeaders=host&X-Amz-Signature=02fd778e712594d5e7db06e1d7839bb145f85a54e071fdc37d493c682f5eec7e"
};

function guessCT(path) {
  if (path.endsWith(".html")) return "text/html; charset=utf-8";
  if (path.endsWith(".css")) return "text/css; charset=utf-8";
  if (path.endsWith(".js")) return "application/javascript; charset=utf-8";
  if (path.endsWith(".json")) return "application/json; charset=utf-8";
  if (path.endsWith(".xml")) return "application/xml; charset=utf-8";
  if (path.endsWith(".txt")) return "text/plain; charset=utf-8";
  return "application/octet-stream";
}

async function handle(request) {
  const url = new URL(request.url);
  const path = url.pathname;

  let key = path.replace(/^\//, "");
  if (key === "") key = "index.html";

  for (const candidate of [key, key + ".html"]) {
    if (FILES[candidate]) {
      try {
        const resp = await fetch(FILES[candidate], {
          cf: { cacheTtl: 60, cacheEverything: true }
        });
        return new Response(await resp.text(), {
          headers: {
            "Content-Type": guessCT(candidate),
            "Cache-Control": "public, max-age=60"
          }
        });
      } catch (e) {
        return new Response("Upstream error: " + e.message, { status: 502 });
      }
    }
  }

  return new Response("Not found: " + path, { status: 404 });
}
