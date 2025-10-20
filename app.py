"""
Caption Composer Web Interface
Local Flask server for the trading intelligence tool
"""

from flask import Flask, jsonify, send_from_directory, request
from flask_cors import CORS
from caption_composer import generate_from_ticker
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configure Flask
app.config['JSON_SORT_KEYS'] = False

@app.route('/')
def index():
    """Serve the main HTML page"""
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    """Serve static files (CSS, JS, etc.)"""
    return send_from_directory('.', path)

@app.route('/api/caption/<ticker>')
def get_caption(ticker):
    """
    API endpoint to get trading intelligence for a ticker
    Returns comprehensive market data, analyst ratings, and poetic captions
    """
    try:
        # Validate ticker
        if not ticker or len(ticker) > 10:
            return jsonify({
                'error': 'Invalid ticker symbol',
                'message': 'Please provide a valid ticker symbol (1-10 characters)'
            }), 400
        
        # Generate caption and intelligence
        result = generate_from_ticker(ticker.upper())
        
        # Return full result
        return jsonify(result)
    
    except Exception as e:
        return jsonify({
            'error': 'Failed to fetch data',
            'message': str(e),
            'ticker': ticker.upper()
        }), 500

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Caption Composer API',
        'version': '2.1'
    })

if __name__ == '__main__':
    print("\n" + "="*80)
    print("🪔 TradeGPT-Aladdin Web Interface")
    print("="*80)
    print("\n📊 Serving live market data with poetic intelligence")
    print("🌐 Access at: http://localhost:5000")
    print("💡 API Endpoint: http://localhost:5000/api/caption/<TICKER>")
    print("\nPress Ctrl+C to stop the server\n")
    
    # Run the Flask app
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
        use_reloader=True
    )
