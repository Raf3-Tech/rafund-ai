# Rafund Development Setup Guide

## 🚀 Environment Setup

### System Requirements
- **OS**: Windows, macOS, or Linux
- **Python**: 3.8+ (3.11+ recommended)
- **Git**: Latest version
- **RAM**: 8GB minimum
- **Storage**: 50GB+ for data and models

---

## 📦 Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/rafund/rafund.git
cd rafund
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install all required packages
pip install -r requirements.txt

# Install development dependencies
pip install -r requirements-dev.txt
```

### 4. Configuration Setup

```bash
# Copy example environment file
cp config/example.env config/.env

# Edit configuration
# - Add API keys
# - Set database credentials
# - Configure paths
nano config/.env  # or use your preferred editor
```

### 5. Initialize Database

```bash
# Create database
python scripts/init_db.py

# Run migrations
python scripts/migrate_db.py
```

---

## 🛠️ Development Tools Setup

### Code Editor (VS Code Recommended)

**Extensions to install:**
```
- Python (Microsoft)
- Pylance
- Jupyter
- SQLTools
- Git Graph
- Better Comments
- Code Spell Checker
```

### IDE Configuration

Create `.vscode/settings.json`:

```json
{
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": true,
  "python.formatting.provider": "black",
  "python.formatting.blackArgs": ["--line-length=100"],
  "[python]": {
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
      "source.organizeImports": true
    }
  }
}
```

### Pre-commit Hooks

```bash
# Install pre-commit
pip install pre-commit

# Set up hooks
pre-commit install

# Run hooks manually
pre-commit run --all-files
```

---

## 🗄️ Database Setup

### PostgreSQL (Recommended)

```bash
# Install PostgreSQL
# Windows: Download from postgresql.org
# macOS: brew install postgresql
# Linux: sudo apt-get install postgresql

# Create database
createdb rafund_dev

# Create user
psql -U postgres -c "CREATE USER rafund_user WITH PASSWORD 'your_password';"
psql -U postgres -c "ALTER ROLE rafund_user SUPERUSER;"

# Test connection
psql -U rafund_user -d rafund_dev
```

### Update `.env`

```
DATABASE_URL=postgresql://rafund_user:your_password@localhost:5432/rafund_dev
```

---

## 📊 Jupyter Setup

### Installation

```bash
# Already included in requirements.txt
pip install jupyter jupyterlab

# For additional kernels
python -m ipykernel install --user --name rafund --display-name "Rafund"
```

### Configure Jupyter

Create `~/.jupyter/jupyter_notebook_config.py`:

```python
c.NotebookApp.notebook_dir = 'path/to/rafund/research'
c.NotebookApp.token = ''  # Disable token auth for local dev
c.NotebookApp.allow_remote_access = False
```

### Launch Jupyter

```bash
jupyter lab
# or
jupyter notebook
```

---

## 🔑 API Keys & Credentials

### Required Keys

1. **MSE Data API** (if available)
   - Register at mse.co.mw
   - Add to `config/.env`

2. **Financial Data Providers**
   - Alpha Vantage
   - Yahoo Finance
   - IEX Cloud

3. **Email Service**
   - Gmail/SendGrid for notifications

Add to `.env`:

```
MSE_API_KEY=your_key_here
ALPHA_VANTAGE_KEY=your_key_here
SENDGRID_API_KEY=your_key_here
```

---

## 🧪 Testing Setup

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_scraper.py

# Run with coverage
pytest --cov=src tests/

# Run with verbose output
pytest -v

# Run specific test
pytest tests/test_scraper.py::test_fetch_stocks
```

### Writing Tests

Create test files in `tests/` directory:

```python
import pytest
from src.data.scraper import MSEScraper

class TestMSEScraper:
    @pytest.fixture
    def scraper(self):
        return MSEScraper()
    
    def test_fetch_stocks(self, scraper):
        stocks = scraper.scrape_stock_data()
        assert len(stocks) > 0
        assert 'symbol' in stocks[0]
```

