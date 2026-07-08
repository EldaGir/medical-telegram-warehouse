# Telegram Medical Data Warehouse

## Overview

This project is part of a data engineering pipeline designed to collect, transform, and analyze data from Ethiopian medical-related Telegram channels.

The project extracts messages and media from selected Telegram channels using the Telegram API, stores the raw data in a data lake, and later transforms the data into a structured PostgreSQL data warehouse using dbt and dimensional modeling for analytics.

---

## Project Objectives

- Scrape messages from multiple Telegram channels
- Download associated media (images, documents, etc.)
- Store raw data in JSON format
- Maintain logs for monitoring and debugging
- Load raw data into PostgreSQL
- Transform raw data using dbt
- Build a dimensional (Star Schema) data warehouse
- Generate documentation and data quality tests

---

## Technologies Used

- Python 3.14
- Telethon
- PostgreSQL
- dbt (dbt-postgres)
- Git & GitHub
- python-dotenv
- JSON

---

## Project Structure

```
telegram-medical-data-warehouse/
│
├── data/
│
├── logs/
│   └── scraper.log
│
├── telegram_messages/
│   └── YYYY-MM-DD/
│       ├── messages.json
│       └── media/
│
├── src/
│   ├── scraper.py
│   └── ...
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

---

## Features

### Telegram Data Scraping

- Connects to the Telegram API using Telethon
- Reads API credentials from environment variables
- Scrapes multiple Ethiopian medical-related Telegram channels
- Supports configurable message limits

### Media Download

- Downloads message media (images and documents)
- Stores media alongside scraped messages
- Avoids unnecessary downloads during repeated runs

### Data Storage

- Saves scraped messages in structured JSON format
- Organizes outputs by execution date
- Maintains a clean data lake structure

### Logging

- Logs scraper activity
- Records execution status and errors
- Simplifies debugging and monitoring

---

## Installation

### 1. Clone the repository

```bash
git clone <https://github.com/EldaGir/medical-telegram-warehouse.git>
cd telegram-medical-data-warehouse
```

---

### 2. Create a virtual environment

```bash
python -m venv .venv
```

---

### 3. Activate the virtual environment

Windows

```bash
.venv\Scripts\activate
```

Git Bash

```bash
source .venv/Scripts/activate
```

Linux/macOS

```bash
source .venv/bin/activate
```

---

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file in the project root and add your Telegram API credentials.

```
API_ID=your_api_id
API_HASH=your_api_hash
PHONE_NUMBER=your_phone_number
```

> **Note:** Never commit your `.env` file to GitHub.

---

## Running the Scraper

Execute the scraper using

```bash
python src/scraper.py
```

The scraper will:

- Connect to Telegram
- Retrieve messages from the configured channels
- Download media files
- Save message data as JSON
- Generate execution logs

---

## Output

### Raw Messages

```
telegram_messages/
    YYYY-MM-DD/
        messages.json
```

### Downloaded Media

```
telegram_messages/
    YYYY-MM-DD/
        media/
```

### Logs

```
logs/
    scraper.log
```

---

## Project Workflow

```
Telegram Channels
        │
        ▼
 Telegram API (Telethon)
        │
        ▼
 Python Scraper
        │
        ▼
 Raw JSON Files + Media
        │
        ▼
 PostgreSQL (Raw Layer)
        │
        ▼
 dbt Transformations
        │
        ▼
 Star Schema Data Warehouse
        │
        ▼
 Analytics & Reporting
```

---

## Development Progress

### ✅ Task 1 — Data Collection

- Telegram API authentication
- Multi-channel scraping
- Media downloading
- JSON storage
- Logging
- Configurable message limits

### 🔄 Task 2 — Data Modeling and Transformation

- Load JSON into PostgreSQL
- Initialize dbt project
- Create staging models
- Build dimensional models
- Implement dbt tests
- Generate dbt documentation

### ⏳ Task 3

To be implemented.

---

## Notes

- API credentials are stored securely using environment variables.
- The repository excludes sensitive files through `.gitignore`.
- Output folders are generated automatically based on the execution date.

---

## Author

**Elda**


Financial AI Mastering Program