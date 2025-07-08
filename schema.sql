CREATE TABLE reports (
    id SERIAL PRIMARY KEY,
    slug VARCHAR(255) NOT NULL UNIQUE,
    text TEXT NOT NULL,
    date_created TIMESTAMPTZ DEFAULT NOW(),
    date_updated TIMESTAMPTZ
);
