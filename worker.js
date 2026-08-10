addEventListener("fetch", event => {
  event.respondWith(handle(event.request));
});

const FILES = {
  "derecho-civil.html": "https://9eb1832f3e42a1dbd6ba854f8d6a1cb2.r2.cloudflarestorage.com/ai-whisperers-backups/rubicon-eas/derecho-civil.html?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=${R2_ACCESS_KEY_ID}%2F20260810%2Fauto%2Fs3%2Faws4_request&X-Amz-Date=20260810T205245Z&X-Amz-Expires=604800&X-Amz-SignedHeaders=host&X-Amz-Signature=1e6f17ae19e5e7c7dea2c2fe5e150b2be3f5e45d3e1ac86d3714cff44a2e37c7",
  "casos.html": "https://9eb1832f3e42a1dbd6ba854f8d6a1cb2.r2.cloudflarestorage.com/ai-whisperers-backups/rubicon-eas/casos.html?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=${R2_ACCESS_KEY_ID}%2F20260810%2Fauto%2Fs3%2Faws4_request&X-Amz-Date=20260810T205245Z&X-Amz-Expires=604800&X-Amz-SignedHeaders=host&X-Amz-Signature=4f3e4bdf2b902c506d8e6ef3553a8967dfd4adc9ebe44c0a4a16977c21f2a0da",
  "derecho-ambiental.html": "https://9eb1832f3e42a1dbd6ba854f8d6a1cb2.r2.cloudflarestorage.com/ai-whisperers-backups/rubicon-eas/derecho-ambiental.html?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=${R2_ACCESS_KEY_ID}%2F20260810%2Fauto%2Fs3%2Faws4_request&X-Amz-Date=20260810T205245Z&X-Amz-Expires=604800&X-Amz-SignedHeaders=host&X-Amz-Signature=cd9304f72e65bdbdf9080936f7453f8639d3537a3ae59f2c125c244cc42af988",
  "index.html": "https://9eb1832f3e42a1dbd6ba854f8d6a1cb2.r2.cloudflarestorage.com/ai-whisperers-backups/rubicon-eas/index.html?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=${R2_ACCESS_KEY_ID}%2F20260810%2Fauto%2Fs3%2Faws4_request&X-Amz-Date=20260810T205245Z&X-Amz-Expires=604800&X-Amz-SignedHeaders=host&X-Amz-Signature=906f1323943bf292f42810a4ac3e8e8ca402dc3f0fd0205a938c587f1f30258d",
  "contacto.html": "https://9eb1832f3e42a1dbd6ba854f8d6a1cb2.r2.cloudflarestorage.com/ai-whisperers-backups/rubicon-eas/contacto.html?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=${R2_ACCESS_KEY_ID}%2F20260810%2Fauto%2Fs3%2Faws4_request&X-Amz-Date=20260810T205245Z&X-Amz-Expires=604800&X-Amz-SignedHeaders=host&X-Amz-Signature=7a318d6867b751002f85eca6748e4f164ec9a8724af3a8c3b350c30399e97a24",
  "derecho-penal.html": "https://9eb1832f3e42a1dbd6ba854f8d6a1cb2.r2.cloudflarestorage.com/ai-whisperers-backups/rubicon-eas/derecho-penal.html?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=${R2_ACCESS_KEY_ID}%2F20260810%2Fauto%2Fs3%2Faws4_request&X-Amz-Date=20260810T205245Z&X-Amz-Expires=604800&X-Amz-SignedHeaders=host&X-Amz-Signature=9d9905f692c0877b145e5943d8d4333488beb16f7dad66571c98dc5872ebe8fc",
  "nosotros.html": "https://9eb1832f3e42a1dbd6ba854f8d6a1cb2.r2.cloudflarestorage.com/ai-whisperers-backups/rubicon-eas/nosotros.html?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=${R2_ACCESS_KEY_ID}%2F20260810%2Fauto%2Fs3%2Faws4_request&X-Amz-Date=20260810T205245Z&X-Amz-Expires=604800&X-Amz-SignedHeaders=host&X-Amz-Signature=4daeef919599d193995e8745248654c46865ff1d24d686c292340781cd783607",
  "blog.html": "https://9eb1832f3e42a1dbd6ba854f8d6a1cb2.r2.cloudflarestorage.com/ai-whisperers-backups/rubicon-eas/blog.html?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=${R2_ACCESS_KEY_ID}%2F20260810%2Fauto%2Fs3%2Faws4_request&X-Amz-Date=20260810T205245Z&X-Amz-Expires=604800&X-Amz-SignedHeaders=host&X-Amz-Signature=715906db388b830c306aa28e394b66a9c6401751d22c993116e6878b6530451f",
  "assets/styles.css": "https://9eb1832f3e42a1dbd6ba854f8d6a1cb2.r2.cloudflarestorage.com/ai-whisperers-backups/rubicon-eas/assets/styles.css?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=${R2_ACCESS_KEY_ID}%2F20260810%2Fauto%2Fs3%2Faws4_request&X-Amz-Date=20260810T205245Z&X-Amz-Expires=604800&X-Amz-SignedHeaders=host&X-Amz-Signature=9ecffd2da9376a6d9ae8cbfe10e16556f279d75283944ead3831a99f220ada62",
  "assets/content.es.json": "https://9eb1832f3e42a1dbd6ba854f8d6a1cb2.r2.cloudflarestorage.com/ai-whisperers-backups/rubicon-eas/assets/content.es.json?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=${R2_ACCESS_KEY_ID}%2F20260810%2Fauto%2Fs3%2Faws4_request&X-Amz-Date=20260810T205245Z&X-Amz-Expires=604800&X-Amz-SignedHeaders=host&X-Amz-Signature=771ba5b61a81e2ef1e1f9c53d1f889d75d7a42e25aa3007a82c9cfef0173b84d",
  "assets/main.js": "https://9eb1832f3e42a1dbd6ba854f8d6a1cb2.r2.cloudflarestorage.com/ai-whisperers-backups/rubicon-eas/assets/main.js?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=${R2_ACCESS_KEY_ID}%2F20260810%2Fauto%2Fs3%2Faws4_request&X-Amz-Date=20260810T205245Z&X-Amz-Expires=604800&X-Amz-SignedHeaders=host&X-Amz-Signature=6843349df50f665ec8ecbe440fe1b2ab7a24c5f4e41c2f2ff8d7e0c2ab7f6b53"
};

function guessCT(path) {
  if (path.endsWith(".html")) return "text/html; charset=utf-8";
  if (path.endsWith(".css")) return "text/css; charset=utf-8";
  if (path.endsWith(".js")) return "application/javascript; charset=utf-8";
  if (path.endsWith(".json")) return "application/json; charset=utf-8";
  if (path.endsWith(".svg")) return "image/svg+xml";
  return "application/octet-stream";
}

async function handle(request) {
  const url = new URL(request.url);
  const path = url.pathname;

  // Strip leading /
  let key = path.replace(/^\//, "");

  // Root → index.html
  if (key === "") key = "index.html";

  // Strip query/hash from filename match
  for (const candidate of [key, key + ".html"]) {
    if (FILES[candidate]) {
      try {
        const resp = await fetch(FILES[candidate], {
          cf: { cacheTtl: 300, cacheEverything: true }
        });
        return new Response(await resp.text(), {
          headers: {
            "Content-Type": guessCT(candidate),
            "Cache-Control": "public, max-age=300"
          }
        });
      } catch (e) {
        return new Response("Upstream error: " + e.message, { status: 502 });
      }
    }
  }

  return new Response("Not found: " + path, { status: 404 });
}
