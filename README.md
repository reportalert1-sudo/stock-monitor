# US Stock Monitor

A powerful stock screening and monitoring application for S&P 500 stocks with advanced ranking, thematic tagging, and historical tracking.

## 🎯 Features

- **4-Dimensional Ranking System**: Combines YTD%, 5D%, Turnover Ratio (surge), and 20D Volume (abundance)
- **Interactive Leaderboards**: Drill down by themes, sectors, industries, and sub-industries
- **Custom Themes**: Tag stocks with your own investment themes
- **Color-Coded Insights**: Visual highlighting for performance and volume metrics
- **Persistent UI**: Save column order, widths, and table height preferences

## 📦 Two Versions

### 1. Local Version (`app.py`) - Full Featured
- ✅ Historical snapshot storage (SQLite)
- ✅ Automated daily scans via Windows Task Scheduler
- ✅ Date picker for historical analysis
- ✅ Complete data persistence
- ✅ Privacy and full control

**Use for**: Daily automated scans, historical tracking, primary analysis

### 2. Cloud Version (`app_cloud.py`) - Mobile Optimized
- ✅ Lightweight and fast
- ✅ Mobile-friendly interface
- ✅ Quick ad-hoc scans
- ✅ Session-based theme editing
- ❌ No historical data storage

**Use for**: Mobile access, quick checks, sharing with others

## 🚀 Quick Start

### Local Setup

1. **Install Dependencies**:
```bash
pip install -r requirements.txt
```

2. **Run the App**:
```bash
streamlit run src/app.py
```

Or use the convenience script:
```bash
run_monitor.bat
```

3. **Set Up Automated Scans** (Optional):
See `SCHEDULER_SETUP.md` for Windows Task Scheduler configuration.

### Cloud Deployment

See `DEPLOYMENT.md` for complete instructions to deploy to Streamlit Community Cloud.

**Quick Deploy**:
1. Push to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Select your repo
4. Set main file to: `src/app_cloud.py`
5. Deploy!

## 📊 How It Works

1. **Fetch Data**: Pulls real-time data from Yahoo Finance for all S&P 500 stocks
2. **Calculate Metrics**: Computes performance, volume, and turnover metrics
3. **Rank Stocks**: Multi-dimensional ranking system identifies top opportunities
4. **Interactive Analysis**: Filter, drill down, and tag stocks with custom themes
5. **Persist Insights**: Save themes, UI preferences, and historical snapshots

## 🎨 Color Coding

- 🟢🔴 **Green/Red**: Performance metrics (YTD%, 5D%)
- 🟠 **Orange**: Turnover Ratio (volume surge indicator)
- 🔵 **Blue**: Avg 20D Turnover (volume abundance)
- 🟢🔴 **Green/Red (reversed)**: Overall Rank (lower is better)

## 📁 Project Structure

```
stock_monitor/
├── src/
│   ├── app.py              # Local version (full features)
│   ├── app_cloud.py        # Cloud version (mobile optimized)
│   ├── data.py             # Data fetching and ranking logic
│   ├── storage.py          # Persistence layer (SQLite + JSON)
│   └── classifier.py       # Stock classification utilities
├── data/                   # Local data storage (gitignored)
│   ├── snapshots.db        # Historical snapshots
│   ├── metadata.parquet    # Stock metadata cache
│   ├── market_data.parquet # Market data cache
│   └── settings.json       # UI preferences
├── logs/                   # Scheduler logs (gitignored)
├── tests/                  # Test scripts
├── requirements.txt        # Python dependencies
├── DEPLOYMENT.md           # Cloud deployment guide
├── SCHEDULER_SETUP.md      # Automated scan setup
└── README.md               # This file
```

## ⏰ Automated Daily Scans

The local version supports automated daily scans via Windows Task Scheduler:

1. Configure scheduler to run at 6:00 AM HKT (5:00 PM ET previous day)
2. Automatically fetches data and saves snapshot
3. View historical data anytime via date picker

See `SCHEDULER_SETUP.md` for complete setup instructions.

## 🔒 Privacy

- **Local version**: 100% private, all data stored locally
- **Cloud version**: Public on free Streamlit tier (or upgrade for privacy)

## 📝 License

This project is for personal use. Market data provided by Yahoo Finance.

## 🙏 Acknowledgments

- **Data Source**: Yahoo Finance via `yfinance`
- **Framework**: Streamlit
- **Inspiration**: Value investing and momentum strategies
