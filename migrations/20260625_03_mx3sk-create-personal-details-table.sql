-- Create Personal Details Table
-- depends: 20260625_02_6i1p7-create-provider-table

-- migrate: apply
CREATE TABLE IF NOT EXISTS personal_details (
    user_id UUID PRIMARY KEY REFERENCES users(user_id),
    date_of_birth DATE NOT NULL,
    gender VARCHAR(10) NOT NULL,
    phone_number VARCHAR(12) NOT NULL,
    alternate_phone_number VARCHAR(12),
    nationality VARCHAR(50) NOT NULL,
    street VARCHAR(255) NOT NULL,
    city VARCHAR(50) NOT NULL,
    district VARCHAR(50) NOT NULL,
    state VARCHAR(50) NOT NULL,
    pin_code VARCHAR(10) NOT NULL,
    country VARCHAR(50) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    created_by UUID REFERENCES users(user_id) NOT NULL,
    updated_at TIMESTAMPTZ,
    updated_by UUID REFERENCES users(user_id)
);


-- migrate: rollback
DROP TABLE IF EXISTS personal_details;
