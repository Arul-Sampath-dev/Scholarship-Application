-- Create provider table
-- depends: 20260625_01_nkbov-create-users-tabe

-- migrate: apply

CREATE TABLE IF NOT EXISTS providers (
    provider_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    provider_name VARCHAR(255) NOT NULL,
    user_id UUID REFERENCES users(user_id),
    created_at TIMESTAMPTZ DEFAULT NOW()
);


-- migrate: rollback
DROP TABLE IF EXISTS providers;
