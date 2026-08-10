"""
Hermes Agent — Evolution API MCP Integration
=============================================
Wrapper que permite a Hermes (el agente de escritorio) comunicarse
con Ometz Dental WhatsApp Business via Evolution API.

Capacidades:
- send_message(to, text) — enviar mensaje a un paciente
- list_chats() — listar conversaciones activas
- get_messages(phone, limit) — leer historial de mensajes
- get_pending_escalations() — ver mensajes escalados
- mark_escalation_resolved(id) — cerrar escalación
- classify_text(text) — clasificar sin enviar
- search_contacts(query) — buscar en el CRM

Uso:
    from hermes_mcp_integration import WhatsAppClient
    wa = WhatsAppClient()
    await wa.send_message("+595 987 126 790", "Hola Gaby")

Owner: Erebus (Hermes-AI)
Status: v1.0 — 27 jul 2026
"""

import os
import logging
from typing import Optional, List, Dict
from datetime import datetime
import httpx

logger = logging.getLogger("hermes-wa-integration")


class WhatsAppClient:
    """Cliente Evolution API para Hermes."""

    def __init__(
        self,
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
        instance: str = "ometsdental-business",
    ):
        self.base_url = base_url or os.getenv("EVOLUTION_API_URL", "http://localhost:8080")
        self.api_key = api_key or os.getenv("EVOLUTION_API_KEY", "")
        self.instance = instance
        self.headers = {"apikey": self.api_key, "Content-Type": "application/json"}

    async def _request(self, method: str, path: str, **kwargs):
        url = f"{self.base_url}{path}"
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.request(method, url, headers=self.headers, **kwargs)
            response.raise_for_status()
            return response.json()

    async def send_message(self, to: str, text: str) -> dict:
        """Enviar un mensaje a un paciente."""
        phone = to.replace("+", "").replace(" ", "")
        return await self._request(
            "POST",
            f"/message/sendText/{self.instance}",
            json={"number": phone, "text": text},
        )

    async def send_image(self, to: str, image_url: str, caption: str = "") -> dict:
        """Enviar una imagen con caption."""
        phone = to.replace("+", "").replace(" ", "")
        return await self._request(
            "POST",
            f"/message/sendImage/{self.instance}",
            json={"number": phone, "mediatype": "image", "media": image_url, "caption": caption},
        )

    async def send_audio(self, to: str, audio_url: str) -> dict:
        """Enviar un audio."""
        phone = to.replace("+", "").replace(" ", "")
        return await self._request(
            "POST",
            f"/message/sendWhatsAppAudio/{self.instance}",
            json={"number": phone, "audio": audio_url},
        )

    async def list_chats(self) -> List[dict]:
        """Listar todas las conversaciones activas."""
        return await self._request("GET", f"/chat/findChats/{self.instance}")

    async def get_messages(self, phone: str, limit: int = 50) -> List[dict]:
        """Obtener historial de mensajes con un paciente."""
        phone_clean = phone.replace("+", "").replace(" ", "")
        return await self._request(
            "GET",
            f"/chat/findMessages/{self.instance}",
            params={"where": {"key": {"remoteJid": f"{phone_clean}@s.whatsapp.net"}}, "limit": limit},
        )

    async def get_contacts(self) -> List[dict]:
        """Listar todos los contactos."""
        return await self._request("GET", f"/chat/findContacts/{self.instance}")

    async def find_contact(self, name: str) -> List[dict]:
        """Buscar contactos por nombre."""
        contacts = await self.get_contacts()
        return [c for c in contacts if name.lower() in (c.get("name", "") or "").lower()]

    async def get_connection_state(self) -> dict:
        """Estado de la conexión Evolution API."""
        return await self._request("GET", f"/instance/connectionState/{self.instance}")

    async def get_qr(self) -> dict:
        """Obtener QR code para reconectar."""
        return await self._request("GET", f"/instance/connect/{self.instance}")

    async def logout(self) -> dict:
        """Cerrar sesión y desconectar Evolution API."""
        return await self._request("DELETE", f"/instance/logout/{self.instance}")

    async def restart(self) -> dict:
        """Reiniciar la instancia."""
        return await self._request("POST", f"/instance/restart/{self.instance}")

    # === CRM (Supabase directo) ===

    async def get_pending_escalations(self, supabase_url: str, supabase_key: str) -> List[dict]:
        """Obtener escalaciones pendientes (requiere Supabase)."""
        from supabase import create_client
        supabase = create_client(supabase_url, supabase_key)
        result = supabase.table("wa_escalations").select("*").eq("status", "pending").execute()
        return result.data

    async def mark_escalation_resolved(
        self, escalation_id: int, resolved_by: str, notes: str = "",
        supabase_url: Optional[str] = None, supabase_key: Optional[str] = None,
    ) -> dict:
        """Marcar escalación como resuelta."""
        from supabase import create_client
        url = supabase_url or os.getenv("SUPABASE_URL")
        key = supabase_key or os.getenv("SUPABASE_SERVICE_KEY")
        supabase = create_client(url, key)
        result = supabase.table("wa_escalations").update({
            "status": "resolved",
            "resolved_at": datetime.now().isoformat(),
            "resolved_by": resolved_by,
            "resolution_notes": notes,
        }).eq("id", escalation_id).execute()
        return result.data

    async def get_recent_messages(self, limit: int = 20, supabase_url: Optional[str] = None, supabase_key: Optional[str] = None) -> List[dict]:
        """Obtener mensajes recientes (vía Supabase)."""
        from supabase import create_client
        url = supabase_url or os.getenv("SUPABASE_URL")
        key = supabase_key or os.getenv("SUPABASE_SERVICE_KEY")
        supabase = create_client(url, key)
        result = supabase.table("wa_messages").select(
            "*"
        ).order(
            "created_at", desc=True
        ).limit(limit).execute()
        return result.data

    async def search_contact(self, query: str, supabase_url: Optional[str] = None, supabase_key: Optional[str] = None) -> List[dict]:
        """Buscar contacto en el CRM."""
        from supabase import create_client
        url = supabase_url or os.getenv("SUPABASE_URL")
        key = supabase_key or os.getenv("SUPABASE_SERVICE_KEY")
        supabase = create_client(url, key)
        result = supabase.table("wa_contacts").select("*").or_(
            f"name.ilike.%{query}%,phone.ilike.%{query}%"
        ).execute()
        return result.data

    async def update_contact(self, phone: str, updates: dict, supabase_url: Optional[str] = None, supabase_key: Optional[str] = None) -> dict:
        """Actualizar un contacto."""
        from supabase import create_client
        url = supabase_url or os.getenv("SUPABASE_URL")
        key = supabase_key or os.getenv("SUPABASE_SERVICE_KEY")
        supabase = create_client(url, key)
        updates["updated_at"] = datetime.now().isoformat()
        result = supabase.table("wa_contacts").update(updates).eq("phone", phone).execute()
        return result.data


