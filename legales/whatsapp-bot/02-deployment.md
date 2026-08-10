# 🚀 Evolution API — Deployment Guide
## Ometz Dental WhatsApp Business Integration

**Versión:** 1.0 — 27 jul 2026
**Stack:** Evolution API v2 (Baileys) · Postgres · Redis · FastAPI webhook · Supabase CRM
**Target:** Docker Swarm (mismo VPS que el cliente actual)
**Phone:** `+595 987 126 790` (Tigo Business, activado 27 jul)

---

## ⚠️ DISCLAIMER

> **Evolution API usa el protocolo WhatsApp Web (no la API oficial de Meta).**
> Funciona escaneando el QR de WhatsApp Business desde el celular con el chip Tigo.
> Es lo mismo que hacer "WhatsApp Web" pero con una API programable.
>
> **Riesgos:**
> - Si Meta cambia el protocolo, Evolution se rompe hasta que actualicen
> - Si el celular está offline más de 14 días, la sesión se pierde (hay que re-escanear QR)
> - Riesgo MUY bajo de ban si no se respetan los rate limits
>
> **Beneficio:**
> - Cero costo (vs WhatsApp Business API oficial ~$0.05/msj)
> - Control total
> - Integración directa con Hermes

---

## 📋 PREREQUISITOS

