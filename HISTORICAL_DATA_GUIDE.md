# Historical Data Implementation Guide

## 📊 Overview

Your MSE Dashboard now supports **historical data analysis** with:
- ✅ Time-series price tracking
- ✅ Volume analysis
- ✅ Multi-stock comparisons
- ✅ Historical statistics (high, low, average, volatility)
- ✅ SQLite database for efficient data storage
- ✅ Date range filtering

---

## 🚀 Quick Start

### Step 1: Run the Scraper
The scraper automatically aggregates historical data now:

```bash
# In Jupyter or Python
python scrapper.ipynb
```

This will:
1. Scrape current MSE data
2. Save timestamped CSV files
3. **Automatically aggregate into SQLite database**
4. Export historical JSON for the dashboard

### Step 2: Access Historical Dashboard

Open the new enhanced dashboard:
```
MSE-Dashboard/mse_dashboard_historical_enhanced.html
```

---

## 🏗️ Architecture

### Components

#### 1. **Historical Data Manager** (`historical_data_manager.py`)
```
├── init_database()              → Create SQLite tables
├── aggregate_csv_files()        → Load timestamped CSVs into database
├── get_stock_history()          → Query data by symbol and date range
├── get_price_series()           → Get time series for analysis
├── export_historical_json()     → Export to JSON for dashboard
├── generate_daily_summary()     → Calculate daily statistics
└── run_full_sync()              → Run complete sync pipeline
```

#### 2. **Enhanced Dashboard** (`mse_dashboard_historical_enhanced.html`)
```
├── Date Range Controls
│   ├── Start/End Date Picker
│   ├── Quick Range Selector (7, 30, 90 days)
│   └── Load/Compare Buttons
├── Statistics Display
│   ├── Period High/Low
│   ├── Average Price
│   ├── Volatility
│   ├── Period Change %
│   └── Average Volume
├── Charts
│   ├── Price Trend (Line Chart)
│   ├── Volume Trend (Bar Chart)
│   └── Multi-Stock Comparison (Line Chart)
└── Historical Data Table
    └── Date, Symbol, OHLC, Volume, Turnover
```

#### 3. **Database Schema** (`mse_historical.db`)
```sql
-- stocks_history table
CREATE TABLE stocks_history (
    date TEXT,
    symbol TEXT,
    open_price REAL,
    close_price REAL,
    change_percent REAL,
    volume REAL,
    turnover REAL,
    timestamp TEXT
);

-- indices_history table
CREATE TABLE indices_history (
    date TEXT,
    symbol TEXT,
    value REAL,
    change REAL,
    timestamp TEXT
);

-- daily_summary table
CREATE TABLE daily_summary (
    date TEXT,
    total_stocks INTEGER,
    gainers INTEGER,
    losers INTEGER,
    avg_change REAL,
    total_volume REAL,
    total_turnover REAL
);
```

---

## 💾 Data Flow

```
scrapper.ipynb
     ↓
Scrapes MSE data
     ↓
Saves timestamped CSVs:
  - mse_stocks_YYYYMMDD_HHMMSS.csv
  - mse_indices_YYYYMMDD_HHMMSS.csv
     ↓
Calls historical_data_manager.py
     ↓
├─ aggregate_csv_files()
│   └─ Load all CSVs into SQLite database
├─ export_historical_json()
│   └─ Export to mse_historical_data.json
└─ generate_daily_summary()
    └─ Calculate daily statistics
     ↓
Dashboard loads mse_historical_data.json
     ↓
User filters by date/symbol and visualizes
```

---

## 🎯 How to Use

### Viewing Historical Data

1. **Open Dashboard**
   - Open `mse_dashboard_historical_enhanced.html` in browser

2. **Select Date Range**
   - Use "Start Date" and "End Date" pickers
   - OR select "Quick Range" (7, 30, 90 days)

3. **Choose Stock Symbol**
   - Select from dropdown populated with all available stocks

4. **Load Data**
   - Click "📊 Load Data" button

5. **View Results**
   - See historical statistics (high, low, average, volatility)
   - Price trend chart shows entire period
   - Volume trend below
   - Scrollable table with detailed data

### Comparing Multiple Stocks

1. Select up to 3 stocks in the comparison section
2. Click "Compare" button
3. View overlaid price trends for comparison

---

## 📈 Key Features & Examples

### Feature 1: Price Trend Analysis
```
Shows closing price over time with:
- Green line for price movement
- Shaded area under curve
- Date labels on x-axis
- Price values on y-axis
```

### Feature 2: Volatility Calculation
```
Formula: √(Variance of prices / Mean price)

Example:
  If prices fluctuate wildly = HIGH volatility
  If prices stable = LOW volatility
```

### Feature 3: Period Statistics
```
- Period High: Maximum closing price in range
- Period Low: Minimum closing price in range
- Average Price: Mean of all closing prices
- Volatility %: Standard deviation as percentage
- Period Change %: (Last - First) / First × 100
- Avg Daily Volume: Mean trading volume
```

### Feature 4: Quick Navigation
```
Quick Range Selector:
- "Last 7 Days": Last week's data
- "Last 30 Days": Last month's data
- "Last 90 Days": Last quarter's data
- "Custom Range": Pick your own dates
```

---

## 🔧 Configuration & Customization

### Change Data Directory
In `historical_data_manager.py`:
```python
manager = HistoricalDataManager(data_dir="custom_path")
```

