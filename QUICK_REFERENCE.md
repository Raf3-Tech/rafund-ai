# Rafund - Quick Reference Guide

## 🚀 Getting Started (5 Minutes)

### 1. Environment Setup
```bash
# Clone repo
git clone https://github.com/rafund/rafund.git
cd rafund

# Setup environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install packages
pip install -r requirements.txt
```

### 2. Run Your First Scraper
```bash
# MSE data scraper
python src/data/mse_scraper/scraper.py

# Check output
ls -la data/mse_data/
```

### 3. Start Jupyter
```bash
jupyter lab
# Open http://localhost:8888
# Browse to research/notebooks/
```

---

## 📊 Common Tasks

### Data Tasks

**Fetch MSE stock data:**
```python
from rafund.data import MSEScraper

scraper = MSEScraper()
data = scraper.scrape_stock_data()
print(data[0])  # First stock
```

**Load historical data:**
```python
from rafund.data import load_stock_data

data = load_stock_data('JDH', start='2025-01-01', end='2026-02-08')
print(data.describe())
```

**Save data locally:**
```python
data.to_csv('data/jdh_2025_2026.csv')
data.to_json('data/jdh_2025_2026.json')
```

### Model Tasks

**Train price predictor:**
```python
from rafund.models import LSTMPredictor
from rafund.data import load_stock_data

# Get data
data = load_stock_data('JDH')

# Create and train model
model = LSTMPredictor(lookback=30)
model.fit(data, epochs=50, batch_size=32)

# Make predictions
next_5_days = model.predict(5)
print(next_5_days)
```

**Backtest strategy:**
```python
from rafund.portfolio import Backtester
from rafund.models import MomentumStrategy

# Setup backtest
backtester = Backtester(
    initial_capital=1000000,
    commission=0.001,
    start_date='2024-01-01',
    end_date='2026-02-08'
)

# Run strategy
strategy = MomentumStrategy(lookback=30)
results = backtester.run(strategy)

print(f"Sharpe Ratio: {results.sharpe_ratio:.2f}")
print(f"Max Drawdown: {results.max_drawdown:.2%}")
```

### Portfolio Tasks

**Check portfolio performance:**
```python
from rafund.portfolio import Portfolio

portfolio = Portfolio()
portfolio.load_from_file('portfolios/live_portfolio.json')

print(f"Value: MWK {portfolio.total_value():,.0f}")
print(f"Return: {portfolio.total_return():.2%}")
print(f"Sharpe: {portfolio.sharpe_ratio():.2f}")
```

**Rebalance portfolio:**
```python
target_weights = {
    'JDH': 0.15,
    'NBM': 0.20,
    'NBS': 0.15,
    'ILLOVO': 0.10,
    'NICO': 0.10,
    'FMBCH': 0.15,
    'STANDARD': 0.10,
    'CASH': 0.05
}

rebalancing_trades = portfolio.rebalance_to_weights(target_weights)
for trade in rebalancing_trades:
    print(f"{trade['symbol']}: {trade['action']} {trade['shares']} shares")
```

---

## 🔧 Useful Commands

### Git Commands
```bash
# Create feature branch
git checkout -b feature/new-feature

# Commit changes
git add .
git commit -m "feat: add new feature"

# Push branch
git push origin feature/new-feature

# Create pull request on GitHub
```

### Testing
```bash
# Run all tests
pytest

# Run specific test
pytest tests/unit/test_models.py::TestLSTM

# Run with coverage
pytest --cov=src tests/
```

### Data Operations
```bash
# Export to Excel
import pandas as pd
df = pd.read_csv('data/mse_stocks.csv')
df.to_excel('output.xlsx', sheet_name='Stocks')

# Merge multiple files
import glob
all_data = []
for file in glob.glob('data/raw/*.csv'):
    df = pd.read_csv(file)
    all_data.append(df)
merged = pd.concat(all_data, ignore_index=True)
```

---

## 📈 Performance Metrics Quick Reference

| Metric | Formula | Good Value |
|--------|---------|-----------|
| Return | (End Value - Start Value) / Start Value | >10% annual |
| Volatility | Std Dev of Returns | <15% annual |
| Sharpe Ratio | (Return - Risk Free) / Volatility | >1.0 |
| Sortino Ratio | (Return - Target) / Downside Vol | >1.0 |
| Max Drawdown | (Trough - Peak) / Peak | <15% |
| Win Rate | Wins / Total Trades | >50% |
| Profit Factor | Gross Profit / Gross Loss | >2.0 |

