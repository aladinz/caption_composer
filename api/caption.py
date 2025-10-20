"""
TradeGPT-Aladdin Caption API Endpoint
Handles /api/caption requests
"""

from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# Pre-import heavy modules to reduce cold start time
try:
    import yfinance as yf
    import pandas as pd
    YFINANCE_AVAILABLE = True
except ImportError:
    YFINANCE_AVAILABLE = False

from caption_composer import CaptionComposer
from datetime import datetime

def calculate_days_to_earnings(earnings_date_str):
    """Calculate days until earnings"""
    try:
        if earnings_date_str and earnings_date_str != 'N/A':
            earnings_date = datetime.strptime(earnings_date_str, '%Y-%m-%d')
            today = datetime.now()
            return (earnings_date - today).days
    except:
        pass
    return None

def generate_ai_insights(stock_data, market_outlook, rsi, days_to_earnings):
    """Generate AI insights"""
    insights = {'recommendation': '', 'confidence': 0, 'reasoning': ''}
    
    sentiment = market_outlook.get('overall_sentiment', '')
    action = market_outlook.get('action', '')
    consensus = stock_data.get('consensus_rating', '')
    target_price = stock_data.get('target_price', 0)
    current_price = stock_data.get('price', 0)
    
    upside_to_target = 0
    if target_price and current_price:
        upside_to_target = ((target_price - current_price) / current_price) * 100
    
    bullish_signals = bearish_signals = 0
    
    if rsi < 30:
        bullish_signals += 2
        rsi_signal = "deeply oversold"
    elif rsi < 40:
        bullish_signals += 1
        rsi_signal = "oversold"
    elif rsi > 70:
        bearish_signals += 2
        rsi_signal = "overbought"
    elif rsi > 60:
        bearish_signals += 1
        rsi_signal = "elevated"
    else:
        rsi_signal = "neutral"
    
    if 'Bullish' in sentiment:
        bullish_signals += 2
    elif 'Bearish' in sentiment:
        bearish_signals += 2
    
    if consensus in ['Strong Buy', 'Buy']:
        bullish_signals += 2
    elif consensus in ['Sell', 'Strong Sell']:
        bearish_signals += 2
    
    if upside_to_target > 15:
        bullish_signals += 2
    elif upside_to_target < -10:
        bearish_signals += 2
    
    if days_to_earnings is not None and 0 <= days_to_earnings <= 3:
        insights['reasoning'] = f"Earnings in {days_to_earnings} day(s) - expect high volatility. RSI is {rsi_signal}."
        insights['recommendation'] = "Wait for earnings clarity" if days_to_earnings == 0 else "Exercise caution - earnings imminent"
        insights['confidence'] = 60
        return insights
    elif days_to_earnings and days_to_earnings <= 7:
        bearish_signals += 1
    
    net_signal = bullish_signals - bearish_signals
    
    if net_signal >= 4:
        insights['recommendation'] = "Strong Buy - Multiple bullish indicators align"
        insights['confidence'] = min(85 + (net_signal * 2), 95)
        insights['reasoning'] = f"RSI is {rsi_signal} ({rsi:.1f}), {sentiment.lower()}, with {upside_to_target:.1f}% upside to analyst target."
    elif net_signal >= 2:
        insights['recommendation'] = "Buy - Favorable risk/reward setup"
        insights['confidence'] = 70 + (net_signal * 3)
        insights['reasoning'] = f"Technical momentum ({rsi_signal} RSI) supports {action.lower()}. Analysts rate: {consensus}."
    elif net_signal <= -4:
        insights['recommendation'] = "Strong Sell - Multiple warning signals"
        insights['confidence'] = min(85 + (abs(net_signal) * 2), 95)
        insights['reasoning'] = f"RSI {rsi_signal} ({rsi:.1f}), {sentiment.lower()}. Consider reducing exposure."
    elif net_signal <= -2:
        insights['recommendation'] = "Sell - Risk outweighs reward"
        insights['confidence'] = 70 + (abs(net_signal) * 3)
        insights['reasoning'] = f"Technical weakness ({rsi_signal} RSI) suggests {action.lower()}. Analysts: {consensus}."
    else:
        insights['recommendation'] = "Hold - Mixed signals, monitor closely"
        insights['confidence'] = 50 + abs(net_signal) * 5
        insights['reasoning'] = f"RSI {rsi_signal} at {rsi:.1f}. {sentiment}. Wait for clearer direction."
    
    return insights

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # Get ticker from query string
            parsed = urlparse(self.path)
            params = parse_qs(parsed.query)
            ticker = params.get('ticker', [''])[0].upper().strip()
            
            if not ticker:
                self.send_error(400, "Missing ticker parameter")
                return
            
            # Check if yfinance is available
            if not YFINANCE_AVAILABLE:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({
                    'error': 'yfinance module not available',
                    'dataSource': 'error'
                }).encode())
                return
            
            # Fetch stock data with timeout protection
            stock_data = CaptionComposer.fetch_stock_data(ticker)
            
            if not stock_data:
                self.send_response(404)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({'error': f'Unable to fetch data for {ticker}'}).encode())
                return
            
            # Generate market outlook
            market_outlook = CaptionComposer.analyze_market_outlook(stock_data, stock_data['rsi'])
            
            # Generate forecast tone
            forecast_tone = CaptionComposer.generate_forecast_tone(stock_data['rsi'], ticker, stock_data)
            
            # Generate caption
            caption_result = CaptionComposer.compose(ticker, stock_data['rsi'], forecast_tone)
            
            # Build response
            response = {
                'ticker': ticker,
                'price': stock_data.get('price', 0),
                'rsi': stock_data.get('rsi', 50),
                'dataSource': stock_data.get('data_source', 'unknown'),
                'motif': {
                    'emoji': caption_result.get('motif_emoji', '✨'),
                    'name': caption_result.get('motif', 'Unknown'),
                    'archetype': caption_result.get('archetype', 'The Seeker'),
                    'color': '#219ebc'
                },
                'trendPhase': {
                    'emoji': market_outlook.get('trend_emoji', '📊'),
                    'name': market_outlook.get('trend', 'Unknown')
                },
                'sentiment': market_outlook.get('overall_sentiment', 'Neutral Stance'),
                'forecastTone': forecast_tone,
                'caption': caption_result.get('caption_echo', 'Wisdom awaits those who seek.'),
                'consensus': stock_data.get('consensus_rating', 'Hold'),
                'targetPrice': stock_data.get('target_price', stock_data.get('price', 0)),
                'upside': ((stock_data.get('target_price', 0) - stock_data.get('price', 0)) / stock_data.get('price', 1) * 100) if stock_data.get('target_price') and stock_data.get('price') else 0,
                'earningsDate': stock_data.get('earnings_date', 'N/A'),
                'daysUntilEarnings': stock_data.get('days_to_earnings') if stock_data.get('days_to_earnings') is not None else calculate_days_to_earnings(stock_data.get('earnings_date')),
                'entry': stock_data.get('entry_point', stock_data.get('price', 0)),
                'exit': stock_data.get('exit_point', stock_data.get('price', 0)),
                'stop': stock_data.get('stop_loss', stock_data.get('price', 0)),
                'analystView': market_outlook.get('analyst_sentiment', 'N/A'),
                'recommendedAction': market_outlook.get('action', 'Monitor'),
                'aiInsights': generate_ai_insights(
                    stock_data, 
                    market_outlook, 
                    stock_data.get('rsi', 50),
                    stock_data.get('days_to_earnings') if stock_data.get('days_to_earnings') is not None else calculate_days_to_earnings(stock_data.get('earnings_date'))
                )
            }
            
            # Send response
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            error_response = {
                'error': str(e),
                'type': type(e).__name__,
                'message': 'Internal server error while fetching stock data'
            }
            self.wfile.write(json.dumps(error_response).encode())
            self.wfile.write(json.dumps({'error': str(e)}).encode())
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
