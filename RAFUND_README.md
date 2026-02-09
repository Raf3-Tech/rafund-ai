# Rafund - Company Overview & Documentation

## 🎯 Company Mission
Rafund is an AI-driven investment management company building quantitative trading systems, research tools, and financial technology for the Malawi Stock Exchange. We manage proprietary investment portfolios while conducting advanced research in data science, machine learning, and quantitative finance.

---

## 📋 Quick Navigation
- [Company Overview](#company-overview)
- [Core Business Areas](#core-business-areas)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Documentation Index](#documentation-index)

---

## 🏢 Company Overview

**Rafund** operates across three integrated pillars:

### 1. **Investment Management**
- Actively managed investment portfolios
- Proprietary quantitative strategies
- Risk management and portfolio optimization
- Performance tracking and reporting

### 2. **AI & Data Science Research**
- Machine learning model development
- Predictive analytics for financial markets
- Natural language processing for market sentiment
- Advanced statistical analysis

### 3. **Financial Technology & Tools**
- MSE data scraping and aggregation platforms
- Trading analysis tools
- Portfolio management systems
- Market research dashboards

---

## 🛠️ Core Business Areas

### Financial Data Science
- Real-time market data collection
- Time series analysis and forecasting
- Anomaly detection
- Market microstructure research

### Quantitative Finance
- Algorithm development
- Risk modeling
- Backtesting frameworks
- Performance attribution analysis

### AI & Machine Learning
- Deep learning for price prediction
- Reinforcement learning for portfolio optimization
- Sentiment analysis on financial news
- Pattern recognition in trading data

### Platform Development
- Web-based trading dashboards
- API services for data access
- Portfolio monitoring tools
- Research publication platform

---

## 💻 Technology Stack

### Data & Analysis
- **Python 3.x** - Primary language
- **Pandas** - Data manipulation
- **NumPy/SciPy** - Scientific computing
- **Scikit-learn** - Machine learning
- **TensorFlow/PyTorch** - Deep learning

### Data Collection
- **BeautifulSoup** - Web scraping
- **Requests** - HTTP requests
- **Selenium** - Browser automation

### Visualization & Reporting
- **Matplotlib/Seaborn** - Static visualization
- **Plotly** - Interactive dashboards
- **Jupyter** - Research notebooks

### Infrastructure
- **PostgreSQL** - Data storage
- **Redis** - Caching & real-time data
- **Docker** - Containerization
- **Git** - Version control

### Web & API
- **FastAPI** - REST API framework
- **Flask** - Web application framework
- **SQLAlchemy** - ORM

---

## 📁 Project Structure

```
rafund/
├── research/                 # Research projects & notebooks
│   ├── price_prediction/
│   ├── sentiment_analysis/
│   ├── portfolio_optimization/
│   └── README.md
├── data/                     # Data pipelines & scraping
│   ├── mse_scraper/
│   ├── data_pipelines/
│   ├── market_data/
│   └── README.md
├── tools/                    # Platform & tools development
│   ├── dashboard/
│   ├── api_services/
│   ├── portfolio_manager/
│   └── README.md
├── portfolio/                # Investment portfolio management
│   ├── strategies/
│   ├── backtesting/
│   ├── performance_tracking/
│   └── README.md
├── docs/                     # Documentation
│   ├── ARCHITECTURE.md
│   ├── RESEARCH_METHODOLOGY.md
│   ├── DATA_DICTIONARY.md
│   └── API_REFERENCE.md
├── tests/                    # Unit & integration tests
├── config/                   # Configuration files
├── requirements.txt          # Python dependencies
├── .gitignore
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Git
- PostgreSQL (optional, for data storage)
- Docker (optional, for containerization)

### Installation

```bash
# Clone repository
git clone https://github.com/rafund/rafund.git
cd rafund

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up configuration
cp config/example.env config/.env
# Edit config/.env with your settings

# Initialize database (if applicable)
python scripts/init_db.py
```

### Running Components

```bash
# Run research notebooks
jupyter notebook research/

# Run data pipeline
python data/mse_scraper/scraper.py

# Start API server
python tools/api_services/main.py

# Run tests
pytest tests/
```

---

## 📚 Documentation Index

### Core Documentation
- **[Architecture Overview](ARCHITECTURE.md)** - System design and components
- **[Research Methodology](RESEARCH_METHODOLOGY.md)** - Research framework and process
- **[Data Dictionary](DATA_DICTIONARY.md)** - Data schemas and definitions
- **[API Reference](API_REFERENCE.md)** - Platform API documentation

### Development Guides
- **[Setup Guide](SETUP_GUIDE.md)** - Development environment setup
- **[Contribution Guidelines](CONTRIBUTING.md)** - Code standards and workflow
- **[Deployment Guide](DEPLOYMENT.md)** - Production deployment procedures

### Business Documentation
- **[Portfolio Strategy Guide](PORTFOLIO_STRATEGY.md)** - Investment strategy documentation
- **[Compliance & Risk](COMPLIANCE.md)** - Risk management and compliance
- **[Performance Reporting](PERFORMANCE_REPORTING.md)** - KPIs and metrics

---

## 📊 Key Metrics & KPIs

### Investment Performance
- **Sharpe Ratio** - Risk-adjusted returns
- **Maximum Drawdown** - Downside risk
- **Annualized Return** - Portfolio growth
- **Information Ratio** - Active management performance

### Technology
- **Data Pipeline Latency** - Time to fresh data
- **Model Accuracy** - Prediction performance
- **System Uptime** - Platform availability
- **API Response Time** - Service performance

---

## 🤝 Team Roles & Responsibilities

### Quantitative Researchers
- Develop trading algorithms
- Conduct market analysis
- Build financial models

### Data Scientists
- Develop ML models
- Implement analytics
- Data engineering

### Software Engineers
- Build platforms and tools
- API development
- Infrastructure management

### Portfolio Managers
- Strategy implementation
- Risk management
- Performance monitoring

---

## 📈 Development Roadmap

### Phase 1: Foundation (Q1 2026)
- MSE data infrastructure setup
- Core research frameworks
- Initial portfolio strategies

### Phase 2: Expansion (Q2 2026)
- Platform MVP launch
- Advanced ML models
- API services release

### Phase 3: Scaling (Q3-Q4 2026)
- Multi-market expansion
- Institutional tools
- Research publications

---

## 📞 Contact & Support

For questions or contributions, please refer to the relevant documentation or contact the development team.

---

## 📄 License & Compliance

All code and research at Rafund follows appropriate data protection and financial regulations. Proprietary strategies and models are protected intellectual property.

---

*Last Updated: February 8, 2026*
