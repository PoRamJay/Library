-- Create the library database if it doesn't exist
CREATE DATABASE IF NOT EXISTS library_db;
USE library_db;

-- Create users table
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create collections table
CREATE TABLE collections (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    user_id INT,
    language VARCHAR(2) DEFAULT 'en',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Create books table
CREATE TABLE books (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(255) NOT NULL,
    isbn VARCHAR(13),
    year_published INT,
    publisher VARCHAR(255),
    genre VARCHAR(100),
    description TEXT,
    status VARCHAR(50) DEFAULT 'available',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Create collection_books junction table
CREATE TABLE collection_books (
    collection_id INT,
    book_id INT,
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (collection_id, book_id),
    FOREIGN KEY (collection_id) REFERENCES collections(id) ON DELETE CASCADE,
    FOREIGN KEY (book_id) REFERENCES books(id) ON DELETE CASCADE
);

-- Create admins table
CREATE TABLE admins (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create support_requests table
CREATE TABLE support_requests (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Sample data for testing
INSERT INTO books (title, author, isbn, year_published, publisher, genre, description) VALUES 
('The Great Gatsby', 'F. Scott Fitzgerald', '9780743273565', 1925, 'Scribner', 'Fiction', 'The story of the mysteriously wealthy Jay Gatsby and his love for the beautiful Daisy Buchanan.'),
('To Kill a Mockingbird', 'Harper Lee', '9780446310789', 1960, 'Grand Central Publishing', 'Fiction', 'The story of racial injustice and the loss of innocence in the American South.'),
('1984', 'George Orwell', '9780451524935', 1949, 'Signet Classic', 'Fiction', 'A dystopian social science fiction novel that examines the consequences of totalitarianism.'),
('Pride and Prejudice', 'Jane Austen', '9780141439518', 1813, 'Penguin Classics', 'Fiction', 'A romantic novel of manners that follows the character development of Elizabeth Bennet.');

-- Language codes reference:
-- en: English
-- es: Spanish
-- fr: French
-- de: German
-- it: Italian
-- pt: Portuguese
-- ru: Russian
-- zh: Chinese
-- ja: Japanese
-- ko: Korean

-- If you need to update existing collections table to add the language column, run:
-- ALTER TABLE collections ADD COLUMN language VARCHAR(2) DEFAULT 'en';
-- ALTER TABLE collections ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP; 