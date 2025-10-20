# 🎯 Caption Composer - Quick Reference Guide

## Command Line Usage

```bash
# Interactive mode (comprehensive intelligence)
python caption_composer.py

# Demo mode (quick examples)
python caption_composer.py --demo

# Run example portfolio analyzer
python example_usage.py
```

## Python API Reference

### Quick Functions

```python
from caption_composer import generate_from_ticker

# Simplest usage - get everything from ticker
result = generate_from_ticker("AAPL")
```

### Fetch Stock Data

```python
from caption_composer import CaptionComposer

# Get comprehensive trading intelligence
data = CaptionComposer.fetch_stock_data("NVDA")

# Returns:
{
    "ticker": "NVDA",
    "price": 183.22,
    "rsi": 51.53,
    "consensus_rating": "strong_buy",
    "target_price": 218.51,
    "num_analysts": 54,
    "earnings_date": "2025-02-26",
    "days_to_earnings": 129,
    "entry_point": 185.05,
    "exit_point": 205.40,
    "stop_loss": 174.26,
    "upside_potential": 11.0,
    "data_source": "yfinance"
}
```

### Generate Caption with Custom Data

```python
from caption_composer import generate_caption_echo

# Provide your own RSI and tone
result = generate_caption_echo(
    ticker="TSLA",
    rsi=45.2,
    forecast_tone="Strategic patience with clarity"
)
```

### Calculate Technical Levels

```python
import yfinance as yf
from caption_composer import CaptionComposer

# Get historical data
stock = yf.Ticker("AAPL")
hist = stock.history(period="3mo")
current_price = hist['Close'].iloc[-1]

# Calculate RSI
rsi = CaptionComposer.calculate_rsi(hist['Close'], period=14)

# Calculate entry/exit points
levels = CaptionComposer.calculate_entry_exit_points(hist, current_price, rsi)
print(f"Entry: ${levels['entry']}")
print(f"Exit: ${levels['exit']}")
print(f"Stop: ${levels['stop_loss']}")
print(f"Upside: {levels['upside_potential']}%")
```

## RSI Zones & Strategy

| RSI Range | Motif | Emoji | Strategy |
|-----------|-------|-------|----------|
| 0-29 | Reflection | 🪞 | Oversold - Look for bounce |
| 30-49 | Patience | 🧘 | Consolidation - Wait for confirmation |
| 50-69 | Clarity | 🧭 | Uptrend - Enter with momentum |
| 70-100 | Momentum | 🔥 | Overbought - Take profits or wait |

## Entry/Exit Logic by RSI

### RSI < 30 (Reflection)
- **Entry**: Near current price (0.99x)
- **Exit**: Midpoint to recent high
- **Stop**: 2 ATR below entry
- **Strategy**: Catching oversold bounce

### RSI 30-50 (Patience)
- **Entry**: Wait for 3% pullback (0.97x)
- **Exit**: Near recent high (0.95x)
- **Stop**: 1.5 ATR below entry
- **Strategy**: Buy the dip

### RSI 50-70 (Clarity)
- **Entry**: Enter with momentum (1.01x)
- **Exit**: Above recent high (1.05x)
- **Stop**: 1.5 ATR below entry
- **Strategy**: Ride the trend

### RSI > 70 (Momentum)
- **Entry**: Wait for pullback (None)
- **Exit**: Near current price (1.02x)
- **Stop**: 2 ATR below entry
- **Strategy**: Take profits or wait

## Example Workflows

### Morning Routine
```python
from caption_composer import CaptionComposer

watchlist = ["AAPL", "NVDA", "MSFT", "GOOGL", "AMZN"]

print("☀️ Morning Market Scan\n")
for ticker in watchlist:
    data = CaptionComposer.fetch_stock_data(ticker)
    rsi = data['rsi']
    
    # Determine motif
    if rsi < 30:
        status = "🪞 Oversold"
    elif rsi < 50:
        status = "🧘 Consolidating"
    elif rsi < 70:
        status = "🧭 Trending Up"
    else:
        status = "🔥 Overbought"
    
    print(f"{ticker:6} ${data['price']:7.2f} | RSI {rsi:5.1f} | {status}")
    
    if data['days_to_earnings'] and data['days_to_earnings'] < 7:
        print(f"       ⚠️  Earnings in {data['days_to_earnings']} days!")
```

