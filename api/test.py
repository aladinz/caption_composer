"""
Simple diagnostic endpoint to test yfinance on Vercel
"""

from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # Test yfinance import
            import yfinance as yf
            import pandas as pd
            
            # Try to fetch AAPL quickly
            stock = yf.Ticker("AAPL")
            hist = stock.history(period="1d")
            
            if hist.empty:
                result = {
                    "status": "yfinance installed but no data",
                    "empty": True
                }
            else:
                result = {
                    "status": "SUCCESS",
                    "yfinance_version": yf.__version__,
                    "pandas_version": pd.__version__,
                    "aapl_price": float(hist['Close'].iloc[-1]),
                    "data_shape": str(hist.shape)
                }
        except ImportError as e:
            result = {
                "status": "ImportError",
                "error": str(e)
            }
        except Exception as e:
            result = {
                "status": "Error",
                "error": str(e),
                "type": type(e).__name__
            }
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(result, indent=2).encode())
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
