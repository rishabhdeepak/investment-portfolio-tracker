# WealthTrack — Investment Portfolio Tracker

WealthTrack is a full-stack Django application for tracking investment portfolios across multiple asset classes. Users can manage multiple portfolios, record transactions, monitor real-time portfolio performance, and analyze their investments through a unified dashboard.

> 🚧 **Active Development** — Mutual Fund support is the next major milestone.

---

## What Makes WealthTrack Different

Unlike many beginner portfolio trackers that store holdings directly, WealthTrack derives holdings entirely from transaction history—the same approach used by professional portfolio management systems.

Example:

```
Buy 10 TCS
Sell 2 TCS

Current Holding = 8 TCS
```

This ensures portfolio data is always consistent, accurate, and auditable.

The application is also designed from the ground up to support multiple asset classes such as stocks, mutual funds, ETFs, gold, and more through a unified architecture.

---

## Features

### ✅ Currently Working

- User authentication (Registration, Login, Logout)
- Custom User model
- Multiple portfolio management
- Asset and transaction management
- Automatic holdings calculation from transaction history
- Average cost basis calculation
- Profit & Loss calculation
- Portfolio summaries
- Individual asset detail pages
- Dashboard analytics
  - Total invested
  - Current portfolio value
  - Total profit/loss
  - Overall return percentage
  - Stock allocation
  - Sector allocation
- Redis caching
- Celery & Celery Beat background tasks
- Automatic market price updates using yfinance
- Transaction validation

### 🚧 In Progress

- Mutual Fund support

### 📌 Planned

- Interactive charts (Chart.js)
- Portfolio Health Score
- CAGR & XIRR calculations
- Goal-based investment planner
- REST API using Django REST Framework
- PDF & Excel portfolio exports
- Professional responsive UI/UX
- PostgreSQL production deployment
- Docker support

---

## Tech Stack

### Backend
- Python
- Django
- Django ORM

### Database
- SQLite (Development)
- PostgreSQL (Production)

### Background Tasks
- Celery
- Celery Beat
- Redis

### Market Data
- yfinance

### Frontend
- HTML5
- Bootstrap 5
- JavaScript

### Planned
- Django REST Framework
- Chart.js

---

## Architecture

```
                Browser
                   │
                   ▼
               Django Views
                   │
                   ▼
          Dashboard Services
                   │
                   ▼
              Django Models
                   │
                   ▼
               PostgreSQL

          ▲
          │
 Celery + Redis + Beat
          │
          ▼
   Market Data (yfinance)
```

---

## Getting Started

```bash
git clone https://github.com/rishabhdeepak/investment-portfolio-tracker.git

cd investment-portfolio-tracker

python -m venv venv

# Windows
venv\Scripts\activate

# Linux / macOS
source venv/bin/activate

pip install -r requirements.txt

python manage.py migrate

python manage.py runserver
```

Open your browser and visit:

```
http://127.0.0.1:8000/
```

---

## Project Structure

```
investment-portfolio-tracker/
│
├── accounts/          # Authentication & Custom User Model
├── dashboard/         # Dashboard views and analytics services
├── portfolio/         # Portfolio, Asset & Transaction logic
├── config/            # Django settings & URLs
│
├── templates/
├── static/
│
├── manage.py
└── requirements.txt
```

---

## Roadmap

- [x] Authentication System
- [x] Custom User Model
- [x] Portfolio Management
- [x] Transaction Engine
- [x] Holdings Calculation Engine
- [x] Portfolio Summary Calculations
- [x] Asset Detail Pages
- [x] Dashboard Analytics
- [x] Redis Caching
- [x] Celery & Celery Beat Integration
- [ ] Mutual Fund Support
- [ ] REST API (Django REST Framework)
- [ ] Interactive Charts (Chart.js)
- [ ] Portfolio Health Score
- [ ] Goal-Based Investment Planner
- [ ] PDF / Excel Export
- [ ] Responsive UI/UX Improvements
- [ ] PostgreSQL Production Deployment
- [ ] Docker Support

---

## Future Vision

WealthTrack is being built as a professional portfolio management platform rather than a simple CRUD project. The long-term goal is to support multiple investment instruments, provide advanced portfolio analytics, expose a REST API, and offer a modern, production-ready user experience.

---

## Author

**Rishabh D**

B.Tech Computer Science & Engineering  
IIIT Kottayam

GitHub: https://github.com/rishabhdeepak