### Find Best Setup
```python
from caption_composer import CaptionComposer

tickers = ["AAPL", "NVDA", "TSLA", "MSFT", "GOOGL"]

best = None
best_score = 0

for ticker in tickers:
    data = CaptionComposer.fetch_stock_data(ticker)
    
    if not data['entry_point']:
        continue
    
    # Score: upside potential with RSI bonus
    rsi_bonus = 1.5 if 30 <= data['rsi'] <= 60 else 1.0
    score = data['upside_potential'] * rsi_bonus
    
    if score > best_score:
        best_score = score
        best = (ticker, data)

if best:
    ticker, data = best
    print(f"🏆 Best Setup: {ticker}")
    print(f"   Entry: ${data['entry_point']}")
    print(f"   Target: ${data['exit_point']}")
    print(f"   Upside: {data['upside_potential']}%")
```

### Trade Journal Entry
```python
from caption_composer import generate_from_ticker
import datetime

def log_trade(ticker, action="ENTRY"):
    result = generate_from_ticker(ticker)
    
    print(f"\n{'='*60}")
    print(f"Trade Journal - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"{'='*60}")
    print(f"Ticker: {result['ticker']}")
    print(f"Action: {action}")
    print(f"Price: ${result['price']}")
    print(f"RSI: {result['rsi']}")
    print(f"\n{result['emoji']} {result['motif']}")
    print(f'"{result["caption_echo"]}"')
    print(f"{'='*60}\n")

# Usage
log_trade("NVDA", "ENTRY")
```

## Integration Examples

### Discord Bot
```python
import discord
from caption_composer import generate_from_ticker

@bot.command()
async def analyze(ctx, ticker: str):
    result = generate_from_ticker(ticker.upper())
    
    embed = discord.Embed(
        title=f"📊 {result['ticker']} Analysis",
        color=0x00ff00
    )
    embed.add_field(name="Price", value=f"${result['price']}")
    embed.add_field(name="RSI", value=result['rsi'])
    embed.add_field(name="Motif", value=f"{result['emoji']} {result['motif']}")
    embed.add_field(
        name="Poetic Echo",
        value=f'"{result["caption_echo"]}"',
        inline=False
    )
    
    await ctx.send(embed=embed)
```

### Slack Notification
```python
import requests
from caption_composer import generate_from_ticker

def send_slack_alert(ticker, webhook_url):
    result = generate_from_ticker(ticker)
    
    message = {
        "text": f"🎯 *{result['ticker']}* - ${result['price']}",
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*{result['emoji']} {result['motif']}*\n_{result['caption_echo']}_"
                }
            },
            {
                "type": "section",
                "fields": [
                    {"type": "mrkdwn", "text": f"*RSI:* {result['rsi']}"},
                    {"type": "mrkdwn", "text": f"*Entry:* ${result['entry_point']}"}
                ]
            }
        ]
    }
    
    requests.post(webhook_url, json=message)
```

## Tips & Best Practices

1. **Respect Rate Limits**: Don't hammer the API
2. **Cache Results**: Store data locally for repeated access
3. **Error Handling**: Always wrap in try/except for production use
4. **Combine Signals**: Use RSI with other indicators
5. **Risk Management**: Never risk more than 1-2% per trade
6. **Earnings**: Avoid trading 1-2 days before earnings
7. **Verify Tickers**: Always check ticker symbol is correct
8. **Update Regularly**: Run analysis daily, not every minute

## Performance Notes

- **Speed**: ~2-3 seconds per ticker (includes API call)
- **Batch Processing**: Process tickers sequentially, not parallel (respect API)
- **Caching**: Consider caching results for 5-15 minutes
- **Data Freshness**: Yahoo Finance updates every 15 minutes during market hours

## Keyboard Shortcuts (Interactive Mode)

- `Ctrl+C` - Exit ceremony gracefully
- `y` / `yes` - Analyze another ticker
- `n` / `no` - Exit after analysis

---

**Need help?** Run `python caption_composer.py` and follow the prompts!
