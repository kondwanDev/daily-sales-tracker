# Daily Sales Tracker

A backend application built with **FastAPI** to help small shop owners record daily sales digitally and automatically calculate end-of-day sales totals.

This project was inspired by a real business where sales are recorded manually on paper, making end-of-day balancing slow and prone to human error.

---

## Problem

Many small retail businesses still record sales manually. At the end of each day, the shopkeeper has to add all recorded sales by hand and compare the total with the cash collected. This process is time-consuming and can lead to recording and calculation mistakes.

---

## Solution

Daily Sales Tracker provides a simple way to record sales digitally. The system automatically calculates sales totals, stores sales history, and lays the foundation for future features such as reporting and inventory management.

---

## Project Goals

* Record every sale digitally.
* Automatically calculate daily sales totals.
* Reduce manual calculation errors.
* Maintain a history of sales.
* Generate daily and historical sales reports.

---

## Tech Stack

* Python
* FastAPI
* PostgreSQL
* psycopg
* python-dotenv

---

## Project Structure

```text
daily-sales-tracker/
│
├── app/
├── docs/
├── sql/
├── tests/
├── .gitignore
├── .env.example
├── README.md
└── requirements.txt
```

---

## Documentation

Project documentation is located in the `docs/` directory.

---

## Development Status

🚧 This project is currently under active development.

---

## Future Enhancements

* Inventory management
* Profit analysis
* Expense tracking
* Customer credit management
* Sales analytics dashboard

---

## Author

Developed as a backend learning project using FastAPI while solving a real business problem.
