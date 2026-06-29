-- Create users tabe
-- depends:

-- migrate: apply
CREATE TABLE IF NOT EXISTS users (
    user_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username VARCHAR(50) NOT NULL,
    password VARCHAR(255),
    role VARCHAR(10) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    email_verified bool NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW(),
    created_by UUID REFERENCES users(user_id),
    updated_at TIMESTAMPTZ,
    updated_by UUID REFERENCES users(user_id),
    deleted_at TIMESTAMPTZ,
    deleted_by UUID REFERENCES users(user_id)
);


-- migrate: rollback

DROP TABLE IF EXISTS users;
