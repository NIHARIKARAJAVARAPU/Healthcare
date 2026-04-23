CREATE TABLE IF NOT EXISTS hcp_interactions (
    id SERIAL PRIMARY KEY,
    hcp_name VARCHAR(255) NOT NULL,
    interaction_type VARCHAR(100) NOT NULL,
    interaction_datetime TIMESTAMP NOT NULL,
    attendees JSONB NOT NULL DEFAULT '[]'::jsonb,
    topics_discussed TEXT NOT NULL DEFAULT '',
    materials_shared JSONB NOT NULL DEFAULT '[]'::jsonb,
    samples_distributed JSONB NOT NULL DEFAULT '[]'::jsonb,
    sentiment VARCHAR(50) NOT NULL DEFAULT 'Neutral',
    outcomes TEXT NOT NULL DEFAULT '',
    follow_up_actions JSONB NOT NULL DEFAULT '[]'::jsonb,
    next_step TEXT NOT NULL DEFAULT '',
    compliance_notes TEXT NOT NULL DEFAULT '',
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);
