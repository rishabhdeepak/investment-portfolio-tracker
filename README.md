# WealthTrack — Investment Portfolio Tracker

A Django web application for tracking personal investments across stocks, mutual funds, ETFs, and more.
Users can manage multiple portfolios, log transactions, and monitor their holdings from a single dashboard.

> 🚧 **Active Development** — Profile dashboard in progress.

---

## What Makes This Different

Most portfolio trackers only handle stocks. WealthTrack is designed for multiple asset classes — stocks, mutual funds, ETFs, gold, fixed deposits, and more.

Holdings are **derived from transactions**, not stored manually — the same way real financial systems work.
Buy 10 TCS, sell 2 TCS → current holding is automatically 8 TCS.

---

## Features

### Currently Working
- User registration, login, and logout
- Custom user model (extensible for future fields)
- Portfolio, Asset, and Transaction models
- Derived holdings logic (quantity calculated from transactions)

### In Progress
- Portfolio dashboard

### Planned
- Live market data via yfinance (NSE/BSE supported)
- Profit/loss and average buy price per holding
- Interactive charts with Chart.js
- Portfolio Health Score (custom algorithm)
- CAGR & XIRR calculations
- Goal-based investment planner
- REST API with Django REST Framework
- Portfolio export (PDF / Excel)
- Deployment on Railway / Render

---

## Tech Stack

- **Backend:** Python, Django
- **Database:** SQLite (development) → PostgreSQL (production)
- **Frontend:** HTML5, Bootstrap 5, JavaScript

---

## Getting Started

```bash
git clone https://github.com/rishabhdeepak/investment-portfolio-tracker.git
cd investment-portfolio-tracker

python -m venv venv
venv\Scripts\activate        # Windows

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Open `http://127.0.0.1:8000` in your browser.

---

## Project Structure

```
investment-portfolio-tracker/
│
├── accounts/           # User model, registration, login, logout
├── portfolio/          # Portfolio, Asset, Transaction models + holdings logic
├── dashboard/          # Main dashboard views and templates
├── config/             # Django settings and root URLs
│
├── templates/          # HTML templates (organized by app)
├── static/             # CSS, JS, images
│
├── manage.py
└── requirements.txt
```

---

## Roadmap

- [x] Project setup and app structure
- [x] Custom user model with registration and login
- [x] Portfolio, Asset, and Transaction models
- [x] Derived holdings logic
- [ ] Dashboard with holdings summary
- [ ] Live market data with yfinance
- [ ] Profit/loss calculations
- [ ] Chart.js visualizations
- [ ] Portfolio Health Score
- [ ] Django REST Framework API
- [ ] Deployment

---

## Author

**Rishabh D**
B.Tech CSE, IIIT Kottayam
[github.com/rishabhdeepak](https://github.com/rishabhdeepak)
