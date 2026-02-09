# Rafund - Technical Architecture Overview

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Data Layer                           │
│  ┌──────────────────────────────────────────────────┐   │
│  │   MSE Scraper    │  Yahoo Finance  │   News API   │   │
│  └──────────┬───────────────┬──────────────┬────────┘   │
│             │               │              │             │
│             └───────────────┴──────────────┘             │
│                     ↓                                    │
│  ┌──────────────────────────────────────────────────┐   │
│  │         Data Processing Pipeline                 │   │
│  │  Cleaning │ Normalization │ Feature Engineering  │   │
│  └──────────────────┬─────────────────────────────┘   │
│                     ↓                                   │
│  ┌──────────────────────────────────────────────────┐  │
│  │      Data Storage (PostgreSQL + Redis)          │  │
│  └──────────────────┬─────────────────────────────┘   │
└──────────────────────┼──────────────────────────────────┘
                       │
┌──────────────────────┼──────────────────────────────────┐
│            Model/Analytics Layer                       │
│  ┌──────────────────────────────────────────────────┐  │
│  │  ML Models  │  Statistical Models │  Backtesting │  │
│  │  - LSTM     │  - ARIMA            │  - Strategy   │  │
│  │  - GBM      │  - Regression       │  - Metrics    │  │
│  │  - NLP      │  - Sentiment        │  - Risk Mgmt  │  │
│  └──────────────────────────────────────────────────┘  │
└──────────────────────┬─────────────────────────────────┘
                       │
┌──────────────────────┼──────────────────────────────────┐
│         Portfolio Management Layer                      │
│  ┌──────────────────────────────────────────────────┐  │
│  │  Position Management  │  Risk Management       │   │
│  │  - Entry/Exit         │  - Stop Loss           │   │
│  │  - Rebalancing        │  - Drawdown Monitor    │   │
│  │  - Tracking           │  - Exposure Limits     │   │
│  └──────────────────────────────────────────────────┘  │
└──────────────────────┬─────────────────────────────────┘
                       │
