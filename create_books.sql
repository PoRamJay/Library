-- Create books table if it doesn't exist
CREATE TABLE IF NOT EXISTS books (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(255) NOT NULL,
    isbn VARCHAR(13),
    publication_year INT,
    publisher VARCHAR(255),
    category VARCHAR(100),
    description TEXT,
    status VARCHAR(50) DEFAULT 'available',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Insert a sample book
INSERT INTO books (title, author, isbn, publication_year, publisher, category, description)
VALUES (
    'The Great Gatsby',
    'F. Scott Fitzgerald',
    '9780743273565',
    1925,
    'Scribner',
    'Fiction',
    'The story of the mysteriously wealthy Jay Gatsby and his love for the beautiful Daisy Buchanan.'
);

-- You can add more books using similar INSERT statements:
INSERT INTO books (title, author, isbn, publication_year, publisher, category, description)
VALUES (
    'To Kill a Mockingbird',
    'Harper Lee',
    '9780446310789',
    1960,
    'Grand Central Publishing',
    'Fiction',
    'The story of racial injustice and the loss of innocence in the American South.'
); 