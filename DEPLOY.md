# Rubicón EAS — Deploy & Iteration Playbook

Use this doc to redeploy the static site after content edits, or to advance
to the canonical Host A Swarm deployment.

---

## Credentials

This repo does **not** contain any credentials. The deploy scripts reference
environment variables; replace them with your own before running.

| Variable | What it's for | Where to get it |
|---|---|---|
| `${CF_API_TOKEN}` | Cloudflare API token | Cloudflare → My Profile → API Tokens → Create Token |
| `${CF_ACCOUNT_ID}` | Cloudflare account ID | Cloudflare dashboard → right sidebar |
| `${R2_ACCESS_KEY_ID}` | R2 access key | Cloudflare → R2 → Manage R2 API Tokens |
| `${R2_SECRET_ACCESS_KEY}` | R2 secret key | Cloudflare → R2 → Manage R2 API Tokens |
| `${BUCKET}` | R2 bucket name | Default: `ai-whisperers-backups` |
| `${GH_TOKEN}` | GitHub personal access token | GitHub → Settings → Developer settings → PAT |

### Quick setup

```bash
# Add to your shell rc or .env file
export CF_ACCOUNT_ID="your_account_id"
export CF_API_TOKEN="cfat_your_token"
export R2_ACCESS_KEY_ID="your_r2_key"
export R2_SECRET_ACCESS_KEY="your_r2_secret"
export BUCKET="ai-whisperers-backups"
```

Then the deploy commands in this doc will work.

---

## 1. Static preview (current state)


**Architecture:** CF Worker `rubicon-eas-site` → R2 bucket `ai-whisperers-backups` → CF edge → public.

**Files:** 12 files in `s3://ai-whisperers-backups/rubicon-eas/` (~134KB total).
**Live URL:** https://rubiconeas.paragu-ai.com/
**DNS:** A records `rubiconeas` + `www.rubiconeas` → 38.9.96.179 (proxied).
**Worker routes:** `rubiconeas.paragu-ai.com/*` + `www.rubiconeas.paragu-ai.com/*` → `rubicon-eas-site`.

### To edit content and redeploy

```bash
# 1. Edit sample/assets/content.es.json (or any HTML)
# 2. Re-upload to R2
python3 -c "
import boto3
s3 = boto3.client('s3',
    endpoint_url='https://9eb1832f3e42a1dbd6ba854f8d6a1cb2.r2.cloudflarestorage.com',
    aws_access_key_id='${R2_ACCESS_KEY_ID}',
    aws_secret_access_key='${R2_SECRET_ACCESS_KEY}',
    region_name='auto')
s3.put_object(Bucket='ai-whisperers-backups', Key='rubicon-eas/index.html',
              Body=open('sample/index.html','rb').read(),
              ContentType='text/html; charset=utf-8',
              CacheControl='public, max-age=300')
"
# 3. New R2 URL has different signature → regenerate presigned URL
url=$(python3 -c "import boto3; s3=boto3.client('s3',endpoint_url='https://9eb1832f3e42a1dbd6ba854f8d6a1cb2.r2.cloudflarestorage.com',aws_access_key_id='${R2_ACCESS_KEY_ID}',aws_secret_access_key='${R2_SECRET_ACCESS_KEY}',region_name='auto'); print(s3.generate_presigned_url('get_object',Params={'Bucket':'ai-whisperers-backups','Key':'rubicon-eas/index.html'},ExpiresIn=7*24*3600))")
# 4. Update worker.js with new URL map
# 5. Deploy worker
curl -X PUT "https://api.cloudflare.com/client/v4/accounts/9eb1832f3e42a1dbd6ba854f8d6a1cb2/workers/scripts/rubicon-eas-site" \
  -H "Authorization: Bearer ${CF_API_TOKEN}" \
  -H "Content-Type: application/javascript" \
  --data-binary "@worker.js"
```

### Cache invalidation

CF Worker caches upstream R2 fetches with `cacheTtl: 300` (5 min) and
`cacheEverything: true`. To force fresh content, hit the URL with a
query-string cache buster. Real fixes: edit the script + URL → deploy.

---

## 2. Advanced: real Next.js build on Host A Swarm

Once content is final and the client is ready:

### 2.1 Fork the canonical app

```bash
cp -r /opt/data/build/paragu-ai-leads-monorepo/apps/Clau-Bellino/ \
   /opt/data/build/paragu-ai-platform/apps/rubicon-eas/
```

Replace `content/es.json` with the final content from `sample/assets/content.es.json`.
Add `apps/rubicon-eas/src/app/derecho-civil/page.tsx`, `derecho-penal/`, `derecho-ambiental/`,
`/nosotros/`, `/casos/`, `/contacto/`, `/blog/`.

