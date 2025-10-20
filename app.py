"""
TradeGPT-Aladdin Flask API Server
Serves real-time caption data from caption_composer.py
"""

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from caption_composer import CaptionComposer
from datetime import datetime
import os

app = Flask(__name__, static_folder='.')
CORS(app)  # Enable CORS for local development

def calculate_days_to_earnings(earnings_date_str):
    """Calculate days until earnings from date string"""
    try:
        if earnings_date_str and earnings_date_str != 'N/A':
            earnings_date = datetime.strptime(earnings_date_str, '%Y-%m-%d')
            today = datetime.now()
            delta = (earnings_date - today).days
            return delta
    except Exception as e:
        print(f"Error calculating days to earnings: {e}")
    return None

def generate_ai_insights(stock_data, market_outlook, rsi, days_to_earnings):
    """Generate AI-powered trading insights and recommendations"""
    insights = {
        'recommendation': '',
        'confidence': 0,
        'reasoning': ''
    }
    
    # Analyze multiple factors
    sentiment = market_outlook.get('overall_sentiment', '')
    action = market_outlook.get('action', '')
    consensus = stock_data.get('consensus_rating', '')
    target_price = stock_data.get('target_price', 0)
    current_price = stock_data.get('price', 0)
    
    # Calculate upside to target
    upside_to_target = 0
    if target_price and current_price:
        upside_to_target = ((target_price - current_price) / current_price) * 100
    
    # Determine recommendation based on multiple signals
    bullish_signals = 0
    bearish_signals = 0
    
    # RSI Analysis
    if rsi < 30:
        bullish_signals += 2  # Strong oversold
        rsi_signal = "deeply oversold"
    elif rsi < 40:
        bullish_signals += 1
        rsi_signal = "oversold"
    elif rsi > 70:
        bearish_signals += 2  # Strong overbought
        rsi_signal = "overbought"
    elif rsi > 60:
        bearish_signals += 1
        rsi_signal = "elevated"
    else:
        rsi_signal = "neutral"
    
    # Sentiment Analysis
    if 'Bullish' in sentiment:
        bullish_signals += 2
    elif 'Bearish' in sentiment:
        bearish_signals += 2
    
    # Analyst Consensus
    if consensus in ['Strong Buy', 'Buy']:
        bullish_signals += 2
    elif consensus in ['Sell', 'Strong Sell']:
        bearish_signals += 2
    elif consensus == 'Hold':
        pass  # Neutral
    
    # Upside Potential
    if upside_to_target > 15:
        bullish_signals += 2
    elif upside_to_target < -10:
        bearish_signals += 2
    
    # Earnings Proximity
    if days_to_earnings is not None:
        if 0 <= days_to_earnings <= 3:
            # Very close to earnings - high volatility risk
            insights['reasoning'] = f"Earnings in {days_to_earnings} day(s) - expect high volatility. RSI is {rsi_signal}."
            insights['recommendation'] = "Wait for earnings clarity" if days_to_earnings == 0 else "Exercise caution - earnings imminent"
            insights['confidence'] = 60
            return insights
        elif days_to_earnings <= 7:
            bearish_signals += 1  # Slight caution near earnings
    
    # Calculate net signals
    net_signal = bullish_signals - bearish_signals
    
    # Generate recommendation
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

@app.route('/')
def index():
    """Serve the main HTML page"""
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def static_files(path):
    """Serve static files (CSS, JS)"""
    return send_from_directory('.', path)

@app.route('/api/caption/<ticker>', methods=['GET'])
def get_caption(ticker):
    """
    API endpoint to generate caption for a ticker
    Returns: JSON with all trading intelligence data
    """
    try:
        ticker = ticker.upper().strip()
        
        # Fetch comprehensive stock data
        stock_data = CaptionComposer.fetch_stock_data(ticker)
        
        if stock_data is None:
            return jsonify({
                'error': f'Unable to fetch data for {ticker}. Please check the ticker symbol.',
                'ticker': ticker
            }), 404
        
        # Generate enhanced market outlook
        market_outlook = CaptionComposer.analyze_market_outlook(stock_data, stock_data['rsi'])
        
        # Generate forecast tone
        forecast_tone = CaptionComposer.generate_forecast_tone(
            stock_data['rsi'], 
            ticker, 
            stock_data
        )
        
        # Generate caption echo
        caption_result = CaptionComposer.compose(
            ticker, 
            stock_data['rsi'], 
            forecast_tone
        )
        
        # Build comprehensive response
        response = {
            'ticker': ticker,
            'price': stock_data.get('price', 0),
            'rsi': stock_data.get('rsi', 50),
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
        
        return jsonify(response)
    
    except Exception as e:
        # Log the error for debugging
        print(f"Error processing {ticker}: {str(e)}")
        import traceback
        traceback.print_exc()
        
        return jsonify({
            'error': f'Error processing {ticker}: {str(e)}',
            'ticker': ticker
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'TradeGPT-Aladdin API',
        'version': '1.0.0'
    })

@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors"""
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def server_error(e):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    print("🪔 TradeGPT-Aladdin API Server Starting...")
    print("📊 Serving real-time caption data")
    print("🌐 Access at: http://localhost:5000")
    print("💡 API Endpoint: http://localhost:5000/api/caption/<TICKER>")
    print("\nPress Ctrl+C to stop the server\n")
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
        threaded=True
    )
