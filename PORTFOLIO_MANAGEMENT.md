# Rafund - Portfolio Management Guide

## 📊 Investment Philosophy

Rafund's investment approach is built on:
- **Data-Driven Decisions**: Quantitative analysis over intuition
- **Risk Management**: Controlled drawdowns and volatility
- **Diversification**: Spread across multiple strategies
- **Systematic Execution**: Rule-based, automated trading
- **Continuous Learning**: Adapt to market changes

---

## 🎯 Portfolio Structure

### Asset Allocation

```
Rafund Multi-Strategy Portfolio
├── Core Strategies (70%)
│   ├── Price Momentum (25%)
│   ├── Mean Reversion (20%)
│   ├── Sentiment-Based (15%)
│   └── Fundamental Value (10%)
├── Alternative Strategies (20%)
│   ├── Statistical Arbitrage (10%)
│   └── Pairs Trading (10%)
└── Cash Reserve (10%)
    └── Liquidity/Opportunities
```

### Risk Parameters

| Parameter | Target | Limit |
|-----------|--------|-------|
| Maximum Drawdown | 8% | 15% |
| Annual Volatility | 10% | 15% |
| Sharpe Ratio | 1.5+ | 0.5+ |
| Correlation to MSE | 0.7 | Max 0.9 |
| Portfolio Beta | 1.0 | 0.5-1.5 |

---

## 📈 Strategy Documentation

### 1. Price Momentum Strategy

**Concept:**
Exploit the tendency of prices to continue moving in the same direction over short periods.

**Entry Rules:**
```python
def momentum_signal(prices, lookback=30):
    """Generate momentum buy/sell signals."""
    returns = np.diff(prices) / prices[:-1]
    momentum = np.sum(returns[-lookback:])
    
    if momentum > threshold_buy:
        return "BUY"
    elif momentum < threshold_sell:
        return "SELL"
    else:
        return "HOLD"
```

**Exit Rules:**
- Profit taking: +5% gain
- Stop loss: -2% loss
- Time-based: 20-day hold maximum

**Position Sizing:**
```
Position Size = Portfolio Value × Risk Percent / (Stock Volatility × 100)
```

### 2. Mean Reversion Strategy

**Concept:**
Exploit temporary price deviations from fundamental value.

**Entry Rules:**
```python
def mean_reversion_signal(prices, window=20):
    """Generate mean reversion signals using Bollinger Bands."""
    sma = np.mean(prices[-window:])
    std = np.std(prices[-window:])
    
    if prices[-1] < sma - 2*std:
        return "BUY"  # Price too low
    elif prices[-1] > sma + 2*std:
        return "SELL"  # Price too high
    else:
        return "HOLD"
```

**Exit Rules:**
- Target: Return to SMA + profit buffer
- Stop loss: Break below 3-std band
- Time decay: 15-day hold

### 3. Sentiment-Based Strategy

**Concept:**
Use sentiment analysis from news and social media to predict price moves.

**Data Sources:**
- MSE news releases
- Financial news aggregators
- Social media monitoring
- Corporate announcements

**Signal Generation:**
```python
def sentiment_score(news_articles, sentiment_model):
    """Calculate aggregate sentiment score."""
    scores = [sentiment_model.predict(article) for article in news_articles]
    aggregate = np.mean(scores)
    
    if aggregate > 0.7:
        return "STRONG_BUY"
    elif aggregate > 0.5:
        return "BUY"
    elif aggregate < -0.7:
        return "STRONG_SELL"
    elif aggregate < -0.5:
        return "SELL"
    else:
        return "NEUTRAL"
```

### 4. Fundamental Value Strategy

**Concept:**
Identify undervalued stocks based on financial metrics.

**Key Metrics:**
- Price-to-Earnings (P/E) ratio
- Price-to-Book (P/B) ratio
- Price-to-Sales (P/S) ratio
- Dividend yield
- ROE (Return on Equity)

**Valuation Screen:**
```python
def value_screen(stocks_data, thresholds):
    """Identify undervalued stocks."""
    candidates = []
    
    for stock in stocks_data:
        pe_ratio = stock['price'] / stock['earnings_per_share']
        industry_pe = calculate_industry_average_pe(stock['industry'])
        
        if pe_ratio < industry_pe * 0.8:  # 20% below industry
            if stock['dividend_yield'] > 0.05:  # >5% yield
                candidates.append(stock)
    
    return sorted(candidates, key=lambda x: x['pe_ratio'])
```