# === HIGH-LEVEL HELPERS (uso directo) ===

async def send_to_gaby(message: str) -> dict:
    """Helper: enviar un mensaje a Gaby (cuenta Business)."""
    client = WhatsAppClient()
    return await client.send_message("+595 987 126 790", message)


async def send_to_patient(phone: str, message: str) -> dict:
    """Helper: enviar un mensaje a un paciente."""
    client = WhatsAppClient()
    return await client.send_message(phone, message)


async def broadcast_message(phones: List[str], message: str) -> List[dict]:
    """Enviar un mensaje a múltiples pacientes."""
    import asyncio
    client = WhatsAppClient()
    tasks = [client.send_message(phone, message) for phone in phones]
    return await asyncio.gather(*tasks, return_exceptions=True)


# === CLI USAGE ===

if __name__ == "__main__":
    import sys
    import asyncio

    if len(sys.argv) < 2:
        print("""
Ometz Dental WhatsApp Client

Usage:
  python hermes_mcp_integration.py status
  python hermes_mcp_integration.py send <phone> <message>
  python hermes_mcp_integration.py chats
  python hermes_mcp_integration.py qr
  python hermes_mcp_integration.py restart
        """)
        sys.exit(1)

    async def main():
        client = WhatsAppClient()

        cmd = sys.argv[1]
        if cmd == "status":
            state = await client.get_connection_state()
            print(f"Connection state: {state}")
        elif cmd == "send":
            phone = sys.argv[2]
            message = " ".join(sys.argv[3:])
            result = await client.send_message(phone, message)
            print(f"✅ Sent: {result}")
        elif cmd == "chats":
            chats = await client.list_chats()
            print(f"Active chats: {len(chats)}")
            for c in chats[:10]:
                print(f"  - {c.get('name', 'Unknown')}: {c.get('lastMessage', {}).get('message', {}).get('conversation', '')[:50]}")
        elif cmd == "qr":
            qr = await client.get_qr()
            print(f"QR code: {qr.get('qrcode', '')[:100]}...")
        elif cmd == "restart":
            result = await client.restart()
            print(f"✅ Restarted: {result}")
        else:
            print(f"Unknown command: {cmd}")
            sys.exit(1)

    asyncio.run(main())