### Change Database File
```python
manager = HistoricalDataManager(db_file="custom_name.db")
```

### Change Historical Data Export Location
In dashboard HTML, update:
```javascript
const HISTORICAL_DATA_FILE = '../mse_data/mse_historical_data.json';
```

### Customize Chart Colors
In dashboard HTML, modify chart datasets:
```javascript
{
    borderColor: '#00ff88',      // Change from green
    backgroundColor: 'rgba(0, 255, 136, 0.1)'
}
```

---

## 📊 Database Queries

### Get Historical Data for a Symbol
```python
from historical_data_manager import HistoricalDataManager

manager = HistoricalDataManager()
data = manager.get_stock_history(
    symbol='AIRTEL',
    start_date='2026-01-01',
    end_date='2026-02-10'
)
print(data)
```

### Get Price Series for Analysis
```python
series = manager.get_price_series(
    symbol='NBM',
    start_date='2026-01-01',
    end_date='2026-02-10'
)
# Returns: date, close_price, volume, change_percent
```

### Get Available Dates
```python
dates = manager.get_available_dates()
print(f"Data available from {dates[-1]} to {dates[0]}")
```

### Generate Daily Summary
```python
manager.generate_daily_summary()
# Creates statistics by date in daily_summary table
```

---

## 🐛 Troubleshooting

### Problem: Historical data not loading in dashboard
**Solution:**
1. Ensure `mse_historical_data.json` exists in `mse_data/` directory
2. Run the scraper first to generate data:
   ```python
   python scrapper.ipynb
   ```
3. Check browser console (F12) for errors
4. Verify file path in dashboard matches actual location

### Problem: No date options showing
**Solution:**
1. Check if `mse_historical.db` was created
2. Verify scraper ran successfully
3. Run `historical_data_manager.run_full_sync()` manually

### Problem: Charts not displaying
**Solution:**
1. Ensure Chart.js is loaded (check console)
2. Verify data is not empty for selected range
3. Check browser console for JavaScript errors

### Problem: Empty table results
**Solution:**
1. Check if data exists for selected symbol and date range
2. Try a broader date range
3. Verify symbol spelling matches exactly
4. Check if database has been populated

---

## 📝 Manual Data Sync

If you want to manually sync historical data:

```bash
python
>>> from historical_data_manager import HistoricalDataManager
>>> manager = HistoricalDataManager()
>>> manager.run_full_sync()
```

Output:
```
============================================================
HISTORICAL DATA SYNC
============================================================

📊 Aggregating historical data from CSV files...
  ✓ Loaded 20 stocks from 2026-02-10
  ✓ Loaded 20 stocks from 2026-02-09
  ✓ Loaded indices from 2026-02-10
  ✓ Loaded indices from 2026-02-09
✓ Aggregation complete!

✓ Historical data exported to mse_data/mse_historical_data.json
✓ Daily summaries generated!

✓ Total dates available: 2
  Date range: 2026-02-09 to 2026-02-10
============================================================
```

---

## 🎨 Dashboard Customization

### Colors & Styling
Edit the `<style>` section in `mse_dashboard_historical_enhanced.html`:

```css
:root {
    --bg-primary: #000000;        /* Main background */
    --bg-secondary: #1a1a1a;      /* Secondary background */
    --bg-card: #252525;           /* Card background */
    --text-primary: #ffffff;      /* Main text */
    --text-secondary: #b0b0b0;    /* Secondary text */
    --border-color: #404040;      /* Borders */
}
```

### Add More Historical Features

**Example: Add 52-week high/low:**
```javascript
// In calculateStatistics()
const last52weeks = data.slice(-252); // Approx 252 trading days
const high52w = Math.max(...last52weeks.map(d => parseFloat(d.close_price)));
const low52w = Math.min(...last52weeks.map(d => parseFloat(d.close_price)));
```

---

## 🔄 Integration with Daily Scraping

To automatically update historical data daily:

```python
# In scrapper.ipynb, after scraper.run()
from historical_data_manager import HistoricalDataManager
import schedule
import time

def daily_sync():
    scraper = MSEScraper()
    scraper.run()
    
    manager = HistoricalDataManager()
    manager.run_full_sync()

# Schedule for 9 AM daily
schedule.every().day.at("09:00").do(daily_sync)

# Run scheduler
while True:
    schedule.run_pending()
    time.sleep(1)
```

---

## 📚 Related Files

- **Scraper**: `scrapper.ipynb` - Data collection
- **Historical Manager**: `historical_data_manager.py` - Data aggregation
- **Dashboard (Current)**: `mse_dashboard.html` - Latest data view
- **Dashboard (Enhanced)**: `mse_dashboard_historical_enhanced.html` - Historical analysis
- **Database**: `mse_data/mse_historical.db` - SQLite historical storage
- **Export**: `mse_data/mse_historical_data.json` - JSON export for dashboard
- **Data Directory**: `mse_data/` - All CSV/JSON data files

---

## 🚀 Next Steps

1. **Run the scraper** to populate historical data
2. **Open the enhanced dashboard** to view historical trends
3. **Compare stocks** using the comparison feature
4. **Analyze volatility** and price movements
5. **Export data** for further analysis

---

## 📞 Support

For issues or questions:
1. Check the **Troubleshooting** section above
2. Review **Data Flow** diagram
3. Check browser console (F12) for errors
4. Verify file paths and data existence

---

*Last Updated: February 10, 2026*
*Rafund Investment Management*
