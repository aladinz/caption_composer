"""
Test the enhanced market outlook feature
"""

from caption_composer import CaptionComposer, generate_from_ticker

print("=" * 80)
print("🔮 Enhanced Market Outlook - Demo")
print("=" * 80)
print()

# Test with different market conditions
test_tickers = ["NVDA", "AAPL", "TSLA"]

for ticker in test_tickers:
    print(f"\n{'═' * 80}")
    print(f"Analyzing {ticker}...")
    print('═' * 80)
    
    # Fetch data
    stock_data = CaptionComposer.fetch_stock_data(ticker)
    rsi = stock_data['rsi']
    
    # Get market outlook
    outlook = CaptionComposer.analyze_market_outlook(stock_data, rsi)
    
    # Get forecast tone
    tone = CaptionComposer.generate_forecast_tone(rsi, ticker, stock_data)
    
    # Display
    print(f"\n📊 {ticker} - ${stock_data['price']} | RSI: {rsi}")
    print()
    print("🔮 MARKET OUTLOOK:")
    print(f"   Sentiment:       {outlook['overall_sentiment']}")
    print(f"   Trend:           {outlook['trend_emoji']} {outlook['trend']}")
    print(f"   Analyst View:    {outlook['analyst_sentiment']}")
    print(f"   RSI Signal:      {outlook['rsi_sentiment']}")
    print(f"   Action:          {outlook['action']}")
    print()
    print(f"📝 Outlook: {outlook['outlook']}")
    print()
    print(f"🎭 Forecast Tone: \"{tone}\"")
    
    if outlook['earnings_warning']:
        print(f"\n⚠️  {outlook['earnings_warning']}")
    
    # Price vs target
    if outlook['price_vs_target']:
        direction = "above" if outlook['price_vs_target'] < 0 else "below"
        print(f"\n💰 Price is {abs(outlook['price_vs_target']):.1f}% {direction} analyst target")

print("\n" + "=" * 80)
print("✨ Enhanced outlook provides deeper strategic insight! ✨")
print("=" * 80)
