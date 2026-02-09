# Rafund Development Standards & Contribution Guidelines

## 🎯 Code Quality Standards

### Python Code Style

**Follow PEP 8** with these guidelines:

```python
# ✅ Good
def calculate_portfolio_return(returns: list[float], weights: list[float]) -> float:
    """Calculate weighted portfolio return.
    
    Args:
        returns: List of asset returns
        weights: List of portfolio weights
        
    Returns:
        Portfolio return
    """
    return sum(r * w for r, w in zip(returns, weights))

# ❌ Bad
def calcPortReturn(r,w):
    return sum([r[i]*w[i] for i in range(len(r))])
```

### Type Hints

```python
from typing import List, Dict, Tuple, Optional

def analyze_stocks(symbols: List[str], 
                   lookback: int = 252) -> Dict[str, float]:
    """Analyze stock performance."""
    pass

def get_stock_data(symbol: str) -> Optional[Dict]:
    """Fetch stock data."""
    pass
```

### Docstrings (Google Style)

```python
def calculate_sharpe_ratio(returns: list[float], 
                           risk_free_rate: float = 0.02) -> float:
    """Calculate Sharpe Ratio for a returns series.
    
    The Sharpe Ratio measures risk-adjusted return by comparing
    excess returns to volatility.
    
    Args:
        returns: Array of daily returns
        risk_free_rate: Annual risk-free rate (default: 2%)
        
    Returns:
        Sharpe Ratio (annualized)
        
    Raises:
        ValueError: If returns is empty
        
    Example:
        >>> returns = [0.01, 0.02, -0.01, 0.03]
        >>> sharpe = calculate_sharpe_ratio(returns)
        >>> print(sharpe)
        2.45
    """
    if not returns:
        raise ValueError("Returns cannot be empty")
    
    excess_returns = [r - risk_free_rate/252 for r in returns]
    return (np.mean(excess_returns) * 252) / (np.std(excess_returns) * np.sqrt(252))
```

---

## 📝 Commit Message Format

### Format
```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Code style
- `refactor`: Code refactoring
- `test`: Testing
- `chore`: Build/maintenance
- `perf`: Performance
- `research`: Research work

### Examples

**Good Commits:**
```
feat(models): implement LSTM price predictor for MSE stocks

- Add LSTM architecture with 3 layers
- Implement data preprocessing pipeline
- Add validation with walk-forward testing
- Achieve 85% directional accuracy on test set

Closes #42
```

```
fix(scraper): handle MSE website structure change

The MSE website updated table markup. Fixed CSS selectors
to correctly parse stock data from new table format.

Tested on 2026-02-08 data successfully.
```

```
docs: add research methodology guide

Comprehensive guide covering:
- Research process from hypothesis to deployment
- Backtesting framework and best practices
- Common pitfalls and how to avoid them
```

---

## 🧪 Testing Standards

### Test File Structure

```
tests/
├── unit/
│   ├── test_data_processors.py
│   ├── test_models.py
│   └── test_portfolio.py
├── integration/
│   ├── test_data_pipeline.py
│   └── test_model_pipeline.py
└── fixtures/
    ├── sample_data.csv
    └── mock_api_responses.json
```

### Test Coverage

**Minimum Requirements:**
- Overall: 70% code coverage
- Critical paths: 90%+
- Data processing: 85%+

### Unit Testing

```python
import pytest
from rafund.models import PricePredictor
from rafund.data import fetch_stock_data

class TestPricePredictor:
    """Test suite for PricePredictor model."""
    
    @pytest.fixture
    def sample_data(self):
        """Load sample training data."""
        return fetch_stock_data('JDH', start='2024-01-01', end='2026-02-08')
    
    @pytest.fixture
    def predictor(self):
        """Initialize predictor."""
        return PricePredictor(model_type='lstm')
    
    def test_initialization(self, predictor):
        """Test predictor initializes correctly."""
        assert predictor.model_type == 'lstm'
        assert predictor.trained == False
    
    def test_training(self, predictor, sample_data):
        """Test model training."""
        predictor.train(sample_data)
        assert predictor.trained == True
        assert predictor.loss < 0.1
    
    def test_prediction(self, predictor, sample_data):
        """Test prediction generation."""
        predictor.train(sample_data)
        predictions = predictor.predict(sample_data[-30:])
        
        assert len(predictions) == 30
        assert all(isinstance(p, float) for p in predictions)
    
    def test_prediction_shape(self, predictor, sample_data):
        """Test prediction output shape."""
        predictor.train(sample_data)
        predictions = predictor.predict(sample_data[-10:])
        
        assert predictions.shape == (10,)
    
    @pytest.mark.parametrize("lookback", [5, 10, 20, 30])
    def test_various_lookback_periods(self, predictor, lookback, sample_data):
        """Test with different lookback periods."""
        predictor.lookback = lookback
        predictor.train(sample_data)
        predictions = predictor.predict(sample_data[-lookback:])
        
        assert len(predictions) > 0
```

### Integration Testing

```python
class TestDataModelPipeline:
    """Test integration between data and models."""
    
    def test_end_to_end_prediction(self):
        """Test full pipeline from data to prediction."""
        # Fetch data
        data = fetch_stock_data('JDH')
        
        # Process data
        processed = preprocess_data(data)
        
        # Train model
        model = PricePredictor()
        model.train(processed)
        
        # Generate predictions
        predictions = model.predict(processed[-20:])
        
        # Verify output
        assert len(predictions) == 20
        assert all(p > 0 for p in predictions)  # Prices should be positive
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src tests/

# Run specific test file
pytest tests/unit/test_models.py

# Run specific test
pytest tests/unit/test_models.py::TestPricePredictor::test_training

# Run with verbose output
pytest -v