### Infra
- VPS con Docker Swarm ya corriendo (Hostinger, DigitalOcean, etc.)
- Dominio `ometzdental.com` con DNS apuntando al VPS
- SSL cert (Let's Encrypt vía traefik o certbot)
- ~2GB RAM libre para Evolution + Postgres + Redis

### Secrets a generar
```bash
# Generar tokens seguros
openssl rand -hex 32  # EVOLUTION_API_TOKEN
openssl rand -hex 32  # JWT_SECRET
openssl rand -hex 32  # WEBHOOK_HMAC_SECRET
openssl rand -hex 32  # EVOLUTION_API_KEY
openssl rand -hex 32  # REDIS_PASSWORD
openssl rand -hex 32  # POSTGRES_PASSWORD
```

### URLs
- `https://api.ometzdental.com` — Evolution API endpoint
- `https://api.ometzdental.com/webhooks/evolution` — webhook destino
- `https://api.ometzdental.com/dashboard` — dashboard opcional

---

## 🏗️ FASE 1 — Desplegar Evolution API (15 min)

### 1.1 Crear el stack

```bash
mkdir -p /root/ometsdental-stack
cd /root/ometsdental-stack
```

Copiar `evolution-api-config.json` del repo a `/root/ometsdental-stack/config.json`.

### 1.2 Crear docker-compose.yml

```yaml
version: "3.8"

services:
  evolution-api:
    image: evoapicloud/evolution-api:v2.0.0
    container_name: ometsdental-evolution-api
    restart: always
    ports:
      - "8080:8080"
    environment:
      - SERVER_PORT=8080
      - SERVER_URL=https://api.ometzdental.com
      - AUTHENTICATION_TYPE=apikey
      - AUTHENTICATION_API_KEY=${EVOLUTION_API_KEY}
      - AUTHENTICATION_JWT_SECRET=${JWT_SECRET}
      - DATABASE_ENABLED=true
      - DATABASE_PROVIDER=postgresql
      - DATABASE_CONNECTION_URI=postgresql://evolution:${POSTGRES_PASSWORD}@postgres:5432/evolution
      - REDIS_ENABLED=true
      - REDIS_URI=redis://:${REDIS_PASSWORD}@redis:6379
      - WEBHOOK_GLOBAL_ENABLED=true
      - WEBHOOK_GLOBAL_URL=https://api.ometzdental.com/webhooks/evolution
      - WEBHOOK_GLOBAL_WEBHOOK_BY_EVENTS=true
      - WEBHOOK_GLOBAL_WEBHOOK_BASE64=false
      - LOG_LEVEL=INFO
    volumes:
      - evolution_data:/evolution/store
    networks:
      - ometsdental-net
    depends_on:
      - postgres
      - redis
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  webhook-handler:
    build: 
      context: /root/dentist/08_WHATSAPP/evolution-api/webhook-handler
      dockerfile: Dockerfile
    container_name: ometsdental-webhook-handler
    restart: always
    ports:
      - "8081:8080"
    environment:
      - EVOLUTION_API_URL=http://evolution-api:8080
      - EVOLUTION_API_KEY=${EVOLUTION_API_KEY}
      - WEBHOOK_HMAC_SECRET=${WEBHOOK_HMAC_SECRET}
      - SUPABASE_URL=${SUPABASE_URL}
      - SUPABASE_SERVICE_KEY=${SUPABASE_SERVICE_KEY}
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    networks:
      - ometsdental-net
    depends_on:
      - evolution-api

  postgres:
    image: postgres:16-alpine
    container_name: ometsdental-postgres
    restart: always
    environment:
      - POSTGRES_USER=evolution
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
      - POSTGRES_DB=evolution
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - ometsdental-net

  redis:
    image: redis:7-alpine
    container_name: ometsdental-redis
    restart: always
    command: redis-server --requirepass ${REDIS_PASSWORD}
    volumes:
      - redis_data:/data
    networks:
      - ometsdental-net

volumes:
  evolution_data:
  postgres_data:
  redis_data:

networks:
  ometsdental-net:
    driver: overlay
```

### 1.3 Levantar el stack

```bash
cd /root/ometsdental-stack
docker stack deploy -c docker-compose.yml ometsdental
```

### 1.4 Verificar

```bash
# Esperar 30 segundos y chequear
sleep 30
docker service ls | grep ometsdental
curl -f http://localhost:8080/health
# Esperado: {"status":"ok"}
```

---

## 🌐 FASE 2 — Nginx + SSL (10 min)

### 2.1 Configurar Nginx

```bash
cat > /etc/nginx/sites-available/ometzdental-api <<'EOF'
upstream evolution_api {
    server localhost:8080;
}

upstream webhook_handler {
    server localhost:8081;
}

server {
    listen 443 ssl http2;
    server_name api.ometzdental.com;

    ssl_certificate /etc/letsencrypt/live/api.ometzdental.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/api.ometzdental.com/privkey.pem;

    # Evolution API
    location / {
        proxy_pass http://evolution_api;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Webhook handler
    location /webhooks/evolution {
        proxy_pass http://webhook_handler/webhooks/evolution;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}

server {
    listen 80;
    server_name api.ometzdental.com;
    return 301 https://$server_name$request_uri;
}
EOF

ln -s /etc/nginx/sites-available/ometzdental-api /etc/nginx/sites-enabled/
nginx -t && systemctl reload nginx
```

### 2.2 SSL con certbot

```bash
certbot --nginx -d api.ometzdental.com --non-interactive --agree-tos -m ops@ometzdental.com
```

---

## 📱 FASE 3 — Conectar Gaby (5 min)

### 3.1 Crear instancia

```bash
curl -X POST http://localhost:8080/instance/create \
  -H "apikey: ${EVOLUTION_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "instanceName": "ometsdental-business",
    "number": "595987126790",
    "integration": "WHATSAPP-BUSINESS"
  }'
```

### 3.2 Obtener QR

```bash
curl http://localhost:8080/instance/connect/ometsdental-business \
  -H "apikey: ${EVOLUTION_API_KEY}"
```

Devuelve un QR en base64. Gaby lo escanea desde WA Business:

1. **Abrí WA Business** en el celular con el chip Tigo
2. **≡ → Ajustes → Herramientas para la empresa → Más herramientas → WhatsApp Business API**
3. O si no aparece: **Vincular dispositivo** (es lo mismo)
4. Escaneá el QR de Evolution API

### 3.3 Verificar conexión

```bash
curl http://localhost:8080/instance/connectionState/ometsdental-business \
  -H "apikey: ${EVOLUTION_API_KEY}"
# Esperado: {"instance":{"state":"open"}}
```

---

## 🧪 FASE 4 — Test (5 min)

### 4.1 Mandar mensaje de prueba

Desde tu celular personal, mandá un WhatsApp a `+595 987 126 790`:

```
Hola, ¿cuánto cuesta una consulta?
```

En ~5 segundos, WA Business debería responder con `/precio` (auto-classification).

### 4.2 Verificar logs

```bash
docker logs -f ometsdental-evolution-api
# Debería loguear: "MESSAGES_UPSERT" + clasificación "PRICING"
```

### 4.3 Verificar Supabase

```sql
-- En Supabase SQL editor
SELECT * FROM wa_messages ORDER BY created_at DESC LIMIT 5;
SELECT * FROM wa_contacts WHERE phone = '+595 XXX';
```

---

## 📊 FASE 5 — Dashboard (opcional, 10 min)

### 5.1 Grafana simple

```bash
docker run -d --name grafana \
  -p 3000:3000 \
  -e GF_SECURITY_ADMIN_PASSWORD=admin \
  grafana/grafana
```

Acceder a `http://localhost:3000` (admin/admin).

### 5.2 Conectar a Postgres

Agregar data source: Postgres @ `postgres:5432`. Tabla `wa_messages`.

### 5.3 Panel básico

```sql
SELECT 
  DATE_TRUNC('day', created_at) as day,
  COUNT(*) as total_messages,
  COUNT(DISTINCT contact_phone) as unique_contacts,
  COUNT(CASE WHEN classification = 'URGENT' THEN 1 END) as urgent,
  COUNT(CASE WHEN classification = 'APPOINTMENT' THEN 1 END) as appointments
FROM wa_messages 
WHERE created_at > NOW() - INTERVAL '30 days'
GROUP BY 1
ORDER BY 1;
```

---

## 🔒 FASE 6 — Hardening (10 min)

### 6.1 Firewall

```bash
ufw allow 443/tcp
ufw allow 80/tcp
ufw deny 8080/tcp  # Evolution API no expuesto a internet
ufw deny 8081/tcp  # Webhook no expuesto a internet
```

### 6.2 Fail2ban

```bash
apt install fail2ban -y
systemctl enable fail2ban
```

### 6.3 Backups

```bash
# Backup diario del Postgres
cat > /etc/cron.daily/backup-evolution <<'EOF'
#!/bin/bash
docker exec ometsdental-postgres pg_dump -U evolution evolution | \
  gzip > /var/backups/evolution-$(date +%Y%m%d).sql.gz
# Retention: 30 días
find /var/backups -name "evolution-*.sql.gz" -mtime +30 -delete
EOF
chmod +x /etc/cron.daily/backup-evolution
```

### 6.4 Monitoring

```bash
# Healthcheck cada 5 min
cat > /etc/cron.d/healthcheck-evolution <<'EOF'
*/5 * * * * curl -sf http://localhost:8080/health || echo "Evolution API DOWN" | mail -s "ALERT" ops@ometzdental.com
EOF
```

---

## 🆘 TROUBLESHOOTING

### Evolution API no responde
```bash
docker logs ometsdental-evolution-api --tail 100
docker service ps ometsdental_evolution-api
```

### QR no aparece
```bash
# Forzar refresh
curl -X POST http://localhost:8080/instance/refresh/ometsdental-business \
  -H "apikey: ${EVOLUTION_API_KEY}"
```

### QR expiró
Los QR expiran cada 60 segundos. Re-generar:
```bash
curl http://localhost:8080/instance/connect/ometsdental-business \
  -H "apikey: ${EVOLUTION_API_KEY}"
```

### Gaby perdió la conexión
Si el celular estuvo offline >14 días, la sesión expira. Re-escanear QR.

### Mensajes no se procesan
```bash
# Verificar webhook
docker logs ometsdental-webhook-handler --tail 50
# Test manual
curl -X POST http://localhost:8081/webhooks/evolution \
  -H "Content-Type: application/json" \
  -d '{"event":"MESSAGES_UPSERT","instance":"ometsdental-business","data":{"key":{"remoteJid":"595XXXXXXXXX@s.whatsapp.net"},"message":{"conversation":"test"}}}'
```

---

## 💰 COSTS

| Concepto | Costo |
|---|---|
| Evolution API (self-hosted) | $0 |
| Meta of WhatsApp Business API | $0.05/msj (~$10-50/mes según volumen) |
| VPS adicional (si se necesita) | $5-20/mes |
| OpenAI API (clasificación) | ~$0.001/mensaje |
| Supabase (free tier) | $0 |

**Total: $0/mes para 500-1000 mensajes/día.** En escala >5000 m/d, conviene migrar a WhatsApp Business API oficial.

---

## 📋 CROSS-REFERENCES

- Config: `evolution-api-config.json`
- Quick replies: `08_WHATSAPP/templates/final/quick-replies-v2-final.md`
- Operations guide: `08_WHATSAPP/automation/whatsapp-operations-guide.md`
- Webhook handler: `evolution-api/webhook-handler/`
- Supabase schema: `evolution-api/SUPABASE-SCHEMA.sql`
- Hermes integration: `evolution-api/hermes-mcp-integration.py`
- Deploy script: `scripts/deploy-evolution-api.sh`

---

## 🎯 PRÓXIMOS PASOS POST-DEPLOY

1. **Día 1**: Gaby conecta el QR. Test con 5 mensajes de prueba.
2. **Día 2-3**: Validar clasificación. Ajustar prompts si hay errores.
3. **Semana 1**: Monitorear. Kiki responde urgencias.
4. **Semana 2**: Activar Meta Ads (en paralelo).
5. **Semana 4**: Optimizar. A/B test respuestas.

---

**STATUS:** v1.0 — Deployment guide completo. Listo para ejecutar.
