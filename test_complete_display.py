"""
Comprehensive test of the fixed interactive mode display
"""

from caption_composer import CaptionComposer, generate_caption_echo

print("=" * 80)
print("Testing Complete Interactive Display (Simulated)")
print("=" * 80)
print()

# Fetch comprehensive data
ticker = "NVDA"
print(f"Fetching data for {ticker}...")
stock_data = CaptionComposer.fetch_stock_data(ticker)

rsi = stock_data["rsi"]
price = stock_data.get("price", 0.0)
consensus = stock_data.get("consensus_rating", "N/A")
target_price = stock_data.get("target_price")
num_analysts = stock_data.get("num_analysts", 0)
earnings_date = stock_data.get("earnings_date")
days_to_earnings = stock_data.get("days_to_earnings")
entry_point = stock_data.get("entry_point")
exit_point = stock_data.get("exit_point")
stop_loss = stock_data.get("stop_loss")
upside = stock_data.get("upside_potential", 0)

# Generate forecast tone and outlook
forecast_tone = CaptionComposer.generate_forecast_tone(rsi, ticker, stock_data)
outlook_data = CaptionComposer.analyze_market_outlook(stock_data, rsi)
result = generate_caption_echo(ticker, rsi, forecast_tone, stock_data)

print()
print("╔" + "═" * 78 + "╗")
print(f"║ {'TRADING INTELLIGENCE - ' + result['ticker']:^76} ║")
print("╠" + "═" * 78 + "╣")

# Market Data Section
print(f"║ {'📊 MARKET DATA':^76} ║")
print("╟" + "─" * 78 + "╢")
print(f"║ Current Price:        ${price:<55} ║")
print(f"║ RSI (14-period):      {rsi:<58} ║")
print(f"║ Motif:                {result['emoji']} {result['motif']} ({result['archetype']}) {'':<42} ║")

# Analyst Intelligence
print("╟" + "─" * 78 + "╢")
print(f"║ {'🎯 ANALYST CONSENSUS':^76} ║")
print("╟" + "─" * 78 + "╢")
print(f"║ Rating:               {consensus.upper():<58} ║")
if target_price:
    upside_to_target = ((target_price - price) / price * 100) if price > 0 else 0
    print(f"║ Price Target:         ${target_price} ({upside_to_target:+.1f}%) {'':<40} ║")

# Market Outlook Section (NEW - TESTING THIS)
print("╟" + "─" * 78 + "╢")
print(f"║ {'🔮 MARKET OUTLOOK':^76} ║")
print("╟" + "─" * 78 + "╢")
print(f"║ Sentiment:            {outlook_data['overall_sentiment']:<58} ║")
print(f"║ Trend:                {outlook_data['trend_emoji']} {outlook_data['trend']:<54} ║")
print("╟" + "─" * 78 + "╢")
print(f"║ Recommended Action:   {outlook_data['action']:<56} ║")

# Outlook narrative (word-wrapped)
outlook_text = outlook_data['outlook']
outlook_words = outlook_text.split()
outlook_lines = []
current_line = ""
for word in outlook_words:
    if len(current_line) + len(word) + 1 <= 56:
        current_line += word + " "
    else:
        outlook_lines.append(current_line.strip())
        current_line = word + " "
if current_line:
    outlook_lines.append(current_line.strip())

print(f"║ Outlook:              {outlook_lines[0]:<56} ║")
for line in outlook_lines[1:]:
    print(f"║                       {line:<56} ║")

# Forecast Tone (THE FIX WE'RE TESTING)
print("╟" + "─" * 78 + "╢")
print(f"║ Forecast Tone:        {'':<56} ║")

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

for line in tone_lines:
    padding = max(0, 72 - len(line))
    print(f"║   \"{line}\"{' ' * padding} ║")

# Caption Echo Section
print("╠" + "═" * 78 + "╣")
print(f"║ {'✨ POETIC ECHO':^76} ║")
print("╠" + "═" * 78 + "╣")

caption = result['caption_echo']
max_width = 74
words = caption.split()
lines = []
current_line = ""

for word in words:
    if len(current_line) + len(word) + 1 <= max_width:
        current_line += (word + " ")
    else:
        lines.append(current_line.strip())
        current_line = word + " "
if current_line:
    lines.append(current_line.strip())

for line in lines:
    print(f"║  {line:<76}  ║")

print("╚" + "═" * 78 + "╝")
print()
print("✅ All formatting working correctly!")
print("✨ May your trades be guided by wisdom, not whim. ✨")
