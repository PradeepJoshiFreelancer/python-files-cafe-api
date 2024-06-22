# Flask REST API Project

This project demonstrates a simple REST API built using Flask, SQLAlchemy, and SQLite. It manages a collection of cafes with various attributes.

## Installation

To run this project, ensure you have Python 3.x and pip installed. Use the following command to install the required dependencies:

```bash
pip install -r requirements.txt
```

This will install Flask and SQLAlchemy.

## Usage

1. **Run the Application**: Execute `python app.py` to start the Flask server.
2. **Endpoints**:
   - `/random`: GET a random cafe from the database.
   - `/all`: GET all cafes from the database.
   - `/search?loc=<location>`: GET cafes by location.
   - `/add` (POST): Add a new cafe.
   - `/update/<int:cafe_id>` (PATCH): Update coffee price for a cafe.
   - `/report-closed/<int:cafe_id>` (DELETE): Delete a cafe record (authorization required).

## Database

- **cafes.db**: SQLite database file located in the root directory.
- **Cafe Table Schema**:
  - `id`: Primary key (integer).
  - `name`: Cafe name (string).
  - `map_url`: URL for cafe location map (string).
  - `img_url`: URL for cafe image (string).
  - `location`: Cafe location (string).
  - `seats`: Number of seats available (string).
  - `has_toilet`: Boolean indicating presence of a toilet.
  - `has_wifi`: Boolean indicating presence of WiFi.
  - `has_sockets`: Boolean indicating presence of power sockets.
  - `can_take_calls`: Boolean indicating if cafe allows phone calls.
  - `coffee_price`: Price of coffee (string).

## API Documentation

- **GET /random**: Retrieve a random cafe.
- **GET /all**: Retrieve all cafes.
- **GET /search?loc=<location>**: Search cafes by location.
- **POST /add**: Add a new cafe.
- **PATCH /update/<int:cafe_id>?coffee_price=<new_price>**: Update coffee price for a cafe.
- **DELETE /report-closed/<int:cafe_id>?key=<key>**: Delete a cafe record (requires authorization key).

## Notes

- This project uses SQLite for local database storage.
- Ensure proper authorization (`key="TOP-SECRET"`) for DELETE requests.
- For PATCH requests, provide `coffee_price` as a query parameter.

