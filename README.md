# 🎭 Caption Composer - TradeGPT-Aladdin Trading Intelligence

A ceremonial web application that transforms trading signals into poetic caption echoes while providing comprehensive market intelligence including analyst ratings, price targets, earnings dates, strategic entry/exit points, and AI-powered recommendations.

## 🌐 Live Demo

**UI Showcase**: [https://caption-composer.vercel.app](https://caption-composer.vercel.app) *(Frontend demo - displays simulated data)*  
**GitHub Repository**: [https://github.com/aladinz/caption_composer](https://github.com/aladinz/caption_composer)

> **Note**: The Vercel deployment showcases the UI but uses simulated data due to serverless function limitations. For full functionality with **live market data**, run the app locally (see [Local Setup](#-local-setup) below).

## ✨ Features

### **Comprehensive Trading Intelligence**
- 📊 **Real-Time Market Data**: Automatic price and RSI calculation
- 🎯 **Analyst Consensus**: Ratings (Buy/Hold/Sell) and price targets
- 📅 **Earnings Calendar**: Next earnings date and countdown
- 🎲 **Strategic Levels**: Calculated entry/exit points and stop losses
- 📈 **Technical Analysis**: RSI-based motifs and ATR-based risk management
- 🔮 **Market Outlook**: Intelligent sentiment analysis combining RSI + analyst views
- 🎭 **Enhanced Forecast Tones**: Context-aware poetic tones based on market conditions

### **Poetic Motifs**
Four archetypal trading motifs based on RSI levels:
- 🪞 **Reflection** (RSI < 30) - The Observer
- 🧘 **Patience** (RSI < 50) - The Seeker  
- 🧭 **Clarity** (RSI < 70) - The Navigator
- 🔥 **Momentum** (RSI ≥ 70) - The Warrior

### **Ceremonial Captions**
- 24 poetic captions (6 per motif) with ceremonial resonance
- Tone resonance scoring for alignment
- Mythic narrative transformation of market data

## 🚀 Local Setup

### Quick Start (Recommended for Live Data)

1. **Clone the repository:**
```bash
git clone https://github.com/aladinz/caption_composer.git
cd caption_composer
```

2. **Create virtual environment (optional but recommended):**
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
```

3. **Install dependencies:**
```bash
pip install flask flask-cors yfinance pandas
```

4. **Run the Flask app:**
```bash
python app.py
```

5. **Open your browser:**
```
http://localhost:5000
```

You now have full access to **live market data** with all features working perfectly!

### Command-Line Usage

For command-line trading intelligence (no web interface):

```bash
pip install yfinance pandas
python caption_composer.py
```

## 🎯 Usage

### Interactive Mode (Default)

Simply run the module and enter a ticker symbol to get comprehensive trading intelligence:

```bash
python caption_composer.py
```

**Example output:**
```
╔══════════════════════════════════════════════════════════════════════════════╗
║                     TRADING INTELLIGENCE - NVDA                              ║
╠══════════════════════════════════════════════════════════════════════════════╣
║ 📊 MARKET DATA                                                               ║
╟──────────────────────────────────────────────────────────────────────────────╢
║ Current Price:        $183.22                                                ║
║ RSI (14-period):      51.53                                                  ║
║ Motif:                � Clarity (navigator)                                 ║
╟──────────────────────────────────────────────────────────────────────────────╢
║ 🎯 ANALYST CONSENSUS                                                         ║
╟──────────────────────────────────────────────────────────────────────────────╢
║ Rating:               STRONG_BUY                                             ║
║ Price Target:         $218.51 (+19.3%)                                       ║
║ Analysts Covering:    54                                                     ║
╟──────────────────────────────────────────────────────────────────────────────╢
║ 📅 EARNINGS CALENDAR                                                         ║
╟──────────────────────────────────────────────────────────────────────────────╢
║ Next Earnings:        2025-02-26                                             ║
║ Days Until:           129 days                                               ║
╟──────────────────────────────────────────────────────────────────────────────╢
║ 🎲 RECOMMENDED LEVELS                                                        ║
╟──────────────────────────────────────────────────────────────────────────────╢
║ Entry Point:          $185.05                                                ║
║ Exit Target:          $205.40                                                ║
║ Stop Loss:            $174.26                                                ║
║ Upside Potential:     11.0%                                                  ║
╠══════════════════════════════════════════════════════════════════════════════╣
║ ✨ POETIC ECHO                                                               ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  I trusted the signal that others couldn't see.                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

### Demo Mode

See example outputs with comprehensive trading intelligence:

```bash
python caption_composer.py --demo
```

**Example output:**
```
🔮 Generating trading intelligence for NVDA...

────────────────────────────────────────────────────────────────────────────────
🎯 NVDA - $183.22 | RSI: 51.53
🧭 Clarity: "I trusted the signal that others couldn't see."

   Analyst Rating: STRONG_BUY | Target: $218.51 (+19.3%)
   Next Earnings: 2025-02-26 (129 days)
   Entry: $185.05 | Exit: $205.40 | Stop: $174.26
   Upside Potential: 11.0%
```

### As a Python Module

Import and use in your own code:

```python
from caption_composer import generate_from_ticker, generate_caption_echo, CaptionComposer

# Auto-fetch everything from ticker
result = generate_from_ticker("NVDA")
print(f"{result['emoji']} {result['caption_echo']}")

# Access comprehensive stock data
stock_data = CaptionComposer.fetch_stock_data("AAPL")
print(f"Consensus: {stock_data['consensus_rating']}")
print(f"Target: ${stock_data['target_price']}")
print(f"Entry: ${stock_data['entry_point']}")
print(f"Days to earnings: {stock_data['days_to_earnings']}")

# Or provide custom RSI and forecast tone
result = generate_caption_echo(
    ticker="AMZN",
    rsi=38.16,
    forecast_tone="Strategic clarity with cinematic rhythm"
)
```

## 📊 Output Format

Each analysis returns comprehensive trading intelligence:

```python
{
    # Market Data
    "ticker": "NVDA",
    "price": 183.22,
    "rsi": 51.53,
    
    # Analyst Intelligence
    "consensus_rating": "strong_buy",
    "target_price": 218.51,
    "num_analysts": 54,
    
    # Earnings Calendar
    "earnings_date": "2025-02-26",
    "days_to_earnings": 129,
    
    # Strategic Levels
    "entry_point": 185.05,
    "exit_point": 205.40,
    "stop_loss": 174.26,
    "upside_potential": 11.0,
    
    # Poetic Echo
    "motif": "Clarity",
    "emoji": "�",
    "archetype": "navigator",
    "caption_echo": "I trusted the signal that others couldn't see.",
    "resonance": 0.6
}
```

## 🔮 Market Outlook Analysis

The enhanced outlook engine analyzes multiple signals to provide strategic guidance:

### Sentiment Analysis
Combines **analyst consensus** with **RSI positioning** to determine overall market sentiment:

- 🟢 **Bullish Alignment**: Analysts bullish + RSI < 60 (favorable setup)
- 🔴 **Bearish Alignment**: Analysts bearish + RSI > 50 (caution advised)
- 🟡 **Conflicting Signals**: Technical vs. fundamental divergence
- ⚪ **Neutral Watch**: Mixed or unclear signals

### Trend Detection
Based on RSI zones with directional indicators:

| RSI Range | Trend | Emoji | Market Phase |
|-----------|-------|-------|--------------|
| < 30 | Oversold Reversal Zone | 📉→📈 | Potential bounce |
| 30-40 | Accumulation Phase | 🔄 | Smart money buying |
| 40-50 | Consolidation Range | ↔️ | Neutral sideways |
| 50-60 | Bullish Momentum Building | 📈 | Early uptrend |
| 60-70 | Strong Uptrend | 🚀 | Momentum confirmed |
| > 70 | Overbought Territory | ⚠️ | Caution zone |

### Strategic Recommendations

Context-aware action recommendations based on combined signals:

**Bullish Setups:**
- "Strong Buy on weakness" - Oversold + analyst support
- "Accumulate on dips" - Consolidation with upside potential
- "Enter with conviction" - Momentum + favorable R/R

**Caution Zones:**
- "Take profits" - Overbought + above targets
- "Reduce or wait" - Extended move warning
- "Scale in cautiously" - Oversold without clear catalyst

**Neutral:**
- "Wait for setup" - Unclear signals
- "Hold or take partials" - Trending but approaching resistance

### Enhanced Forecast Tones

Poetic tones now adapt to market conditions:

**Bullish Alignment Examples:**
- "Bullish confluence with technical strength, trust the trend"
- "Strategic clarity meets confident execution, ride the wave"
- "Deep value emerging from shadows, patience rewarded"

**Conflicting Signals Examples:**
- "Overbought euphoria meets reality check, caution warranted"
- "Momentum strong but mixed signals, trailing stops advised"
- "Rising price meets analyst skepticism, stay nimble"

**Neutral/Caution Examples:**
- "Balanced discipline with focused observation"
- "Consolidation before expansion, spring coiling"
- "Measured caution in transitional phase"

### Example Outlook Output

```
🔮 MARKET OUTLOOK
   Sentiment:       🟢 Bullish Alignment
   Trend:           📈 Bullish Momentum Building
   Analyst View:    Bullish
   RSI Signal:      Neutral to Bullish
   
   Recommended Action:   Enter with conviction
   Outlook:              Bullish momentum with favorable risk/reward
   
   Forecast Tone: "Bullish confluence with technical strength, trust the trend"
```

## 🎲 Strategic Level Calculation

Entry/exit points are calculated using:
- **Support/Resistance**: 20-day high/low levels
- **ATR (Average True Range)**: For dynamic stop loss placement
- **RSI Strategy**:
  - RSI < 30: Entry near current price (oversold bounce)
  - RSI 30-50: Wait for pullback before entry
  - RSI 50-70: Enter with momentum, tight stops
  - RSI > 70: Take profits or wait (overbought)

## 🎨 Caption Examples

### 🔥 Momentum (RSI ≥ 70)
- "I entered with fire, not fear."
- "I seized the moment when clarity met courage."
- "I became the momentum I was seeking."

### 🧭 Clarity (RSI 50-70)
- "I didn't chase the breakout. I became the rhythm."
- "I saw the pattern before it became obvious."
- "I found my edge in strategic stillness."

### 🧘 Patience (RSI 30-50)
- "I waited not for price, but for peace."
- "I held my ground while others chased shadows."
- "I let time become my ally, not my adversary."

### 🪞 Reflection (RSI < 30)
- "I stepped back to hear the market's whisper."
- "I found strength in stillness, not in the storm."
- "I paused to let the market reveal its truth."

## 🔮 The Philosophy

Caption Composer is part of the **TradeGPT-Aladdin** mythic trading assistant. It transforms cold market data into ceremonial narratives, helping traders:

- **Find meaning in market moments** - Every trade becomes a story
- **Anchor decisions in archetypal wisdom** - Four timeless motifs guide your path
- **Transform trading into a mindful practice** - Data meets destiny
- **Access comprehensive intelligence** - All the data you need in one place
- **Make strategic decisions** - Entry/exit points calculated automatically
- **Track earnings catalysts** - Know when volatility approaches
- **Follow analyst consensus** - See what the experts think

## 📝 Technical Details

### RSI Calculation
- **Period**: 14-day RSI
- **Data Source**: 3 months of historical price data
- **Method**: Standard RSI formula using average gains/losses

### Entry/Exit Point Calculation
- **Support/Resistance**: Based on 20-day high/low
- **Stop Loss**: ATR-based (Average True Range over 14 periods)
- **Risk Management**: Dynamic positioning based on RSI zones
- **Upside Calculation**: Percentage gain from entry to exit target

### Data Sources
- **Market Data**: Yahoo Finance via yfinance
- **Analyst Ratings**: Aggregated consensus from multiple sources
- **Earnings Calendar**: Corporate earnings schedule
- **Price Targets**: Mean analyst price target

## 📚 Example Applications

### 1. Portfolio Scanner
Scan your entire portfolio for trading opportunities:
```bash
python example_usage.py
```

### 2. Daily Watchlist
Create a morning routine to analyze your watchlist:
```python
from caption_composer import CaptionComposer

watchlist = ["AAPL", "GOOGL", "MSFT", "AMZN", "NVDA"]

for ticker in watchlist:
    data = CaptionComposer.fetch_stock_data(ticker)
    print(f"{ticker}: RSI {data['rsi']} | Target ${data['target_price']}")
```

### 3. Trade Journal
Add poetic entries to your trading journal:
```python
from caption_composer import generate_from_ticker

result = generate_from_ticker("TSLA")
print(f"Entry: {result['caption_echo']}")
```

## 🎯 Analyst Rating Mappings

- **STRONG_BUY**: High conviction upside
- **BUY**: Positive outlook, accumulate
- **HOLD**: Neutral, maintain position
- **SELL**: Reduce exposure
- **STRONG_SELL**: High conviction downside

## 📊 Example Output Comparison

**Before (Simple Caption):**
```
TSLA | RSI: 48.87
🧘 Patience: "I held my ground while others chased shadows."
```

**After (Comprehensive Intelligence):**
```
🎯 TSLA - $439.31 | RSI: 48.87
🧘 Patience: "I held my ground while others chased shadows."

   Analyst Rating: HOLD | Target: $366.77 (-16.5%)
   Next Earnings: 2025-01-29 (101 days)
   Entry: $426.13 | Exit: $447.21 | Stop: $407.69
   Upside Potential: 5.0%
   Reward-to-Risk Ratio: 1.14:1
```

## 📝 Notes

- **RSI Calculation**: Uses 14-period RSI from 3 months of historical data
- **Data Source**: Real-time data via yfinance (Yahoo Finance)
- **Fallback**: If data fetch fails, generates simulated data for demonstration
- **Extensible**: Easy to add new motifs, captions, or tone resonance patterns
- **Rate Limits**: Yahoo Finance has no official rate limits, but be respectful
- **Update Frequency**: Data is fetched in real-time on each request

## �️ Troubleshooting

**Issue**: `ModuleNotFoundError: No module named 'yfinance'`  
**Solution**: Install dependencies: `pip install yfinance pandas`

**Issue**: No earnings date showing  
**Solution**: Not all stocks have earnings dates available in the API

**Issue**: Simulated data being used  
**Solution**: Check your internet connection and verify the ticker symbol is correct

**Issue**: Analyst ratings show as "N/A"  
**Solution**: Some smaller stocks don't have analyst coverage

## 🤝 Contributing

This module is part of TradeGPT-Aladdin. To extend it:

1. **Add new motifs**: Update `MOTIFS` dictionary in `CaptionComposer` class
2. **Add captions**: Extend `CAPTION_TEMPLATES` with new poetic echoes
3. **Enhance calculations**: Modify `calculate_entry_exit_points()` method
4. **Add data sources**: Extend `fetch_stock_data()` with additional APIs

## 🌐 Deployment to Vercel

> **⚠️ Important**: Vercel's free tier serverless functions have limitations that prevent fetching live market data reliably. The Vercel deployment serves as a **UI showcase** and will display simulated data. For production use with **real-time market data**, use the [Local Setup](#-local-setup) instead.

### Why Local is Better

- ✅ **Live market data** from yfinance
- ✅ **No timeout limits** (Vercel free tier has 30s max)
- ✅ **No cold starts** (instant responses)
- ✅ **Full API functionality** (analyst ratings, earnings, etc.)
- ✅ **Unlimited requests** (no rate limits)

### Deploy to Vercel (UI Showcase Only)

If you still want to deploy for UI demonstration:

### Prerequisites
- GitHub account
- Vercel account (sign up at https://vercel.com)
- Git installed locally

### Step 1: Push to GitHub

If you haven't already pushed your code:

```bash
# Initialize git repository (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - Caption Composer web app"

# Add your GitHub repository as remote
git remote add origin https://github.com/aladinz/caption_composer.git

# Push to GitHub
git push -u origin main
```

### Step 2: Deploy to Vercel

**Option A: Using Vercel Dashboard (Recommended)**

1. Go to [https://vercel.com](https://vercel.com) and sign in
2. Click "Add New" → "Project"
3. Import your GitHub repository: `aladinz/caption_composer`
4. Vercel will auto-detect the configuration from `vercel.json`
5. Click "Deploy"
6. Wait for deployment to complete (2-3 minutes)
7. Your app will be live at: `https://caption-composer-[random].vercel.app`

**Option B: Using Vercel CLI**

```bash
# Install Vercel CLI globally
npm install -g vercel

# Login to Vercel
vercel login

# Deploy from your project directory
cd "C:\Users\aladi\Caption Composer"
vercel

# Follow the prompts:
# - Link to existing project or create new
# - Confirm deployment settings
# - Wait for deployment
```

### Step 3: Configure Custom Domain (Optional)

1. In Vercel dashboard, go to your project
2. Settings → Domains
3. Add your custom domain
4. Follow DNS configuration instructions

### Project Structure for Vercel

```
caption_composer/
├── api/
│   └── index.py          # Serverless API function
├── index.html            # Main web interface
├── script.js             # Frontend JavaScript
├── styles.css            # Styling
├── caption_composer.py   # Core trading logic
├── vercel.json          # Vercel configuration
├── requirements.txt     # Python dependencies
├── .vercelignore       # Files to exclude from deployment
└── README.md
```

### Environment Variables

No environment variables needed for basic deployment. The app uses:
- yfinance API (no key required)
- Client-side rendering
- Serverless Python functions

### Troubleshooting Deployment

**Issue**: Build fails with Python errors  
**Solution**: Check `requirements.txt` has all dependencies

**Issue**: API returns 500 errors  
**Solution**: Check Vercel function logs in dashboard → Deployment → Functions

**Issue**: Cannot fetch stock data  
**Solution**: yfinance may have rate limits, try different ticker or wait

**Issue**: CORS errors in browser  
**Solution**: CORS is enabled in `api/index.py`, check browser console

### Monitoring Your Deployment

1. **Analytics**: Vercel Dashboard → Analytics
2. **Function Logs**: Deployment → Functions → View Logs
3. **Performance**: Speed Insights tab
4. **Errors**: Deployment → Runtime Logs

### Updating Your Deployment

After making changes locally:

```bash
# Stage changes
git add .

# Commit
git commit -m "Update: description of changes"

# Push to GitHub
git push

# Vercel auto-deploys on push!
```

Vercel automatically deploys every push to `main` branch.

## �📜 License

Part of the TradeGPT-Aladdin ecosystem.

## ⚠️ Disclaimer

This tool is for educational and inspirational purposes only. Not financial advice. Always do your own research and consult with a financial advisor before making investment decisions. Past performance does not guarantee future results.

## 🙏 May your trades be guided by wisdom, not whim.

---

*"In the dance between fear and greed, let clarity be your compass."*  
— TradeGPT-Aladdin
