"""Quick test to verify all features are working"""

from caption_composer import CaptionComposer, generate_from_ticker

print("🧪 Testing Caption Composer Features...\n")

# Test 1: Data fetching
print("1️⃣  Testing data fetch...")
data = CaptionComposer.fetch_stock_data('AAPL')
assert data is not None
assert 'price' in data
assert 'rsi' in data
assert 'consensus_rating' in data
assert 'target_price' in data
assert 'entry_point' in data
assert 'days_to_earnings' in data
print(f"   ✅ Fetched data for AAPL: ${data['price']} | RSI: {data['rsi']}")

# Test 2: Caption generation
print("\n2️⃣  Testing caption generation...")
result = generate_from_ticker('NVDA')
assert 'caption_echo' in result
assert 'motif' in result
assert 'emoji' in result
print(f"   ✅ Generated caption: {result['emoji']} {result['motif']}")

# Test 3: Entry/exit calculation
print("\n3️⃣  Testing entry/exit calculations...")
assert data['entry_point'] is not None or data['rsi'] > 70
if data['entry_point']:
    print(f"   ✅ Entry: ${data['entry_point']} | Exit: ${data['exit_point']}")
else:
    print(f"   ✅ Wait signal (RSI: {data['rsi']})")

# Test 4: Analyst data
print("\n4️⃣  Testing analyst data...")
assert data['consensus_rating'] is not None
print(f"   ✅ Rating: {data['consensus_rating']} | Target: ${data['target_price']}")

print("\n🎉 All tests passed! Caption Composer is fully operational.")
print("\n✨ May your trades be guided by wisdom, not whim. ✨")
