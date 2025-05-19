-- SQL script to create the 'book_log' table for book borrowing records
CREATE TABLE book_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    book_title VARCHAR(255) NOT NULL,
    book_author VARCHAR(255),
    borrower_name VARCHAR(255) NOT NULL,
    borrower_date DATE NOT NULL,
    returner_date DATE NOT NULL,
    status ENUM('Returned', 'Overdue') NOT NULL,
    transaction_id VARCHAR(32) NOT NULL UNIQUE
);

-- Optional: Add indexes for faster lookups
CREATE INDEX idx_borrower_name ON book_log(borrower_name);
CREATE INDEX idx_status ON book_log(status);
CREATE INDEX idx_transaction_id ON book_log(transaction_id); 