-- Ometz Dental WhatsApp CRM schema
-- Created: 27 jul 2026
-- Owner: Erebus (Hermes-AI)
-- Schema: Supabase Postgres

-- ============================================================
-- 1. wa_contacts — Master contact book
-- ============================================================
CREATE TABLE IF NOT EXISTS wa_contacts (
    id BIGSERIAL PRIMARY KEY,
    phone TEXT UNIQUE NOT NULL,
    name TEXT,
    is_existing_patient BOOLEAN DEFAULT FALSE,
    is_referral BOOLEAN DEFAULT FALSE,
    referred_by TEXT,
    source TEXT DEFAULT 'whatsapp',
    first_message_at TIMESTAMPTZ,
    last_message_at TIMESTAMPTZ,
    total_messages INTEGER DEFAULT 0,
    last_classification TEXT,
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_contacts_phone ON wa_contacts(phone);
CREATE INDEX idx_contacts_last_message ON wa_contacts(last_message_at DESC);
CREATE INDEX idx_contacts_existing_patient ON wa_contacts(is_existing_patient);

-- ============================================================
-- 2. wa_messages — All messages (inbound + outbound)
-- ============================================================
CREATE TABLE IF NOT EXISTS wa_messages (
    id BIGSERIAL PRIMARY KEY,
    phone TEXT NOT NULL,
    direction TEXT NOT NULL CHECK (direction IN ('inbound', 'outbound')),
    text TEXT NOT NULL,
    category TEXT,
    priority TEXT,
    confidence NUMERIC(3, 2),
    escalation_needed BOOLEAN DEFAULT FALSE,
    auto BOOLEAN DEFAULT FALSE,
    message_id TEXT,
    quoted_message_id TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_messages_phone ON wa_messages(phone);
CREATE INDEX idx_messages_created ON wa_messages(created_at DESC);
CREATE INDEX idx_messages_category ON wa_messages(category);
CREATE INDEX idx_messages_priority ON wa_messages(priority);

-- ============================================================
-- 3. wa_conversations — Aggregated conversation view
-- ============================================================
CREATE TABLE IF NOT EXISTS wa_conversations (
    id BIGSERIAL PRIMARY KEY,
    phone TEXT UNIQUE NOT NULL,
    started_at TIMESTAMPTZ DEFAULT NOW(),
    last_message_at TIMESTAMPTZ DEFAULT NOW(),
    message_count INTEGER DEFAULT 1,
    last_category TEXT,
    last_priority TEXT,
    status TEXT DEFAULT 'open' CHECK (status IN ('open', 'archived', 'escalated')),
    assigned_to TEXT,
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_conversations_phone ON wa_conversations(phone);
CREATE INDEX idx_conversations_status ON wa_conversations(status);
CREATE INDEX idx_conversations_last_message ON wa_conversations(last_message_at DESC);

-- ============================================================
-- 4. wa_appointments — Calendar bookings
-- ============================================================
CREATE TABLE IF NOT EXISTS wa_appointments (
    id BIGSERIAL PRIMARY KEY,
    phone TEXT NOT NULL,
    patient_name TEXT,
    service TEXT,
    scheduled_at TIMESTAMPTZ NOT NULL,
    duration_minutes INTEGER DEFAULT 60,
    status TEXT DEFAULT 'scheduled' CHECK (status IN ('scheduled', 'confirmed', 'attended', 'no_show', 'cancelled', 'rescheduled')),
    notes TEXT,
    google_calendar_event_id TEXT,
    reminder_sent_24h BOOLEAN DEFAULT FALSE,
    reminder_sent_1h BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_appointments_phone ON wa_appointments(phone);
CREATE INDEX idx_appointments_scheduled ON wa_appointments(scheduled_at);
CREATE INDEX idx_appointments_status ON wa_appointments(status);

-- ============================================================
-- 5. wa_escalations — Messages requiring human attention
-- ============================================================
CREATE TABLE IF NOT EXISTS wa_escalations (
    id BIGSERIAL PRIMARY KEY,
    phone TEXT NOT NULL,
    category TEXT NOT NULL,
    priority TEXT NOT NULL,
    original_message TEXT,
    original_message_id TEXT,
    escalation_target TEXT,
    status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'in_progress', 'resolved', 'closed')),
    resolved_at TIMESTAMPTZ,
    resolved_by TEXT,
    resolution_notes TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_escalations_status ON wa_escalations(status);
CREATE INDEX idx_escalations_priority ON wa_escalations(priority);
CREATE INDEX idx_escalations_phone ON wa_escalations(phone);

-- ============================================================
-- 6. wa_events — System events (connection, errors)
-- ============================================================
CREATE TABLE IF NOT EXISTS wa_events (
    id BIGSERIAL PRIMARY KEY,
    event TEXT NOT NULL,
    instance TEXT,
    state TEXT,
    details JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_events_event ON wa_events(event);
CREATE INDEX idx_events_created ON wa_events(created_at DESC);

-- ============================================================
-- 7. wa_metrics — Daily aggregated metrics
-- ============================================================
CREATE TABLE IF NOT EXISTS wa_metrics (
    id BIGSERIAL PRIMARY KEY,
    date DATE UNIQUE NOT NULL,
    total_messages INTEGER DEFAULT 0,
    inbound_messages INTEGER DEFAULT 0,
    outbound_messages INTEGER DEFAULT 0,
    unique_contacts INTEGER DEFAULT 0,
    urgent_count INTEGER DEFAULT 0,
    hot_lead_count INTEGER DEFAULT 0,
    appointment_count INTEGER DEFAULT 0,
    pricing_count INTEGER DEFAULT 0,
    avg_response_time_seconds INTEGER,
    conversion_to_appointment INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_metrics_date ON wa_metrics(date DESC);

-- ============================================================
-- 8. Row-level security (RLS)
-- ============================================================
ALTER TABLE wa_contacts ENABLE ROW LEVEL SECURITY;
ALTER TABLE wa_messages ENABLE ROW LEVEL SECURITY;
ALTER TABLE wa_conversations ENABLE ROW LEVEL SECURITY;
ALTER TABLE wa_appointments ENABLE ROW LEVEL SECURITY;
ALTER TABLE wa_escalations ENABLE ROW LEVEL SECURITY;
ALTER TABLE wa_events ENABLE ROW LEVEL SECURITY;
ALTER TABLE wa_metrics ENABLE ROW LEVEL SECURITY;

-- Allow service role full access (webhook handler uses service key)
CREATE POLICY "service_role_all" ON wa_contacts FOR ALL USING (auth.role() = 'service_role');
CREATE POLICY "service_role_all" ON wa_messages FOR ALL USING (auth.role() = 'service_role');
CREATE POLICY "service_role_all" ON wa_conversations FOR ALL USING (auth.role() = 'service_role');
CREATE POLICY "service_role_all" ON wa_appointments FOR ALL USING (auth.role() = 'service_role');
CREATE POLICY "service_role_all" ON wa_escalations FOR ALL USING (auth.role() = 'service_role');
CREATE POLICY "service_role_all" ON wa_events FOR ALL USING (auth.role() = 'service_role');
CREATE POLICY "service_role_all" ON wa_metrics FOR ALL USING (auth.role() = 'service_role');

-- ============================================================
-- 9. Functions — auto-update updated_at
-- ============================================================
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_contacts_updated_at BEFORE UPDATE ON wa_contacts
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_conversations_updated_at BEFORE UPDATE ON wa_conversations
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_appointments_updated_at BEFORE UPDATE ON wa_appointments
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ============================================================
-- 10. View — Recent messages dashboard
-- ============================================================
CREATE OR REPLACE VIEW wa_recent_messages AS
SELECT 
    m.id,
    m.created_at,
    m.phone,
    c.name AS contact_name,
    m.direction,
    m.text,
    m.category,
    m.priority,
    m.escalation_needed,
    m.confidence
FROM wa_messages m
LEFT JOIN wa_contacts c ON c.phone = m.phone
ORDER BY m.created_at DESC;

-- ============================================================
-- 11. View — Pending escalations
-- ============================================================
CREATE OR REPLACE VIEW wa_pending_escalations AS
SELECT
    e.id,
    e.created_at,
    e.phone,
    c.name AS contact_name,
    e.category,
    e.priority,
    e.original_message,
    e.escalation_target
FROM wa_escalations e
LEFT JOIN wa_contacts c ON c.phone = e.phone
WHERE e.status = 'pending'
ORDER BY 
    CASE e.priority
        WHEN 'URGENT' THEN 1
        WHEN 'HOT_LEAD' THEN 2
        WHEN 'APPOINTMENT' THEN 3
        WHEN 'PRICING' THEN 4
        ELSE 5
    END,
    e.created_at DESC;

-- ============================================================
-- 12. Sample data — Gaby's first messages
-- ============================================================
INSERT INTO wa_contacts (phone, name, first_message_at, last_message_at)
VALUES
    ('+595 987 126 790', 'Ometz Dental (Business)', NOW(), NOW())
ON CONFLICT (phone) DO NOTHING;

-- ============================================================
-- 13. Comments
-- ============================================================
COMMENT ON TABLE wa_contacts IS 'Master contact book for Ometz Dental WA Business';
COMMENT ON TABLE wa_messages IS 'All WhatsApp messages (inbound + outbound)';
COMMENT ON TABLE wa_conversations IS 'Aggregated conversation view per phone';
COMMENT ON TABLE wa_appointments IS 'Booked appointments via WhatsApp';
COMMENT ON TABLE wa_escalations IS 'Messages requiring human attention (URGENT, COMPLAINT, etc.)';
COMMENT ON TABLE wa_events IS 'System events (connection state, errors)';
COMMENT ON TABLE wa_metrics IS 'Daily aggregated metrics for dashboard';
