-- User Model
CREATE TABLE IF NOT EXISTS users (
    user_id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    email VARCHAR NOT NULL,
    password VARCHAR NOT NULL,
    membership_date DATE NOT NULL
);

-- Book Model
CREATE TABLE IF NOT EXISTS books (
    book_id SERIAL PRIMARY KEY,
    title VARCHAR NOT NULL,
    isbn VARCHAR NOT NULL,
    published_date DATE NOT NULL,
    genre VARCHAR NOT NULL
);

-- BookDetails Model
CREATE TABLE IF NOT EXISTS book_details (
    details_id SERIAL PRIMARY KEY,
    book_id INTEGER REFERENCES books(book_id) UNIQUE,
    number_of_pages INTEGER NOT NULL,
    publisher VARCHAR NOT NULL,
    language VARCHAR NOT NULL
);

-- BorrowedBooks Model
CREATE TABLE IF NOT EXISTS borrowed_books (
    user_id INTEGER REFERENCES users(user_id),
    book_id INTEGER REFERENCES books(book_id),
    borrow_date DATE NOT NULL,
    return_date DATE,
    PRIMARY KEY (user_id, book_id)
);