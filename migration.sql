-- Migration script for library database updates
USE library_db;

-- Add timestamps to users table if they don't exist
ALTER TABLE users
ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

-- Update collections table
ALTER TABLE collections
ADD COLUMN IF NOT EXISTS language VARCHAR(2) DEFAULT 'en',
ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
ADD COLUMN IF NOT EXISTS user_id INT,
ADD FOREIGN KEY IF NOT EXISTS (user_id) REFERENCES users(id);

-- Update books table
ALTER TABLE books
ADD COLUMN IF NOT EXISTS isbn VARCHAR(13),
ADD COLUMN IF NOT EXISTS year_published INT,
ADD COLUMN IF NOT EXISTS publisher VARCHAR(255),
ADD COLUMN IF NOT EXISTS genre VARCHAR(100),
ADD COLUMN IF NOT EXISTS description TEXT,
ADD COLUMN IF NOT EXISTS status VARCHAR(50) DEFAULT 'available',
ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP;

-- Create collection_books junction table if it doesn't exist
CREATE TABLE IF NOT EXISTS collection_books (
    collection_id INT,
    book_id INT,
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (collection_id, book_id),
    FOREIGN KEY (collection_id) REFERENCES collections(id) ON DELETE CASCADE,
    FOREIGN KEY (book_id) REFERENCES books(id) ON DELETE CASCADE
);

-- Create admins table if it doesn't exist
CREATE TABLE IF NOT EXISTS admins (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create support_requests table if it doesn't exist
CREATE TABLE IF NOT EXISTS support_requests (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Add sample books data if books table is empty
INSERT IGNORE INTO books (title, author, isbn, year_published, publisher, genre, description) 
SELECT * FROM (
    SELECT 'The Great Gatsby', 'F. Scott Fitzgerald', '9780743273565', 1925, 'Scribner', 'Fiction', 'The story of the mysteriously wealthy Jay Gatsby and his love for the beautiful Daisy Buchanan.'
    UNION ALL
    SELECT 'To Kill a Mockingbird', 'Harper Lee', '9780446310789', 1960, 'Grand Central Publishing', 'Fiction', 'The story of racial injustice and the loss of innocence in the American South.'
    UNION ALL
    SELECT '1984', 'George Orwell', '9780451524935', 1949, 'Signet Classic', 'Fiction', 'A dystopian social science fiction novel that examines the consequences of totalitarianism.'
    UNION ALL
    SELECT 'Pride and Prejudice', 'Jane Austen', '9780141439518', 1813, 'Penguin Classics', 'Fiction', 'A romantic novel of manners that follows the character development of Elizabeth Bennet.'
) AS tmp
WHERE NOT EXISTS (SELECT 1 FROM books LIMIT 1); 