# Run tests matching pattern
pytest -k "prediction"

# Run and stop at first failure
pytest -x
```

---

## 📋 Code Review Checklist

### Functionality
- [ ] Code works as intended
- [ ] Handles edge cases
- [ ] No unhandled exceptions
- [ ] Performance acceptable

### Quality
- [ ] Follows code style guide
- [ ] No code duplication
- [ ] Proper error handling
- [ ] Adequate logging

### Documentation
- [ ] Functions documented
- [ ] Complex logic explained
- [ ] Examples provided
- [ ] Type hints present

### Testing
- [ ] Tests present
- [ ] Tests passing
- [ ] Good coverage
- [ ] Edge cases tested

### Safety
- [ ] No hardcoded values
- [ ] No credentials in code
- [ ] Input validation present
- [ ] SQL injection prevented

---

## 🔍 Linting & Formatting

### Setup

```bash
# Install tools
pip install black pylint flake8 mypy

# Auto-format code
black src/

# Check style
flake8 src/

# Type checking
mypy src/

# Linting
pylint src/
```

### Configuration Files

**`.flake8`:**
```ini
[flake8]
max-line-length = 100
exclude = .git,__pycache__,.venv
ignore = E203,W503
```

**`pyproject.toml` (Black):**
```toml
[tool.black]
line-length = 100
target-version = ['py38', 'py39', 'py310', 'py311']
```

---

## 🚀 Git Workflow

### Feature Development

```bash
# Create feature branch from main
git checkout -b feature/mse-data-scraper

# Make commits regularly
git add src/data/mse_scraper.py
git commit -m "feat: add MSE mainboard scraper"

# Keep branch updated
git fetch origin
git rebase origin/main

# Push feature branch
git push origin feature/mse-data-scraper

# Create Pull Request on GitHub
# Request review from team members
# Address review comments
# Merge when approved
```

### Branch Naming

```
feature/<description>      # New features
fix/<issue>               # Bug fixes
docs/<topic>              # Documentation
research/<project>        # Research projects
refactor/<component>      # Code improvements
```

### Rebasing vs Merging

```bash
# Prefer rebasing for clean history
git rebase origin/main

# Before pushing to shared branch
git push -f origin feature/your-feature

# Use merge for release branches
git merge --no-ff feature/your-feature
```

---

## 📦 Dependency Management

### Adding Dependencies

```bash
# Install new package
pip install package-name

# Add to requirements.txt manually or:
pip freeze > requirements.txt

# Create separate dev requirements
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Document why dependency is needed
# In code comments or README
```

### Requirements File Structure

**`requirements.txt`:**
```
# Core dependencies
numpy==1.24.0
pandas==2.0.0
scikit-learn==1.2.0

# Web scraping
beautifulsoup4==4.11.0
requests==2.28.0

# Data storage
sqlalchemy==2.0.0
psycopg2-binary==2.9.0
```

**`requirements-dev.txt`:**
```
-r requirements.txt

# Development tools
jupyter==1.0.0
black==23.1.0
pylint==2.16.0
pytest==7.2.0
pytest-cov==4.0.0
```

---

## 🔐 Security Practices

### Credential Management

```python
# ❌ DON'T do this
DB_PASSWORD = "my_password_123"
API_KEY = "abc123xyz"

# ✅ DO this
import os
from dotenv import load_dotenv

load_dotenv()
DB_PASSWORD = os.getenv('DB_PASSWORD')
API_KEY = os.getenv('API_KEY')
```

### `.env.example` (commit this)

```
DB_PASSWORD=your_password_here
API_KEY=your_api_key_here
MSE_USER=your_username_here
```

### `.gitignore`

```
.env
.env.local
__pycache__/
.pytest_cache/
.coverage
*.log
venv/
node_modules/
.DS_Store
```

---

## 📊 Performance Standards

### Code Performance

```python
import time
from functools import wraps

def performance_timer(func):
    """Decorator to measure function execution time."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end-start:.2f} seconds")
        return result
    return wrapper

@performance_timer
def expensive_operation():
    # Your code here
    pass
```

### Benchmarking

```python
import timeit

# Benchmark different approaches
time_taken = timeit.timeit(
    'calculate_returns(data)',
    globals=globals(),
    number=1000
)
print(f"Average time: {time_taken/1000:.4f}s")
```

---

## 📚 Documentation Requirements

### README for New Features

```markdown
## Feature: Stock Price Prediction

### Overview
LSTM-based neural network for predicting next-day MSE stock prices.

### Usage
```python
from rafund.models import StockPredictor

predictor = StockPredictor(ticker='JDH')
predictor.train(data)
prediction = predictor.predict()
```
```

### API Documentation

```python
def calculate_portfolio_metrics(returns: np.ndarray,
                               weights: np.ndarray) -> dict:
    """
    Calculate key performance metrics for portfolio.
    
    Parameters:
    -----------
    returns : np.ndarray
        Asset returns (n_assets, n_periods)
    weights : np.ndarray
        Portfolio weights (n_assets,)
        
    Returns:
    --------
    dict
        Containing 'sharpe_ratio', 'volatility', 'return'
        
    See Also:
    ---------
    calculate_sharpe_ratio : Individual metric calculation
    """
```

---

## ✅ Pre-Submission Checklist

- [ ] Code follows PEP 8
- [ ] All tests pass: `pytest`
- [ ] Coverage > 70%: `pytest --cov`
- [ ] Linting passes: `flake8 src/`
- [ ] Type checking passes: `mypy src/`
- [ ] Code formatted: `black src/`
- [ ] Docstrings present
- [ ] No hardcoded values
- [ ] No credentials in code
- [ ] Commit messages clear
- [ ] Documentation updated
- [ ] CHANGELOG updated

---

*Last Updated: February 8, 2026*