### 2.2 Build

```bash
cd /opt/data/build/paragu-ai-platform/apps/rubicon-eas
PATH=/opt/data/build/pnpm-install/node_modules/.bin:$PATH pnpm install
PATH=/opt/data/build/pnpm-install/node_modules/.bin:$PATH pnpm build
# Output: .next/standalone/apps/rubicon-eas/
```

### 2.3 Push to Host A

```bash
tar czf rubicon-eas.tar.gz -C .next/standalone .
ssh root@38.9.96.179 "mkdir -p /opt/stacks/rubicon-eas && cd /opt/stacks/rubicon-eas && tar xzf -" < rubicon-eas.tar.gz
```

### 2.4 Build Docker image (on Host A)

Dockerfile.standalone (reuse from ometz/nexa):
```dockerfile
FROM node:20-alpine
WORKDIR /app
COPY . .
ENV PORT=3000
EXPOSE 3000
CMD ["node", "server.js"]
```

```bash
docker build -t rubicon-eas:prod -f Dockerfile.standalone .
```

### 2.5 docker-compose.yml

```yaml
version: '3.8'
services:
  web:
    image: rubicon-eas:prod
    networks:
      - traefik-public
    deploy:
      labels:
        - traefik.enable=true
        - traefik.swarm.network=traefik-public
        - traefik.http.routers.rubicon-eas.rule=Host(`rubiconeas.paragu-ai.com`)
        - traefik.http.routers.rubicon-eas.entrypoints=websecure
        - traefik.http.routers.rubicon-eas.tls=true
        - traefik.http.routers.rubicon-eas.tls.certresolver=le
        - traefik.http.services.rubicon-eas.loadbalancer.server.port=3000
        - traefik.http.routers.rubicon-eas-http.rule=Host(`rubiconeas.paragu-ai.com`)
        - traefik.http.routers.rubicon-eas-http.entrypoints=web
        - traefik.http.routers.rubicon-eas-http.middlewares=redirect-to-https@docker
    restart: unless-stopped
networks:
  traefik-public:
    external: true
```

```bash
docker stack deploy -c docker-compose.yml rubicon-eas
```

### 2.6 DNS

DNS A record `rubiconeas.paragu-ai.com` MUST be `proxied: false` (grey-cloud)
for Let's Encrypt HTTP-01 to work.

### 2.7 Verify

```bash
curl -k https://rubiconeas.paragu-ai.com/ -I
# Expect: HTTP/2 200, server: nginx (Traefik)
```

---

## 3. Triage bot integration (n8n + Evolution API)

End-to-end:
1. User submits form on `contacto.html`
2. POST to `/api/lead` (write that endpoint under Next.js)
3. Webhook → n8n workflow `Rubicon-EAS-Lead-Intake`
4. n8n formats Mensaje message and POSTs to Evolution API
5. Evolution API sends WhatsApp message to partner's number

**n8n webhook URL:** `https://n8n.paragu-ai.com/webhook/rubicon-eas-lead`
**Evolution API endpoint:** `https://evolution.paragu-ai.com/message/sendText/<instance>`

Partner's WhatsApp instance: `+595 981 234 567` (placeholder, real one needed).

---

## 4. Domain: `rubiconeas.com.py`

**Status:** NOT registered.
**Action:** Client registers at https://nic.py
**Cost:** ~gs. 200-300k/yr
**Once registered:**
1. Add zone to CF account 9eb1832f3e42a1dbd6ba854f8d6a1cb2
2. Point nameservers to CF (or transfer)
3. Add Worker route or Host A Swarm Traefik rule for apex + www
4. Update Worker if needed (handle apex domain)

Until then: `rubiconeas.paragu-ai.com` is the live preview.

---

## 5. Rollback

If the new Worker breaks the site:

```bash
# Re-deploy the previous Worker version
curl -X GET "https://api.cloudflare.com/client/v4/accounts/9eb1832f3e42a1dbd6ba854f8d6a1cb2/workers/scripts/rubicon-eas-site/versions" \
  -H "Authorization: Bearer ${CF_API_TOKEN}"
# Find the previous version_id, then:
curl -X PUT "https://api.cloudflare.com/client/v4/accounts/9eb1832f3e42a1dbd6ba854f8d6a1cb2/workers/scripts/rubicon-eas-site" \
  -H "Authorization: Bearer ${CF_API_TOKEN}" \
  -H "Content-Type: application/javascript" \
  --data-binary "@worker.js.bak"
```

For Host A Swarm: `docker service update --image rubicon-eas:prod-previous rubicon-eas_web`.
