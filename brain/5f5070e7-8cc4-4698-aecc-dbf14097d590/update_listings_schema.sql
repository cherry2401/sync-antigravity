-- Add missing columns to bds_listings to match frontend Listing interface
ALTER TABLE bds_listings ADD COLUMN IF NOT EXISTS bedrooms text;
ALTER TABLE bds_listings ADD COLUMN IF NOT EXISTS bathrooms text;
ALTER TABLE bds_listings ADD COLUMN IF NOT EXISTS direction text;
ALTER TABLE bds_listings ADD COLUMN IF NOT EXISTS furniture text;
ALTER TABLE bds_listings ADD COLUMN IF NOT EXISTS legal text;
ALTER TABLE bds_listings ADD COLUMN IF NOT EXISTS floors text;
ALTER TABLE bds_listings ADD COLUMN IF NOT EXISTS project text;
ALTER TABLE bds_listings ADD COLUMN IF NOT EXISTS street text;
ALTER TABLE bds_listings ADD COLUMN IF NOT EXISTS ward text;
ALTER TABLE bds_listings ADD COLUMN IF NOT EXISTS entrance_width text;
ALTER TABLE bds_listings ADD COLUMN IF NOT EXISTS frontage_width text;
ALTER TABLE bds_listings ADD COLUMN IF NOT EXISTS price_unit text;
