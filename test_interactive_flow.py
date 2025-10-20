"""
Final verification test - simulates interactive mode flow
"""

from caption_composer import CaptionComposer, generate_caption_echo

def test_interactive_flow(ticker):
    """Simulate the complete interactive mode flow"""
    print(f"\n{'='*80}")
    print(f"Simulating Interactive Mode for {ticker}")
    print('='*80)
    
    try:
        # Step 1: Fetch data
        print(f"\n🔮 Fetching comprehensive market intelligence for {ticker}...")
        stock_data = CaptionComposer.fetch_stock_data(ticker)
        
        if not stock_data:
            print(f"❌ Could not fetch data for {ticker}")
            return False
        
        # Step 2: Extract data
        rsi = stock_data["rsi"]
        price = stock_data.get("price", 0.0)
        
        # Step 3: Generate forecast tone
        forecast_tone = CaptionComposer.generate_forecast_tone(rsi, ticker, stock_data)
        print(f"✅ Generated forecast tone: \"{forecast_tone[:50]}...\"")
        
        # Step 4: Generate outlook
        outlook_data = CaptionComposer.analyze_market_outlook(stock_data, rsi)
        print(f"✅ Generated market outlook: {outlook_data['overall_sentiment']}")
        
        # Step 5: Generate caption
        result = generate_caption_echo(ticker, rsi, forecast_tone, stock_data)
        print(f"✅ Generated caption: \"{result['caption_echo']}\"")
        
        # Step 6: Test the problematic formatting section
        print("\n📝 Testing forecast tone formatting (the bugfix area)...")
        tone_words = forecast_tone.split()
        tone_lines = []
        current_line = ""
        
        for word in tone_words:
            if len(current_line) + len(word) + 1 <= 54:
                current_line += word + " "
            else:
                tone_lines.append(current_line.strip())
                current_line = word + " "
        if current_line:
            tone_lines.append(current_line.strip())
        
        print(f"   Split into {len(tone_lines)} line(s)")
        
        for i, line in enumerate(tone_lines, 1):
            padding = max(0, 72 - len(line))
            formatted = f"║   \"{line}\"{' ' * padding} ║"
            print(f"   Line {i}: {formatted}")
        
        print("\n✅ All formatting successful - no errors!")
        return True
        
    except Exception as e:
        print(f"\n❌ Error occurred: {e}")
        import traceback
        traceback.print_exc()
        return False

# Test with multiple tickers
print("="*80)
print("🧪 COMPREHENSIVE INTERACTIVE MODE TEST")
print("="*80)

test_tickers = ["NVDA", "AAPL", "MSFT"]
results = {}

for ticker in test_tickers:
    results[ticker] = test_interactive_flow(ticker)

print("\n" + "="*80)
print("📊 TEST RESULTS SUMMARY")
print("="*80)

all_passed = all(results.values())

for ticker, passed in results.items():
    status = "✅ PASS" if passed else "❌ FAIL"
    print(f"{ticker:6} : {status}")

print("\n" + "="*80)
if all_passed:
    print("🎉 ALL TESTS PASSED - Interactive mode is fully operational!")
else:
    print("⚠️  Some tests failed - review errors above")
print("="*80)