---

## 🐛 Debugging Common Issues

### Issue: "ModuleNotFoundError"
```bash
# Solution: Ensure virtual environment is activated
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Reinstall packages
pip install -r requirements.txt
```

### Issue: "ConnectionError" when scraping
```bash
# Solution: Check internet connection and MSE website status
import requests
response = requests.get('https://mse.co.mw/market/mainboard')
print(response.status_code)  # Should be 200
```

### Issue: "Database connection failed"
```bash
# Solution: Check PostgreSQL is running
# macOS: brew services start postgresql
# Linux: sudo systemctl start postgresql
# Windows: Check Services or pgAdmin

# Test connection
psql -U rafund_user -d rafund_dev
```

### Issue: "Out of memory" with large datasets
```python
# Solution: Process in chunks
import pandas as pd

chunks = pd.read_csv('large_file.csv', chunksize=10000)
for chunk in chunks:
    process_chunk(chunk)
    # Memory is freed between iterations
```

---

## 📚 File Navigation

```
rafund/
├── README.md                      ← Start here
├── SETUP_GUIDE.md                 ← Installation
├── DEVELOPMENT_STANDARDS.md       ← Code rules
├── RESEARCH_METHODOLOGY.md        ← Research process
├── PORTFOLIO_MANAGEMENT.md        ← Portfolio guide
├── QUICK_REFERENCE.md             ← This file

├── src/                           ← Main code
│   ├── data/                      ← Data scraping
│   ├── models/                    ← ML models
│   ├── portfolio/                 ← Portfolio management
│   └── utils/                     ← Utilities

├── research/                      ← Research projects
│   └── notebooks/                 ← Jupyter notebooks

├── tests/                         ← Tests
│   ├── unit/
│   └── integration/

└── config/                        ← Configuration
    └── example.env                ← Copy to .env
```

---

## 🔗 Important Links

- **GitHub**: https://github.com/rafund/rafund
- **Documentation**: ./docs/
- **API Docs**: src/api/openapi.json
- **Research Papers**: research/papers/
- **Data Sources**: https://mse.co.mw/

---

## 👥 Team Contacts

- **Engineering Lead**: engineering@rafund.co.mw
- **Research Lead**: research@rafund.co.mw
- **Portfolio Manager**: portfolio@rafund.co.mw
- **Main Contact**: contact@rafund.co.mw

---

## ⏰ Important Dates

- **Market Hours**: 9:30 AM - 4:00 PM (Malawi Time)
- **Trading Days**: Monday - Friday
- **Holiday Calendar**: See docs/holidays.md
- **Reporting**: Monthly on first Friday

---

## 💡 Pro Tips

1. **Always commit before major changes**
   ```bash
   git commit -m "wip: before major refactor"
   ```

2. **Test locally before pushing**
   ```bash
   pytest --cov=src
   ```

3. **Document as you code**
   ```python
   def complex_function(param1, param2):
       """Brief description.
       
       Longer explanation of logic.
       """
   ```

4. **Use type hints**
   ```python
   def calculate_return(prices: list[float]) -> float:
       pass
   ```

5. **Keep functions small and focused**
   - Easier to test
   - Easier to understand
   - Easier to reuse

---

## 📝 Templates

### Feature Request Template
```
**Title**: Brief description

**Problem**: What problem does this solve?

**Solution**: How should this be implemented?

**Acceptance Criteria**:
- [ ] Criterion 1
- [ ] Criterion 2
```

### Bug Report Template
```
**Title**: Brief description

**Environment**: 
- OS: 
- Python: 
- Packages: (pip freeze)

**Steps to Reproduce**:
1. 
2. 
3. 

**Expected**: What should happen

**Actual**: What actually happened

**Error Message**: 
```

---

## 🎓 Learning Paths

### Beginner
1. Read RAFUND_README.md
2. Follow SETUP_GUIDE.md
3. Run example notebooks
4. Understand data flow

### Intermediate
1. Study RESEARCH_METHODOLOGY.md
2. Implement simple strategy
3. Backtest strategy
4. Review code with senior dev

### Advanced
1. Read academic papers
2. Develop novel ML model
3. Deploy to production
4. Mentor junior developers

---

*Last Updated: February 8, 2026*
*For latest updates, check GitHub: https://github.com/rafund/rafund*
