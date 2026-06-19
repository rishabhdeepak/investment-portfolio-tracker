# WealthTrack — Investment Portfolio Tracker

A Django web application for tracking personal investment portfolios. Users can manage their stock holdings, monitor performance, and gain insight into their portfolio composition.

> 🚧 **Active Development** — Core functionality is working. Features like live market data, REST API, and charts are in progress.

---

## Features

### Currently Working
- Add, edit, and delete stock holdings manually
- Portfolio dashboard

### In Progress
- Live market data via yfinance
- Portfolio performance charts (Chart.js)
- REST API with Django REST Framework
- JWT-based API authentication
- Portfolio health score (custom algorithm)
- Investment goal planner

---

## Tech Stack

- **Backend:** Python, Django
- **Database:** SQLite (development)
- **Frontend:** HTML, CSS (Django templates)

---

## Getting Started

```bash
# Clone the repo
git clone https://github.com/rishabhdeepak/investment-portfolio-tracker.git
cd investment-portfolio-tracker

# Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start the development server
python manage.py runserver
```

Then open `http://127.0.0.1:8000` in your browser.

---

## Project Structure

```
investment-portfolio-tracker/
├── accounts/       # User authentication
├── config/         # Project settings and URLs
├── dashboard/      # Portfolio dashboard views
├── portfolio/      # Core portfolio and holdings logic
├── templates/      # HTML templates
└── manage.py
```

---

## Roadmap

- [x] Project setup and app structure
- [x] User authentication
- [ ] Manual stock holding entry
- [ ] Live price data with yfinance
- [ ] Portfolio charts with Chart.js
- [ ] REST API with Django REST Framework
- [ ] JWT authentication for API
- [ ] Portfolio health score
- [ ] Goal planner
- [ ] Deployment (Railway / Render)

---

## Author

**Rishabh Deepak** — [github.com/rishabhdeepak](https://github.com/rishabhdeepak)
