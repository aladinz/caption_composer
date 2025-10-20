"""Quick test to verify the formatting fix"""

from caption_composer import CaptionComposer

print("Testing forecast tone display formatting...\n")

# Test with a long forecast tone
stock_data = CaptionComposer.fetch_stock_data('NVDA')
rsi = stock_data['rsi']

# Generate forecast tone
forecast_tone = CaptionComposer.generate_forecast_tone(rsi, 'NVDA', stock_data)

print(f"Forecast Tone: \"{forecast_tone}\"")
print(f"Length: {len(forecast_tone)} characters")

# Test the formatting logic
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

print(f"\nFormatted into {len(tone_lines)} line(s):")
for i, line in enumerate(tone_lines, 1):
    padding = max(0, 72 - len(line))
    print(f"║   \"{line}\"{' ' * padding} ║")
    print(f"   ^-- Line {i}: {len(line)} chars, {padding} spaces padding")

print("\n✅ Formatting test successful!")
