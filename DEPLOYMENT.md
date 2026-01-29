# Streamlit Cloud Deployment Guide

## Two-Version Architecture

This project has **two versions** optimized for different use cases:

### 📱 Cloud Version (`app_cloud.py`) - Deploy This One
- **Lightweight**: No historical data storage
- **Mobile-optimized**: Simplified UI for quick access
- **Fast**: Reduced features = faster loading
- **Session-based**: Themes and settings persist during session only
- **Perfect for**: Mobile access, quick scans, sharing with others

### 💻 Local Version (`app.py`) - Keep This Local
- **Full-featured**: Historical snapshots, automated scans
- **Data persistence**: SQLite database for historical tracking
- **Scheduled scans**: Windows Task Scheduler integration
- **Complete control**: All data stored locally
- **Perfect for**: Daily automated scans, historical analysis, primary workflow

**Recommended Setup**: Deploy `app_cloud.py` to Streamlit Cloud for mobile access, keep `app.py` running locally for full features.

---

## Prerequisites

1. **GitHub Account** - You'll need a GitHub account to host your code
2. **Streamlit Community Cloud Account** - Sign up at [share.streamlit.io](https://share.streamlit.io)

## Step-by-Step Deployment

### 1. Prepare Your Repository

First, create a GitHub repository for your stock monitor:

1. Go to [github.com](https://github.com) and create a new repository
2. Name it something like `stock-monitor` or `us-stock-scanner`
3. Make it **Public** (required for free Streamlit Community Cloud)

### 2. Push Your Code to GitHub

Open PowerShell in your project directory and run:

```bash
cd C:\Users\User\.gemini\antigravity\scratch\stock_monitor

# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - US Stock Monitor"

# Add your GitHub repository as remote (replace with your actual repo URL)
git remote add origin https://github.com/YOUR_USERNAME/stock-monitor.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### 3. Deploy to Streamlit Cloud

1. **Go to Streamlit Cloud**: Visit [share.streamlit.io](https://share.streamlit.io)

2. **Sign in with GitHub**: Click "Sign in with GitHub"

3. **Create New App**:
   - Click "New app" button
   - Select your repository: `YOUR_USERNAME/stock-monitor`
   - Branch: `main`
   - Main file path: `src/app_cloud.py` ⚠️ **Important: Use cloud version!**
   - App URL: Choose a custom URL (e.g., `your-stock-monitor`)

4. **Click "Deploy"**: Streamlit will automatically:
   - Install dependencies from `requirements.txt`
   - Start your app
   - Provide a public URL

### 4. Access Your Deployed App

Your app will be live at:
```
https://YOUR-APP-NAME.streamlit.app
```

You can access it from anywhere - phone, tablet, or any browser!

## Important Considerations

### ⚠️ Data Persistence

**Issue**: Streamlit Community Cloud uses ephemeral storage - your data will be lost when the app restarts.

**Solutions**:

1. **Use Streamlit Secrets for API Keys** (if needed in future)
2. **External Database** (for persistent snapshots):
   - Use a free PostgreSQL database (e.g., Supabase, Neon)
   - Modify `storage.py` to use PostgreSQL instead of SQLite
   - Store connection string in Streamlit Secrets

3. **Accept Ephemeral Nature**:
   - Use cloud deployment for viewing/analysis only
   - Keep local version for historical snapshots
   - Run scheduled scans locally, view data on cloud

### 🔒 Privacy Considerations

**Your app will be PUBLIC** on Streamlit Community Cloud free tier.

If you want privacy:
- **Option 1**: Use Streamlit Cloud Teams ($20/month) for password protection
- **Option 2**: Deploy to your own server (Heroku, Railway, DigitalOcean)
- **Option 3**: Keep it local and use Tailscale/Ngrok for remote access

### 📊 Resource Limits

Streamlit Community Cloud free tier has:
- **1 GB RAM** - Should be sufficient for 503 stocks
- **1 CPU core** - Scans will be slower than local
- **Automatic sleep** - App sleeps after inactivity, wakes on access

### 🔄 Auto-Updates

Any changes you push to GitHub will automatically redeploy your app!

```bash
# Make changes locally
git add .
git commit -m "Update feature X"
git push

# App automatically redeploys in ~1-2 minutes
```

## Recommended Setup

For the best experience, I recommend a **hybrid approach**:

1. **Local Instance** (Primary):
   - Run scheduled snapshots daily at 6:00 AM
   - Store all historical data locally
   - Full control and privacy

2. **Cloud Instance** (Secondary):
   - Quick access from mobile/remote
   - Share with others if needed
   - Run ad-hoc scans only (no historical data)

## Alternative: Private Cloud Deployment

If you want a private cloud deployment with full features:

### Option A: Railway.app (Recommended)
- Free tier: 500 hours/month
- Persistent storage
- Private by default
- Easy deployment from GitHub

### Option B: Render.com
- Free tier available
- Persistent storage
- Private apps supported

### Option C: DigitalOcean App Platform
- $5/month
- Full control
- Persistent storage

## Files Needed for Deployment

✅ Already created:
- `requirements.txt` - Python dependencies
- `src/app.py` - Main application
- `src/data.py` - Data fetching logic
- `src/storage.py` - Storage functions

## Testing Before Deployment

Test locally to ensure everything works:

```bash
# Install from requirements.txt
pip install -r requirements.txt

# Run the app
streamlit run src/app.py
```

If it works locally, it will work on Streamlit Cloud!

## Troubleshooting

**App won't start:**
- Check logs in Streamlit Cloud dashboard
- Verify `requirements.txt` has all dependencies
- Ensure `src/app.py` path is correct

**Slow performance:**
- Reduce number of stocks in scan
- Add caching with `@st.cache_data`
- Consider upgrading to paid tier

**Data not persisting:**
- Expected behavior on free tier
- Use external database or keep local version

## Next Steps

Would you like me to:
1. Create a `.gitignore` file to exclude sensitive data?
2. Add caching to improve cloud performance?
3. Create a PostgreSQL version of `storage.py` for persistent cloud data?
4. Set up deployment to Railway/Render instead?

Let me know what you'd prefer!
