# Family Money App 💰

A web-based financial management application for family budgeting, cashflow tracking, and investment overview.

## Features (Planned)

- ✅ **Budgeting** - Create and track budgets by category
- 🔄 **Cashflow Tracking** - Monitor income and expenses over time
- 🔄 **Investment Overview** - Track and visualize investment portfolio
- 📊 **Dashboard** - Visual overview of family financial health

## Tech Stack

### Backend
- **FastAPI** - Modern, fast Python web framework
- **SQLAlchemy** - ORM for database management
- **SQLite** - Database (can migrate to PostgreSQL later)
- **Pydantic** - Data validation

### Frontend
- **React** - UI framework
- **Vite** - Build tool and dev server
- **Tailwind CSS** - Responsive styling
- **Recharts** - Data visualization
- **TypeScript** - Type safety

## Project Structure

```
money-app/
├── backend/          # FastAPI application
│   ├── app/
│   │   ├── api/      # API routes
│   │   ├── models/   # Database models
│   │   ├── schemas/  # Pydantic schemas
│   │   └── main.py   # FastAPI app
│   └── requirements.txt
├── frontend/         # React application
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── App.tsx
│   └── package.json
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.8+ 
- Node.js 18+ and npm
- (Optional) A virtual environment tool like `venv` or `virtualenv`

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. (Optional) Seed the database with sample data:
```bash
python app/seed_data.py
```

5. Start the backend server:
```bash
uvicorn app.main:app --reload
```

The backend will run on `http://localhost:8000`
- API docs (Swagger UI): `http://localhost:8000/docs`
- Alternative API docs (ReDoc): `http://localhost:8000/redoc`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The frontend will run on `http://localhost:5173`

### First Steps

1. Start both backend and frontend servers (in separate terminals)
2. Visit `http://localhost:5173` in your browser
3. If you seeded the database, you'll see sample budgets and transactions
4. If not, create categories first, then create budgets and add transactions

## Architecture Overview

### Backend (FastAPI)

- **RESTful API** with automatic OpenAPI documentation
- **SQLAlchemy ORM** for database operations
- **Pydantic** for data validation and serialization
- **SQLite** database (easily migratable to PostgreSQL)

### Frontend (React + TypeScript)

- **React Router** for navigation
- **Axios** for API communication
- **Recharts** for data visualization
- **Tailwind CSS** for responsive, modern styling
- **TypeScript** for type safety

### Data Models

- **Categories**: Organize your expenses (Groceries, Transportation, etc.)
- **Budgets**: Set spending limits by category and period
- **Transactions**: Track income and expenses with dates and descriptions

## Development Notes

- Start with budgeting functionality
- Design for mobile-first, responsive UI
- Focus on clear visualizations and intuitive UX
- Keep code clean and well-documented for learning