┌──────────────────────┼──────────────────────────────────┐
│         Presentation Layer                            │
│  ┌──────────────────────────────────────────────────┐ │
│  │  REST API  │  Dashboard  │  Reports  │  Alerts   │ │
│  └──────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────┘
```

---

## 🗄️ Database Schema

### Tables

```sql
-- Stocks table
CREATE TABLE stocks (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(10) UNIQUE,
    name VARCHAR(255),
    sector VARCHAR(50),
    listing_date DATE,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Price history
CREATE TABLE price_history (
    id SERIAL PRIMARY KEY,
    stock_id INT REFERENCES stocks(id),
    date DATE NOT NULL,
    open DECIMAL(10, 2),
    high DECIMAL(10, 2),
    low DECIMAL(10, 2),
    close DECIMAL(10, 2),
    volume BIGINT,
    UNIQUE(stock_id, date)
);

-- Predictions
CREATE TABLE predictions (
    id SERIAL PRIMARY KEY,
    stock_id INT REFERENCES stocks(id),
    model_name VARCHAR(50),
    prediction_date DATE,
    predicted_price DECIMAL(10, 2),
    confidence DECIMAL(5, 2),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Portfolio
CREATE TABLE portfolio (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    description TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Positions
CREATE TABLE positions (
    id SERIAL PRIMARY KEY,
    portfolio_id INT REFERENCES portfolio(id),
    stock_id INT REFERENCES stocks(id),
    shares DECIMAL(15, 2),
    entry_price DECIMAL(10, 2),
    entry_date DATE,
    stop_loss DECIMAL(10, 2),
    take_profit DECIMAL(10, 2),
    status VARCHAR(20)  -- OPEN, CLOSED, etc.
);
```

---

## 🔌 API Endpoints

### REST API Structure

```
/api/v1/
├── /stocks
│   ├── GET /stocks              # List all stocks
│   ├── GET /stocks/{symbol}     # Get stock details
│   ├── GET /stocks/{symbol}/price-history
│   └── GET /stocks/{symbol}/predictions
├── /portfolio
│   ├── GET /portfolio           # Get portfolio
│   ├── POST /portfolio/rebalance
│   ├── GET /portfolio/metrics
│   └── GET /portfolio/performance
├── /predictions
│   ├── GET /predictions/{symbol}
│   ├── POST /predictions/generate
│   └── POST /predictions/evaluate
└── /backtest
    ├── POST /backtest/run
    ├── GET /backtest/results/{id}
    └── GET /backtest/metrics/{id}
```

### Example API Requests

```bash
# Get stock data
curl https://api.rafund.co.mw/api/v1/stocks/JDH

# Get predictions
curl https://api.rafund.co.mw/api/v1/predictions/NBM

# Get portfolio metrics
curl https://api.rafund.co.mw/api/v1/portfolio/metrics

# Run backtest
curl -X POST https://api.rafund.co.mw/api/v1/backtest/run \
  -H "Content-Type: application/json" \
  -d '{
    "strategy": "momentum",
    "start_date": "2025-01-01",
    "end_date": "2026-02-08",
    "initial_capital": 1000000
  }'
```

---

## 🔄 Data Flow

### Real-time Data Pipeline

```
1. Data Collection (Daily 9:30 AM)
   └─ MSE API / Web Scraper
      └─ Raw JSON/CSV
         └─ Data Validation
            └─ Database Storage

2. Feature Engineering (Daily 5:00 PM)
   └─ Load raw data from DB
      └─ Calculate technical indicators
         └─ Normalize features
            └─ Redis caching
               └─ Model ready

3. Model Inference (Daily 6:00 PM)
   └─ Load features
      └─ Run predictions
         └─ Store predictions
            └─ Calculate confidence

4. Portfolio Updates (Daily 7:00 PM)
   └─ Generate trading signals
      └─ Check risk limits
         └─ Simulate trades
            └─ Update positions
               └─ Alert notifications
```

### Scheduled Jobs (Cron)

```cron
# Data collection - Daily at 9:30 AM
30 09 * * 1-5 python -m rafund.data.jobs.collect_market_data

# Feature engineering - Daily at 5:00 PM
00 17 * * 1-5 python -m rafund.models.jobs.engineer_features

# Model training - Weekly Sunday at 10:00 PM
00 22 * * 0 python -m rafund.models.jobs.train_models

# Portfolio rebalancing - Monthly first Friday
00 14 1 * 5 python -m rafund.portfolio.jobs.rebalance

# Performance reporting - Monthly second Friday
00 16 8-14 * 5 python -m rafund.reporting.jobs.monthly_report
```

---

## 📦 Dependencies & Stack

### Core Libraries

```
# Data Processing
pandas==2.0.0
numpy==1.24.0

# Machine Learning
scikit-learn==1.2.0
tensorflow==2.12.0
xgboost==1.7.0

# Web Framework
fastapi==0.104.0
uvicorn==0.24.0

# Database
sqlalchemy==2.0.0
psycopg2-binary==2.9.0

# Scraping
beautifulsoup4==4.11.0
requests==2.28.0

# Data Visualization
matplotlib==3.7.0
plotly==5.14.0
```

---

## 🔐 Security Architecture

### Authentication & Authorization

```python
# JWT-based authentication
from fastapi.security import HTTPBearer

security = HTTPBearer()

@app.get("/api/v1/portfolio")
async def get_portfolio(credentials: HTTPAuthenticationCredentials = Depends(security)):
    token = credentials.credentials
    payload = verify_jwt_token(token)
    user_id = payload["user_id"]
    # Return user's portfolio
    return Portfolio.get_by_user(user_id)
```

### Data Encryption

```python
# Encrypt sensitive data in database
from cryptography.fernet import Fernet

cipher_suite = Fernet(os.getenv('ENCRYPTION_KEY'))
encrypted_api_key = cipher_suite.encrypt(api_key.encode())
db.save(encrypted_api_key)
```

### Rate Limiting

```python
from slowapi import Limiter

limiter = Limiter(key_func=get_remote_address)

@app.get("/api/v1/predictions")
@limiter.limit("100/minute")
async def get_predictions(request: Request):
    pass
```

---

## 🚀 Deployment Architecture

### Production Environment

```
┌─────────────────────────────────────────┐
│     Load Balancer (Nginx)               │
└────────────────┬────────────────────────┘
                 │
        ┌────────┴────────┐
        ↓                 ↓
   ┌────────────┐    ┌────────────┐
   │  API Pod 1 │    │  API Pod 2 │
   └─────┬──────┘    └──────┬─────┘
         │                  │
         └──────────┬───────┘
                    ↓
        ┌──────────────────────┐
        │  PostgreSQL Master   │
        │  (Primary DB)        │
        └──────────────────────┘
        ┌──────────────────────┐
        │  PostgreSQL Replica  │
        │  (Read-only)         │
        └──────────────────────┘
        ┌──────────────────────┐
        │  Redis Cache         │
        └──────────────────────┘
```

### Docker Deployment

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src/ ./src/
COPY config/ ./config/

ENV PYTHONUNBUFFERED=1
EXPOSE 8000

CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 📊 Monitoring & Logging

### Application Metrics

```python
from prometheus_client import Counter, Histogram

# Define metrics
prediction_counter = Counter('predictions_total', 'Total predictions')
api_request_duration = Histogram('api_request_duration_seconds', 'API request duration')
model_accuracy = Gauge('model_accuracy', 'Current model accuracy')
```

### Logging Configuration

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/rafund.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
```

---

## 🧪 Testing Strategy

### Unit Tests
- Test individual functions
- Mock external dependencies
- Target: 80%+ coverage

### Integration Tests
- Test component interactions
- Use test database
- Test API endpoints

### Stress Tests
- Test with large datasets
- Measure performance
- Identify bottlenecks

### Smoke Tests (Production)
- Daily checks
- Key functionality validation
- Alert on failures

---

## 📈 Scalability Considerations

### Horizontal Scaling
- Stateless API servers (can add/remove as needed)
- Load balancer distributes traffic
- Database replicas for read scaling

### Vertical Scaling
- Cache frequently accessed data (Redis)
- Database indexing optimization
- Async task processing (Celery)

### Performance Optimization
- Database query optimization
- Caching strategies
- Async I/O operations
- Model optimization (quantization, pruning)

---

*Last Updated: February 8, 2026*
