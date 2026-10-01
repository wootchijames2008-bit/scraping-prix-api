📚 Book Price Tracker & FastAPI

A Python project that combines a web scraper and a FastAPI backend to collect, monitor, and synchronize book prices.

🚀 Features

Web Scraper

- Scrapes book data from "Books to Scrape" (https://books.toscrape.com/)
- Collects book titles, prices, ratings, and stock information
- Saves scraped data locally
- Tracks historical prices
- Detects price changes
- Detects good deals
- Logs application activity
- Supports Telegram notifications

FastAPI Backend

- REST API built with FastAPI
- SQLite database with SQLAlchemy
- Create, read, update, and delete books
- Partial updates with "PATCH"
- Price filtering and sorting
- Stock filtering
- Rating filtering
- Input validation with Pydantic
- Automated API tests with pytest

🔄 Scraper ↔ API synchronization

The scraper can communicate with the FastAPI backend.

When a book is scraped:

- If the book does not exist in the API database, it can be created.
- If the book already exists, its current price can be compared with the stored price.
- When the price changes, the API can be updated using "PATCH".

This allows the scraper and API to work together as a small price-tracking system.

🏗️ Project Structure

scraping-prix-api/
│
├── book_api/
│   ├── main.py
│   ├── database.py
│   ├── model.py
│   ├── shemas.py
│   ├── conftest.py
│   ├── test_api.py
│   └── routers/
│       └── livres.py
│
├── scraping_prix v2 -- the comeback/
│   ├── main.py
│   ├── scraper.py
│   ├── sauvegarde.py
│   ├── price_history.py
│   ├── price_checker.py
│   ├── price_change.py
│   ├── notification.py
│   ├── logs.py
│   └── config.py
│
└── README.md

🛠️ Technologies

- Python
- FastAPI
- SQLAlchemy
- SQLite
- BeautifulSoup
- Requests
- Pydantic
- Pytest
- Git & GitHub

🧪 Tests

The FastAPI project currently has 12 passing tests.

Run the tests from the API directory:

cd book_api
pytest

🔐 Security

Sensitive information such as API tokens and credentials should not be stored directly in the repository.

Use environment variables or another secure configuration method for secrets.

📌 Project Status

The project is currently under development.

The scraper and FastAPI backend are functional and are being progressively improved and integrated.

👤 Author

James Wootchi

Built as a personal Python learning project focused on web scraping, APIs, databases, testing, and automation.
