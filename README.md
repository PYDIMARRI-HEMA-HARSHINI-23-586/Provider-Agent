# Provider Agent Validator

This project is a comprehensive system for validating healthcare provider data using a modular, agent-based architecture. It fetches provider information, validates it against external public APIs, extracts data from PDFs, and presents the results in an interactive web dashboard and through a command-line interface.

## Features

- **NPI Validation:** An agent validates provider NPI (National Provider Identifier) data against the official NPI registry API.
- **Address Validation:** An agent validates physical addresses using the OpenStreetMap Nominatim API.
- **PDF Data Extraction:** Ingests provider data from PDF documents using an OCR-powered agent.
- **Confidence Scoring:** Each validation (NPI, Address) is assigned a confidence score, allowing for nuanced data quality assessment.
- **Interactive Dashboard:** A web dashboard built with Streamlit provides a comprehensive view of provider data, validation statuses (Validated, Review, Invalid, Pending), and confidence score distributions.
- **Terminal Validator:** A command-line script to perform on-demand validation for provider data stored in a simple text file.
- **Database Backend:** Uses SQLite to store and manage provider records.

## How It Works

The system is composed of several key components:

1.  **Database:** A SQLite database (`providers.db`) stores the provider information. The schema is defined in `app/models.py` using SQLAlchemy.
2.  **Validation Agents (`app/`):**
    *   `npi_agent.py`: Fetches provider data and queries the NPI API.
    *   `address_agent.py`: Fetches provider data and queries the OpenStreetMap Nominatim API.
    *   `pdf_agent.py`: Contains the logic for processing PDFs with OCR to extract provider information.
3.  **Dashboard (`dashboard.py`):**
    *   A Streamlit application that provides a web interface to view all provider data.
    *   It features a PDF validation page where users can upload a document for extraction and on-the-fly validation.
4.  **Terminal Validator (`terminal_validator.py`):**
    *   A standalone script that reads provider data from `app/data.txt`, runs the core validation logic, and prints a final "Valid" or "Invalid" status to the console.

## Getting Started

### Prerequisites

- Python 3.x
- pip
- Tesseract-OCR: Must be installed on your system. You may need to update the path in `app/pdf_agent.py`.
- Poppler: Must be installed on your system. You may need to update the path in `app/pdf_agent.py`.

### Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd provider-agent
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows, use: .venv\Scripts\activate
    ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

### Usage

#### 1. Set Up the Database

First, create the database schema and populate it with sample data:
```bash
python -m app.seed
```
This creates `providers.db` and seeds it with 200 fake provider records.

#### 2. Run the Web Dashboard

To launch the main application:
```bash
streamlit run dashboard.py
```
- Navigate to the URL provided by Streamlit (usually `http://localhost:8501`).
- From the dashboard, you can view all provider data.
- Use the sidebar navigation to go to the "PDF Validation" page to test the PDF extraction feature. You can use `valid_test_provider.pdf` for this (this PDF is generated with real, verifiable data to demonstrate the solution's effectiveness with real-world inputs).

#### 3. Run Batch Validations (Optional)

You can run the agents directly from the terminal to perform batch validations on the data in the database:
```bash
# Run NPI validation on a batch of providers
python -m app.npi_agent

# Run Address validation on a batch of providers
python -m app.address_agent
```

#### 4. Use the Terminal Validator

To validate the specific data in `app/data.txt`:
```bash
python terminal_validator.py
```
This will run both NPI and Address validation on the data in the file and print a final status to your terminal.

## Technology Stack

- **Backend:** Python
- **Database:** SQLite with SQLAlchemy (ORM)
- **Web Dashboard:** Streamlit
- **PDF Processing:**
    - `pytesseract` for OCR
    - `reportlab` for PDF generation
- **Data Validation:** `requests` (for external APIs)
- **Data Seeding:** `Faker`