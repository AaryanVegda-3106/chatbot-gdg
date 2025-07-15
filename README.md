# University probe assistant

## Description
This is a Python project that appears to be a web application, possibly interacting with a database given the presence of `database.py`. It also includes an admin section, as indicated by `pages/admin.py`.

## Live demo
https://chatbot-gdg-prototype.streamlit.app/

## Features
- Web application functionality (implied by `app.py`)
- Database integration (implied by `database.py`)
- Admin interface (implied by `pages/admin.py`)

## Installation
To set up this project locally, follow these steps:

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd <project-directory>
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Database Setup (if applicable):**
   Depending on `database.py`, you might need to set up a database. Refer to the comments or documentation within `database.py` for specific instructions.

## Usage
To run the application:

```bash
streamlit app.py
```

After running, the application should be accessible via your web browser, typically at `http://127.0.0.1:5000` or a similar address.


## admin credentials
username: admin
password: admin123