### 5. Statistical Arbitrage

**Concept:**
Exploit statistical relationships between securities.

**Implementation:**
```python
from scipy.stats import linregress

def pairs_trading_signal(price1, price2, window=60):
    """Identify statistical arbitrage opportunities."""
    # Calculate correlation
    returns1 = np.diff(price1) / price1[:-1]
    returns2 = np.diff(price2) / price2[:-1]
    
    correlation = np.corrcoef(returns1[-window:], returns2[-window:])[0, 1]
    
    if correlation > 0.7:  # High correlation
        # Calculate spread
        slope, intercept, _, _, _ = linregress(price1[-window:], price2[-window:])
        expected_price2 = slope * price1[-1] + intercept
        spread = price2[-1] - expected_price2
        
        if spread > 2 * np.std(spread):  # Deviation > 2 std
            return "SELL_PAIR"  # Sell overvalued, buy undervalued
```

---

## 💼 Position Management

### Position Sizing

**Fixed Fractional Position Sizing:**
```python
def calculate_position_size(portfolio_value, risk_amount, stop_loss_percent):
    """Calculate number of shares to trade."""
    risk_per_share = portfolio_value * stop_loss_percent / 100
    shares = risk_amount / risk_per_share
    return shares
```

**Risk Percent:** 1-2% of portfolio per trade

### Portfolio Rebalancing

**Monthly Rebalancing:**

```python
def rebalance_portfolio(current_allocation, target_allocation):
    """Rebalance portfolio to target weights."""
    rebalancing_trades = {}
    
    for asset, target_weight in target_allocation.items():
        current_weight = current_allocation.get(asset, 0)
        diff = target_weight - current_weight
        
        if abs(diff) > 0.02:  # Rebalance if diff > 2%
            rebalancing_trades[asset] = diff
    
    return rebalancing_trades
```

**Triggers for Rebalancing:**
- Quarterly review
- Allocation drift > 2%
- Major market events
- Strategy performance change

---

## 📊 Performance Tracking

### Key Performance Indicators (KPIs)

```python
class PortfolioPerformance:
    def __init__(self, returns, benchmark_returns):
        self.returns = returns
        self.benchmark = benchmark_returns
    
    def sharpe_ratio(self, risk_free_rate=0.02):
        """Risk-adjusted return metric."""
        excess_returns = self.returns - risk_free_rate/252
        return np.mean(excess_returns) * 252 / (np.std(excess_returns) * np.sqrt(252))
    
    def sortino_ratio(self, target_return=0):
        """Downside risk-adjusted return."""
        excess_returns = self.returns - target_return
        downside_returns = excess_returns[excess_returns < 0]
        downside_vol = np.std(downside_returns) * np.sqrt(252)
        return np.mean(self.returns) * 252 / downside_vol
    
    def maximum_drawdown(self):
        """Largest peak-to-trough decline."""
        cumulative = np.cumprod(1 + self.returns)
        running_max = np.maximum.accumulate(cumulative)
        drawdown = (cumulative - running_max) / running_max
        return np.min(drawdown)
    
    def calmar_ratio(self):
        """Return per unit of drawdown risk."""
        annual_return = np.mean(self.returns) * 252
        max_drawdown = abs(self.maximum_drawdown())
        return annual_return / max_drawdown
    
    def information_ratio(self):
        """Excess return vs benchmark per unit of tracking error."""
        excess_returns = self.returns - self.benchmark
        tracking_error = np.std(excess_returns) * np.sqrt(252)
        return np.mean(excess_returns) * 252 / tracking_error
    
    def alpha(self, market_returns, risk_free_rate=0.02):
        """Jensen's alpha - excess return beyond market."""
        excess_portfolio = np.mean(self.returns) - risk_free_rate/252
        excess_market = np.mean(market_returns) - risk_free_rate/252
        beta = np.cov(self.returns, market_returns)[0,1] / np.var(market_returns)
        
        expected_return = risk_free_rate/252 + beta * excess_market
        alpha = np.mean(self.returns) - expected_return
        return alpha * 252
```

### Performance Dashboard

**Daily Metrics:**
- Total Return
- Daily P&L
- Portfolio Value
- Positions Summary

**Weekly Metrics:**
- Weekly Return
- Sharpe Ratio (YTD)
- Maximum Drawdown
- Win Rate