---

## 📋 Project Structure Quick Reference

```
rafund/
├── src/
│   ├── data/                 # Data pipelines
│   ├── models/               # ML models
│   ├── portfolio/            # Portfolio management
│   ├── utils/                # Utility functions
│   └── __init__.py
├── research/
│   ├── notebooks/            # Jupyter notebooks
│   └── papers/               # Research papers
├── tests/
│   ├── unit/                 # Unit tests
│   ├── integration/          # Integration tests
│   └── fixtures/             # Test data
├── config/
│   ├── example.env           # Example config
│   └── settings.py           # Configuration class
├── docs/                     # Documentation
├── scripts/                  # Utility scripts
├── requirements.txt          # Dependencies
├── requirements-dev.txt      # Dev dependencies
├── pytest.ini                # Pytest config
├── .gitignore
└── README.md
```

---

## 🔄 Git Workflow

### Clone & Branch

```bash
# Create feature branch
git checkout -b feature/your-feature-name

# Make changes
# ... edit files ...

# Stage changes
git add .

# Commit with message
git commit -m "feat: add new prediction model"

# Push to remote
git push origin feature/your-feature-name
```

### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

Example:
```
feat(models): add lstm price prediction model

Implemented LSTM neural network for stock price forecasting.
Achieves 92% accuracy on validation set.

Closes #123
```

---

## 🐳 Docker Setup (Optional)

### Build Container

```bash
# Build Docker image
docker build -t rafund:latest .

# Run container
docker run -it --name rafund-dev rafund:latest

# Access container shell
docker exec -it rafund-dev bash
```

### Docker Compose

```bash
# Start services
docker-compose up

# Stop services
docker-compose down

# View logs
docker-compose logs -f api
```

---

## 🔧 Common Commands

### Data Pipeline

```bash
# Scrape MSE data
python src/data/mse_scraper/scraper.py

# Process data
python src/data/processors/process_stocks.py

# Generate reports
python src/data/reporters/daily_report.py
```

### Model Training

```bash
# Train prediction model
python src/models/train_predictor.py

# Evaluate model
python src/models/evaluate.py --model lstm_v2

# Generate predictions
python src/models/predict.py --date 2026-02-08
```

### Portfolio Management

```bash
# Calculate portfolio metrics
python src/portfolio/metrics.py

# Rebalance portfolio
python src/portfolio/rebalancer.py

# Performance attribution
python src/portfolio/attribution.py
```

---

## 📚 Learning Resources

- **Python**: https://docs.python.org/3/
- **Pandas**: https://pandas.pydata.org/docs/
- **Scikit-learn**: https://scikit-learn.org/
- **TensorFlow**: https://www.tensorflow.org/
- **Financial Theory**: Hull, Options Futures and Other Derivatives
- **ML in Finance**: Advances in Financial Machine Learning (López de Prado)

---

## 🆘 Troubleshooting

### Issue: Module not found error

```bash
# Reinstall dependencies
pip install -r requirements.txt

# Check Python path
python -c "import sys; print(sys.path)"
```

### Issue: Database connection error

```bash
# Check PostgreSQL running
sudo systemctl status postgresql  # Linux
brew services list               # macOS

# Test connection
psql -U rafund_user -d rafund_dev -c "SELECT 1"
```

### Issue: Jupyter kernel not found

```bash
# List kernels
jupyter kernelspec list

# Remove old kernel
jupyter kernelspec remove rafund

# Reinstall
python -m ipykernel install --user --name rafund
```

---

## ✅ Verification Checklist

- [ ] Python virtual environment activated
- [ ] All requirements installed
- [ ] `.env` file configured
- [ ] Database initialized
- [ ] Tests passing (`pytest`)
- [ ] Jupyter working
- [ ] IDE configured
- [ ] Git configured
- [ ] Pre-commit hooks installed

---

*Last Updated: February 8, 2026*
