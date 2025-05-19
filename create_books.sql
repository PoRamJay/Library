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

INSERT INTO books (title, author, isbn, publication_year, publisher, category, description)
VALUES (
    'We Were Liars',
    'E. Lockhart',
    '9780385741279',
    2014,
    'Delacorte Press',
    'Young Adult Fiction',
    'A suspenseful, modern novel about privilege, secrets, and a group of teenagers on a private island with a shocking twist.'
);

INSERT INTO books (title, author, isbn, publication_year, publisher, category, description)
VALUES (
    'The 48 Laws of Power',
    'Robert Greene',
    '9780140280197',
    1998,
    'Penguin Books',
    'Self-Help',
    'A guide to understanding and wielding power through historical examples, psychological insights, and strategic principles.'
);

INSERT INTO books (title, author, isbn, publication_year, publisher, category, description)
VALUES (
    'Bridgerton: The Viscount Who Loved Me',
    'Julia Quinn',
    '9780062353658',
    2000,
    'Avon Books',
    'Historical Romance',
    'The second novel in the Bridgerton series, following Anthony Bridgerton as he sets out to find a wife—only to fall for his intended’s headstrong sister.'
);

INSERT INTO books (title, author, isbn, publication_year, publisher, category, description)
VALUES (
    'A Game of Thrones',
    'George R. R. Martin',
    '9780553573404',
    1996,
    'Bantam Books',
    'Fantasy',
    'The first book in the epic fantasy series *A Song of Ice and Fire*, where noble families vie for control of the Iron Throne in a land of betrayal, power, and ancient magic.'
);

INSERT INTO books (title, author, isbn, publication_year, publisher, category, description)
VALUES (
    'Milk and Honey',
    'Rupi Kaur',
    '9781449474256',
    2014,
    'Andrews McMeel Publishing',
    'Poetry',
    'A collection of poetry and prose about survival, love, loss, trauma, and femininity, divided into four chapters that each serve a different purpose.'
);

INSERT INTO books (title, author, isbn, publication_year, publisher, category, description)
VALUES (
    'The 5 Love Languages',
    'Gary Chapman',
    '9780802412706',
    1992,
    'Northfield Publishing',
    'Relationships',
    'A practical guide that explains the five distinct ways people give and receive love—words of affirmation, acts of service, receiving gifts, quality time, and physical touch—to help improve communication and connection in relationships.'
);

INSERT INTO books (title, author, isbn, publication_year, publisher, category, description)
VALUES (
    'Artemis Fowl',
    'Eoin Colfer',
    '9780786808014',
    2001,
    'Hyperion Books for Children',
    'Fantasy',
    'A twelve-year-old criminal mastermind, Artemis Fowl, kidnaps a fairy in hopes of restoring his family\'s fortune, but discovers a hidden world of magic and danger.'
);
INSERT INTO books (title, author, isbn, publication_year, publisher, category, description)
VALUES (
    'Atomic Habits',
    'James Clear',
    '9780735211292',
    2018,
    'Avery',
    'Self-help',
    'An easy & proven way to build good habits and break bad ones.'
);

INSERT INTO books (title, author, isbn, publication_year, publisher, category, description)
VALUES (
    'Harry Potter and the Cursed Child',
    'J.K. Rowling, John Tiffany, Jack Thorne',
    '9781338216660',
    2016,
    'Little, Brown',
    'Fantasy',
    'The eighth story in the Harry Potter series, presented as a stage play script, focusing on Harry Potter\'s son Albus.'
),

INSERT INTO books (title, author, isbn, publication_year, publisher, category, description)
VALUES (
    'The Complete Sherlock Holmes',
    'Arthur Conan Doyle',
    '9780553328257',
    1986,
    'Bantam Classics',
    'Mystery',
    'A comprehensive collection of all Sherlock Holmes stories including novels and short stories.'
);
