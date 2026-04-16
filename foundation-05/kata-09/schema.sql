CREATE TABLE IF NOT EXISTS gdp_observations (
  date TEXT PRIMARY KEY,
  value REAL NOT NULL,
  growth_rate REAL
);
