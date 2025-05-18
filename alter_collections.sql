-- Add language column to collections table
ALTER TABLE collections
ADD COLUMN language VARCHAR(2) DEFAULT 'en';

-- Update existing collections to have English as default language
UPDATE collections SET language = 'en' WHERE language IS NULL; 