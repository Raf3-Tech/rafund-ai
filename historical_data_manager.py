"""
Historical Data Manager for MSE Dashboard
Aggregates timestamped data files into a consolidated historical database
"""

import pandas as pd
import json
from pathlib import Path
from datetime import datetime
import sqlite3
import os

class HistoricalDataManager:
    """Manages historical data collection and aggregation"""
    
    def __init__(self, data_dir="mse_data", db_file="mse_historical.db"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        self.db_file = self.data_dir / db_file
        self.init_database()
    
    def init_database(self):
        """Initialize SQLite database with historical tables"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        # Create stocks history table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS stocks_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                symbol TEXT NOT NULL,
                open_price REAL,
                close_price REAL,
                change_percent REAL,
                volume REAL,
                turnover REAL,
                timestamp TEXT,
                UNIQUE(date, symbol)
            )
        ''')
        
        # Create indices history table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS indices_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                symbol TEXT NOT NULL,
                value REAL,
                change REAL,
                timestamp TEXT,
                UNIQUE(date, symbol)
            )
        ''')
        
        # Create daily summary table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS daily_summary (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT UNIQUE NOT NULL,
                total_stocks INTEGER,
                gainers INTEGER,
                losers INTEGER,
                avg_change REAL,
                total_volume REAL,
                total_turnover REAL
            )
        ''')
        
        conn.commit()
        conn.close()
        print(f"✓ Database initialized: {self.db_file}")
    
    def aggregate_csv_files(self):
        """Aggregate all timestamped CSV files into historical database"""
        print("\n📊 Aggregating historical data from CSV files...")
        
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        # Find all timestamped stock CSV files
        stock_files = sorted(self.data_dir.glob("mse_stocks_*.csv"))
        stock_files = [f for f in stock_files if "latest" not in f.name]
        
        for csv_file in stock_files:
            try:
                # Extract date from filename (YYYYMMDD)
                date_str = csv_file.stem.split("_")[2]  # mse_stocks_YYYYMMDD_HHMMSS
                date = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:8]}"
                
                df = pd.read_csv(csv_file)
                
                for _, row in df.iterrows():
                    cursor.execute('''
                        INSERT OR REPLACE INTO stocks_history 
                        (date, symbol, open_price, close_price, change_percent, volume, turnover, timestamp)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        date,
                        row['symbol'],
                        float(row['open_price']),
                        float(row['close_price']),
                        float(row['change_percent']),
                        float(row.get('volume', 0)),
                        float(row.get('turnover', 0)),
                        datetime.now().isoformat()
                    ))
                
                conn.commit()
                print(f"  ✓ Loaded {len(df)} stocks from {date}")
            
            except Exception as e:
                print(f"  ✗ Error processing {csv_file}: {e}")
        
        # Similarly for indices
        indices_files = sorted(self.data_dir.glob("mse_indices_*.csv"))
        indices_files = [f for f in indices_files if "latest" not in f.name]
        
        for csv_file in indices_files:
            try:
                date_str = csv_file.stem.split("_")[2]
                date = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:8]}"
                
                df = pd.read_csv(csv_file)
                
                for _, row in df.iterrows():
                    cursor.execute('''
                        INSERT OR REPLACE INTO indices_history 
                        (date, symbol, value, change, timestamp)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (
                        date,
                        row['symbol'],
                        float(row['value']),
                        float(row.get('change', 0)),
                        datetime.now().isoformat()
                    ))
                
                conn.commit()
                print(f"  ✓ Loaded indices from {date}")
            
            except Exception as e:
                print(f"  ✗ Error processing {csv_file}: {e}")
        
        conn.close()
        print("✓ Aggregation complete!")
    
    def get_stock_history(self, symbol=None, start_date=None, end_date=None):
        """Retrieve stock history for a symbol or all stocks in date range"""
        conn = sqlite3.connect(self.db_file)
        
        query = "SELECT * FROM stocks_history WHERE 1=1"
        params = []
        
        if symbol:
            query += " AND symbol = ?"
            params.append(symbol)
        
        if start_date:
            query += " AND date >= ?"
            params.append(start_date)
        
        if end_date:
            query += " AND date <= ?"
            params.append(end_date)
        
        query += " ORDER BY date ASC, symbol ASC"
        
        df = pd.read_sql_query(query, conn, params=params)
        conn.close()
        
        return df
    
    def get_price_series(self, symbol, start_date=None, end_date=None):
        """Get time series data for a single stock"""
        df = self.get_stock_history(symbol=symbol, start_date=start_date, end_date=end_date)
        return df[['date', 'close_price', 'volume', 'change_percent']]
    
    def export_historical_json(self):
        """Export aggregated historical data as JSON for dashboard"""
        conn = sqlite3.connect(self.db_file)
        
        # Get all unique dates
        dates_df = pd.read_sql_query(
            "SELECT DISTINCT date FROM stocks_history ORDER BY date DESC LIMIT 100", 
            conn
        )
        
        historical_data = {}
        
        for date in dates_df['date']:
            stocks_df = pd.read_sql_query(
                "SELECT * FROM stocks_history WHERE date = ? ORDER BY symbol",
                conn,
                params=(date,)
            )
            
            historical_data[date] = stocks_df.to_dict('records')
        
        conn.close()
        
        # Save to JSON
        json_file = self.data_dir / "mse_historical_data.json"
        with open(json_file, 'w') as f:
            json.dump(historical_data, f, indent=2)
        
        print(f"✓ Historical data exported to {json_file}")
        return json_file
    
    def get_available_dates(self):
        """Get list of available data dates"""
        conn = sqlite3.connect(self.db_file)
        dates_df = pd.read_sql_query(
            "SELECT DISTINCT date FROM stocks_history ORDER BY date DESC",
            conn
        )
        conn.close()
        
        return dates_df['date'].tolist()
    
    def generate_daily_summary(self):
        """Generate daily market summary statistics"""
        conn = sqlite3.connect(self.db_file)
        
        dates = self.get_available_dates()
        
        for date in dates:
            df = self.get_stock_history(start_date=date, end_date=date)
            
            if df.empty:
                continue
            
            gainers = len(df[df['change_percent'] > 0])
            losers = len(df[df['change_percent'] < 0])
            avg_change = df['change_percent'].mean()
            total_volume = df['volume'].sum()
            total_turnover = df['turnover'].sum()
            
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO daily_summary
                (date, total_stocks, gainers, losers, avg_change, total_volume, total_turnover)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                date,
                len(df),
                gainers,
                losers,
                avg_change,
                total_volume,
                total_turnover
            ))
            conn.commit()
        
        conn.close()
        print("✓ Daily summaries generated!")
    
    def run_full_sync(self):
        """Run complete sync: aggregate CSVs → export JSON → generate summaries"""
        print("\n" + "="*60)
        print("HISTORICAL DATA SYNC")
        print("="*60)
        
        self.aggregate_csv_files()
        self.export_historical_json()
        self.generate_daily_summary()
        
        available_dates = self.get_available_dates()
        print(f"\n✓ Total dates available: {len(available_dates)}")
        print(f"  Date range: {available_dates[-1]} to {available_dates[0]}")
        print("="*60 + "\n")


if __name__ == "__main__":
    manager = HistoricalDataManager()
    manager.run_full_sync()