**Monthly Metrics:**
- Monthly Return
- vs Benchmark
- Drawdown Duration
- Strategy Performance

---

## ⚠️ Risk Management

### Risk Limits

```python
class RiskManager:
    def __init__(self, portfolio_value):
        self.portfolio_value = portfolio_value
        self.limits = {
            'single_position': 0.05,      # Max 5% in one stock
            'sector_exposure': 0.30,      # Max 30% in one sector
            'country_exposure': 1.0,      # 100% (only MSE)
            'leverage': 1.0,              # No leverage
            'max_drawdown': 0.15,         # Stop at 15% drawdown
            'daily_loss_limit': 0.02      # Stop at 2% daily loss
        }
    
    def check_position_limit(self, position_value):
        """Ensure position doesn't exceed limit."""
        position_pct = position_value / self.portfolio_value
        return position_pct <= self.limits['single_position']
    
    def check_sector_limit(self, sector, exposure):
        """Ensure sector doesn't exceed limit."""
        return exposure <= self.limits['sector_exposure']
    
    def check_drawdown(self, current_value, peak_value):
        """Monitor drawdown against limit."""
        drawdown = (peak_value - current_value) / peak_value
        if drawdown > self.limits['max_drawdown']:
            return False, f"Drawdown limit exceeded: {drawdown:.2%}"
        return True, "OK"
    
    def check_daily_loss(self, daily_return):
        """Monitor daily losses."""
        if daily_return < -self.limits['daily_loss_limit']:
            return False, f"Daily loss limit exceeded"
        return True, "OK"
```

### Stop Loss & Take Profit

```python
def set_stops_and_limits(entry_price, strategy_type):
    """Set stop-loss and take-profit levels."""
    if strategy_type == 'momentum':
        stop_loss = entry_price * 0.98      # 2% stop
        take_profit = entry_price * 1.05    # 5% target
    
    elif strategy_type == 'mean_reversion':
        stop_loss = entry_price * 0.96      # 4% stop
        take_profit = entry_price * 1.03    # 3% target
    
    elif strategy_type == 'arbitrage':
        stop_loss = entry_price * 0.995     # 0.5% tight stop
        take_profit = entry_price * 1.02    # 2% target
    
    return stop_loss, take_profit
```

---

## 📋 Portfolio Review Process

### Monthly Review

**Steps:**
1. Calculate performance metrics
2. Analyze strategy performance
3. Review risk exposures
4. Rebalance if needed
5. Document findings

**Report Template:**
```markdown
## Portfolio Performance Report - February 2026

### Summary
- Portfolio Value: MWK 10,500,000
- Month Return: +2.3%
- YTD Return: +5.1%
- Max Drawdown: -4.2%

### Strategy Performance
| Strategy | Return | Win Rate | Sharpe |
|----------|--------|----------|--------|
| Momentum | +3.2% | 62% | 1.8 |
| Mean Reversion | +1.5% | 58% | 1.2 |
| Sentiment | +0.8% | 55% | 0.9 |

### Positions
- JDH: 15,000 shares @ 25.50 = MWK 382,500 (3.6%)
- NBM: 50 shares @ 11,719.83 = MWK 585,991 (5.6%)
- ...

### Risk Analysis
- Current Drawdown: -2.1%
- Leverage: 0% (net long 95%)
- Sector Concentration: Acceptable

### Adjustments Made
- Rebalanced after ILLOVO gain
- Took profits on momentum winners
- Added to mean reversion positions
```

---

## 📚 Best Practices

### DO:
- ✅ Keep detailed trading logs
- ✅ Document all decisions
- ✅ Monitor risk daily
- ✅ Review performance regularly
- ✅ Stress test strategies
- ✅ Maintain position discipline
- ✅ Honor stop losses
- ✅ Track tax implications

### DON'T:
- ❌ Over-concentrate positions
- ❌ Ignore stop losses
- ❌ Chase losses (revenge trading)
- ❌ Make emotional decisions
- ❌ Use excessive leverage
- ❌ Neglect risk management
- ❌ Forget tax consequences
- ❌ Assume past performance continues

---

## 📞 Support & Questions

For portfolio-related questions:
1. Check this guide first
2. Review past performance reports
3. Consult risk management committee
4. Document any exceptions

---

*Last Updated: February 8, 2026*
