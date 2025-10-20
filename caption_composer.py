"""
Caption Composer - Poetic Echo Generator for TradeGPT-Aladdin

A ceremonial module that transforms trading signals into poetic caption echoes,
weaving together RSI levels, forecast tones, and archetypal motifs.

Part of the TradeGPT-Aladdin mythic trading assistant.
"""

from typing import Dict, Tuple, Optional
import random
from datetime import datetime, timedelta


class CaptionComposer:
    """Generates poetic caption echoes based on trading motifs and market rhythm."""
    
    # Motif thresholds and definitions
    MOTIFS = {
        "Reflection": {"threshold": 30, "emoji": "🪞", "archetype": "observer"},
        "Patience": {"threshold": 50, "emoji": "🧘", "archetype": "seeker"},
        "Clarity": {"threshold": 70, "emoji": "🧭", "archetype": "navigator"},
        "Momentum": {"threshold": float('inf'), "emoji": "🔥", "archetype": "warrior"}
    }
    
    # Caption templates organized by motif and tone resonance
    CAPTION_TEMPLATES = {
        "Reflection": [
            "I stepped back to hear the market's whisper.",
            "I didn't enter. I listened to the silence between candles.",
            "I found strength in stillness, not in the storm.",
            "I turned away from noise to find the signal.",
            "I reflected not on loss, but on lessons waiting.",
            "I paused to let the market reveal its truth."
        ],
        "Patience": [
            "I waited not for price, but for peace.",
            "I held my ground while others chased shadows.",
            "I trusted the process, not the impulse.",
            "I planted seeds in silence, awaiting the harvest.",
            "I let time become my ally, not my adversary.",
            "I breathed through the uncertainty, anchored in discipline."
        ],
        "Clarity": [
            "I didn't chase the breakout. I became the rhythm.",
            "I entered with vision, not with validation.",
            "I saw the pattern before it became obvious.",
            "I moved with precision, guided by alignment.",
            "I trusted the signal that others couldn't see.",
            "I found my edge in strategic stillness."
        ],
        "Momentum": [
            "I entered with fire, not fear.",
            "I rode the wave that others doubted.",
            "I seized the moment when clarity met courage.",
            "I didn't predict the surge. I embodied it.",
            "I moved with conviction, powered by confluence.",
            "I became the momentum I was seeking."
        ]
    }
    
    # Tone-based caption modifiers for enhanced resonance
    TONE_RESONANCE = {
        "strategic": ["precision", "alignment", "vision", "pattern"],
        "cinematic": ["rhythm", "scene", "moment", "wave"],
        "clarity": ["signal", "truth", "vision", "pattern"],
        "momentum": ["surge", "fire", "power", "conviction"],
        "discipline": ["ground", "process", "anchor", "stillness"],
        "reflection": ["whisper", "silence", "stillness", "lesson"]
    }
    
    @staticmethod
    def fetch_stock_data(ticker: str) -> Optional[Dict]:
        """
        Fetch comprehensive stock data including price, RSI, analyst ratings,
        price targets, earnings date, and technical levels.
        
        Uses yfinance library for free, real-time stock data.
        
        Args:
            ticker: Stock ticker symbol
            
        Returns:
            Dictionary with comprehensive trading intelligence
        """
        try:
            # Try using yfinance
            import yfinance as yf
            import pandas as pd
            
            # Fetch stock data
            stock = yf.Ticker(ticker)
            hist = stock.history(period="3mo")  # Get 3 months of data for RSI calculation
            info = stock.info
            
            if hist.empty:
                print(f"⚠️  No data found for {ticker}. Using simulated data...")
                return CaptionComposer._generate_simulated_data(ticker)
            
            # Calculate RSI (14-period)
            rsi = CaptionComposer.calculate_rsi(hist['Close'], period=14)
            current_price = hist['Close'].iloc[-1]
            
            # Get analyst recommendations
            consensus_rating = info.get('recommendationKey', 'N/A')
            target_price = info.get('targetMeanPrice', None)
            num_analysts = info.get('numberOfAnalystOpinions', 0)
            
            # Get earnings date
            earnings_date = None
            days_to_earnings = None
            try:
                calendar = stock.calendar
                if calendar is not None and 'Earnings Date' in calendar:
                    earnings_dates = calendar.get('Earnings Date')
                    if earnings_dates is not None and len(earnings_dates) > 0:
                        next_earnings = earnings_dates[0]
                        if hasattr(next_earnings, 'strftime'):
                            earnings_date = next_earnings.strftime('%Y-%m-%d')
                            days_to_earnings = (next_earnings - pd.Timestamp.now()).days
            except:
                pass
            
            # Calculate support and resistance levels (simple pivot points)
            entry_exit = CaptionComposer.calculate_entry_exit_points(
                hist, current_price, rsi
            )
            
            return {
                "ticker": ticker.upper(),
                "price": round(current_price, 2),
                "rsi": round(rsi, 2),
                "consensus_rating": consensus_rating,
                "target_price": round(target_price, 2) if target_price else None,
                "num_analysts": num_analysts,
                "earnings_date": earnings_date,
                "days_to_earnings": days_to_earnings,
                "entry_point": entry_exit["entry"],
                "exit_point": entry_exit["exit"],
                "stop_loss": entry_exit["stop_loss"],
                "upside_potential": entry_exit["upside_potential"],
                "data_source": "yfinance"
            }
            
        except ImportError:
            # Fallback: yfinance not installed, use simulated data
            print("⚠️  yfinance not installed. Install with: pip install yfinance")
            print("📊 Using simulated data for demonstration...")
            return CaptionComposer._generate_simulated_data(ticker)
            
        except Exception as e:
            print(f"⚠️  Error fetching data for {ticker}: {e}")
            print("📊 Using simulated data...")
            return CaptionComposer._generate_simulated_data(ticker)
    
    @staticmethod
    def _generate_simulated_data(ticker: str) -> Dict:
        """Generate simulated data when real data is unavailable."""
        import hashlib
        hash_val = int(hashlib.md5(ticker.encode()).hexdigest(), 16)
        simulated_rsi = 20 + (hash_val % 60)  # RSI between 20-80
        simulated_price = 50 + (hash_val % 500)  # Price between 50-550
        
        return {
            "ticker": ticker.upper(),
            "price": round(simulated_price, 2),
            "rsi": round(simulated_rsi, 2),
            "consensus_rating": "hold",
            "target_price": round(simulated_price * 1.15, 2),
            "num_analysts": 10,
            "earnings_date": "N/A",
            "days_to_earnings": None,
            "entry_point": round(simulated_price * 0.98, 2),
            "exit_point": round(simulated_price * 1.10, 2),
            "stop_loss": round(simulated_price * 0.95, 2),
            "upside_potential": 15.0,
            "data_source": "simulated"
        }
    
    @staticmethod
    def calculate_entry_exit_points(hist, current_price: float, rsi: float) -> Dict:
        """
        Calculate strategic entry/exit points based on technical analysis.
        
        Uses support/resistance levels, RSI, and recent price action.
        
        Args:
            hist: Historical price data (pandas DataFrame)
            current_price: Current stock price
            rsi: Current RSI value
            
        Returns:
            Dictionary with entry, exit, and stop loss levels
        """
        import pandas as pd
        
        # Calculate recent high/low (20-day)
        recent_data = hist.tail(20)
        recent_high = recent_data['High'].max()
        recent_low = recent_data['Low'].min()
        
        # Calculate ATR for stop loss
        high_low = recent_data['High'] - recent_data['Low']
        high_close = abs(recent_data['High'] - recent_data['Close'].shift())
        low_close = abs(recent_data['Low'] - recent_data['Close'].shift())
        ranges = pd.concat([high_low, high_close, low_close], axis=1)
        atr = ranges.max(axis=1).rolling(14).mean().iloc[-1]
        
        # Calculate support/resistance pivot points
        pivot = (recent_high + recent_low + current_price) / 3
        resistance1 = (2 * pivot) - recent_low
        support1 = (2 * pivot) - recent_high
        
        # RSI-based strategy with realistic levels
        if rsi < 30:
            # Oversold - opportunity to buy the dip
            entry_point = current_price * 0.99  # Enter near current (small dip)
            exit_point = max(resistance1, current_price * 1.08)  # Target resistance or 8% gain
            stop_loss = max(support1, current_price * 0.94)  # Stop at support or 6% loss
        elif rsi < 50:
            # Neutral-bearish - wait for better entry
            entry_point = current_price * 0.97  # Enter on 3% pullback
            exit_point = max(pivot, current_price * 1.06)  # Target pivot or 6% gain
            stop_loss = max(support1, current_price * 0.93)  # Stop at support or 7% loss
        elif rsi < 70:
            # Neutral-bullish - ride the momentum
            entry_point = current_price * 1.01  # Enter with slight premium
            exit_point = max(resistance1, current_price * 1.10)  # Target resistance or 10% gain
            stop_loss = max(pivot, current_price * 0.95)  # Stop at pivot or 5% loss
        else:
            # Overbought - cautious approach
            entry_point = current_price * 0.95  # Wait for 5% pullback
            exit_point = current_price * 1.03  # Quick 3% profit target
            stop_loss = current_price * 0.92  # Tight 8% stop
        
        # Ensure logical ordering: stop < entry < exit
        if stop_loss and entry_point and stop_loss >= entry_point:
            stop_loss = entry_point * 0.93  # Ensure stop is below entry
        
        if exit_point and entry_point and exit_point <= entry_point:
            exit_point = entry_point * 1.05  # Ensure exit is above entry
        
        # Calculate upside potential
        if entry_point and exit_point:
            upside_potential = ((exit_point - entry_point) / entry_point) * 100
        else:
            upside_potential = 0
        
        return {
            "entry": round(entry_point, 2) if entry_point else None,
            "exit": round(exit_point, 2) if exit_point else None,
            "stop_loss": round(stop_loss, 2) if stop_loss else None,
            "upside_potential": round(upside_potential, 2)
        }
    
    @staticmethod
    def calculate_rsi(prices, period=14):
        """
        Calculate Relative Strength Index (RSI).
        
        Args:
            prices: Series of closing prices
            period: RSI period (default 14)
            
        Returns:
            Current RSI value
        """
        import pandas as pd
        
        # Calculate price changes
        delta = prices.diff()
        
        # Separate gains and losses
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        
        # Calculate RS and RSI
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        
        return rsi.iloc[-1]
    
    @staticmethod
    def analyze_market_outlook(stock_data: Dict, rsi: float) -> Dict:
        """
        Generate comprehensive market outlook with sentiment, trend, and strategic advice.
        
        Args:
            stock_data: Dictionary with comprehensive stock data
            rsi: Current RSI value
            
        Returns:
            Dictionary with outlook, sentiment, trend, and advice
        """
        current_price = stock_data.get('price', 0)
        target_price = stock_data.get('target_price')
        consensus = stock_data.get('consensus_rating', 'N/A')
        days_to_earnings = stock_data.get('days_to_earnings')
        upside_potential = stock_data.get('upside_potential', 0)
        
        # Determine trend direction
        if target_price and current_price > 0:
            price_vs_target = ((target_price - current_price) / current_price) * 100
        else:
            price_vs_target = 0
        
        # Analyze trend
        if rsi < 30:
            trend = "Oversold Reversal Zone"
            trend_emoji = "📉→📈"
        elif rsi < 40:
            trend = "Accumulation Phase"
            trend_emoji = "🔄"
        elif rsi < 50:
            trend = "Consolidation Range"
            trend_emoji = "↔️"
        elif rsi < 60:
            trend = "Bullish Momentum Building"
            trend_emoji = "📈"
        elif rsi < 70:
            trend = "Strong Uptrend"
            trend_emoji = "🚀"
        else:
            trend = "Overbought Territory"
            trend_emoji = "⚠️"
        
        # Determine sentiment
        if consensus in ['strong_buy', 'buy']:
            analyst_sentiment = "Bullish"
        elif consensus in ['strong_sell', 'sell']:
            analyst_sentiment = "Bearish"
        else:
            analyst_sentiment = "Neutral"
        
        # RSI sentiment
        if rsi < 35:
            rsi_sentiment = "Oversold (Contrarian Bullish)"
        elif rsi < 50:
            rsi_sentiment = "Neutral to Bearish"
        elif rsi < 65:
            rsi_sentiment = "Neutral to Bullish"
        else:
            rsi_sentiment = "Overbought (Contrarian Bearish)"
        
        # Combined sentiment
        if analyst_sentiment == "Bullish" and rsi < 60:
            overall_sentiment = "🟢 Bullish Alignment"
        elif analyst_sentiment == "Bearish" and rsi > 50:
            overall_sentiment = "🔴 Bearish Alignment"
        elif (analyst_sentiment == "Bullish" and rsi >= 70) or (analyst_sentiment == "Bearish" and rsi <= 30):
            overall_sentiment = "🟡 Conflicting Signals"
        else:
            overall_sentiment = "⚪ Neutral Watch"
        
        # Strategic outlook
        if rsi < 30 and price_vs_target > 10:
            outlook = "Compelling value opportunity at oversold levels with analyst support"
            action = "Strong Buy on weakness"
        elif rsi < 30:
            outlook = "Oversold bounce candidate, but verify fundamental catalyst"
            action = "Scale in cautiously"
        elif 30 <= rsi < 50 and price_vs_target > 15:
            outlook = "Healthy consolidation with significant upside to target"
            action = "Accumulate on dips"
        elif 30 <= rsi < 50:
            outlook = "Consolidating in neutral zone, await confirmation"
            action = "Wait for setup"
        elif 50 <= rsi < 70 and upside_potential > 8:
            outlook = "Bullish momentum with favorable risk/reward"
            action = "Enter with conviction"
        elif 50 <= rsi < 70:
            outlook = "Trending higher, consider trailing stops"
            action = "Hold or take partials"
        elif rsi >= 70 and price_vs_target < -5:
            outlook = "Overbought and above analyst targets - caution warranted"
            action = "Take profits"
        else:
            outlook = "Extended move, consider profit-taking or wait for pullback"
            action = "Reduce or wait"
        
        # Earnings catalyst warning
        earnings_warning = ""
        if days_to_earnings is not None and 0 <= days_to_earnings <= 7:
            earnings_warning = "⚠️ Earnings imminent - elevated volatility expected"
        elif days_to_earnings is not None and 8 <= days_to_earnings <= 14:
            earnings_warning = "📅 Earnings approaching - monitor closely"
        
        return {
            "outlook": outlook,
            "trend": trend,
            "trend_emoji": trend_emoji,
            "overall_sentiment": overall_sentiment,
            "analyst_sentiment": analyst_sentiment,
            "rsi_sentiment": rsi_sentiment,
            "action": action,
            "earnings_warning": earnings_warning,
            "price_vs_target": round(price_vs_target, 1) if price_vs_target else None
        }
    
    @staticmethod
    def generate_forecast_tone(rsi: float, ticker: str, stock_data: Dict = None) -> str:
        """
        Generate an enhanced poetic forecast tone based on RSI, market conditions, and outlook.
        
        Args:
            rsi: Current RSI value
            ticker: Stock ticker symbol
            stock_data: Optional comprehensive stock data for deeper analysis
            
        Returns:
            Poetic forecast tone string with strategic nuance
        """
        # Get market outlook if data available
        if stock_data:
            outlook_data = CaptionComposer.analyze_market_outlook(stock_data, rsi)
            sentiment = outlook_data['overall_sentiment']
            
            # Enhanced tones based on combined signals
            if rsi < 30:
                if "Bullish" in sentiment:
                    tones = [
                        "Deep value emerging from shadows, patience rewarded",
                        "Oversold whispers of reversal, strategic accumulation beckons",
                        "Market fear creates opportunity, silence before the surge",
                        "Contrarian clarity in capitulation, foundation for ascent"
                    ]
                else:
                    tones = [
                        "Reflective stillness with patient observation",
                        "Deep introspection meets strategic pause",
                        "Caution in oversold territory, await confirmation",
                        "Silence before clarity, patience before action"
                    ]
            elif rsi < 50:
                if "Bullish" in sentiment:
                    tones = [
                        "Strategic clarity with cinematic rhythm, momentum gathering",
                        "Balanced discipline meets bullish conviction",
                        "Patient alignment with analyst optimism, confluence building",
                        "Consolidation before expansion, spring coiling"
                    ]
                else:
                    tones = [
                        "Neutral consolidation, strategic patience required",
                        "Balanced discipline with focused observation",
                        "Patient alignment awaiting clearer catalyst",
                        "Measured caution in transitional phase"
                    ]
            elif rsi < 70:
                if "Bullish" in sentiment:
                    tones = [
                        "Clear signal alignment with precision, trend confirmed",
                        "Strategic clarity meets confident execution, ride the wave",
                        "Vision crystallizing into powerful momentum",
                        "Bullish confluence with technical strength, trust the trend"
                    ]
                else:
                    tones = [
                        "Momentum strong but mixed signals, trailing stops advised",
                        "Technical strength with fundamental caution",
                        "Rising price meets analyst skepticism, stay nimble",
                        "Clear trend but approach targets, consider scaling"
                    ]
            else:  # RSI >= 70
                if "Bearish" in sentiment or "Conflicting" in sentiment:
                    tones = [
                        "Overbought euphoria meets reality check, caution warranted",
                        "Extended rally with warning signs, profit-taking zone",
                        "Fire peaks but oxygen thins, strategic exit considered",
                        "Powerful surge approaching exhaustion, lock in gains"
                    ]
                else:
                    tones = [
                        "Momentum surge with disciplined conviction, strength on strength",
                        "Fire meets focus in perfect timing, let winners run",
                        "Powerful surge with analyst support, managed aggression",
                        "Overbought but supported, tight stops on continued strength"
                    ]
        else:
            # Fallback to simpler tones if no data available
            if rsi < 30:
                tones = [
                    "Reflective stillness with patient observation",
                    "Deep introspection meets strategic pause",
                    "Silence before clarity, patience before action"
                ]
            elif rsi < 50:
                tones = [
                    "Strategic clarity with cinematic rhythm",
                    "Balanced discipline with focused intention",
                    "Patient alignment awaiting confluence"
                ]
            elif rsi < 70:
                tones = [
                    "Clear signal alignment with precision",
                    "Strategic clarity meets confident execution",
                    "Vision crystallizing into momentum"
                ]
            else:
                tones = [
                    "Momentum surge with disciplined conviction",
                    "Fire meets focus in perfect timing",
                    "Powerful surge with strategic clarity"
                ]
        
        return random.choice(tones)
    
    @staticmethod
    def determine_motif(rsi: float) -> Tuple[str, str, str]:
        """
        Determine the archetypal motif based on RSI level.
        
        Args:
            rsi: Relative Strength Index value (0-100)
            
        Returns:
            Tuple of (motif_name, emoji, archetype)
        """
        if rsi < 30:
            motif = "Reflection"
        elif rsi < 50:
            motif = "Patience"
        elif rsi < 70:
            motif = "Clarity"
        else:
            motif = "Momentum"
        
        motif_data = CaptionComposer.MOTIFS[motif]
        return motif, motif_data["emoji"], motif_data["archetype"]
    
    @staticmethod
    def calculate_tone_resonance(forecast_tone: str, motif: str) -> float:
        """
        Calculate how well the forecast tone resonates with the motif.
        
        Args:
            forecast_tone: The tone descriptor from forecast
            motif: The determined motif name
            
        Returns:
            Resonance score (0.0 to 1.0)
        """
        tone_lower = forecast_tone.lower()
        motif_lower = motif.lower()
        
        # Base resonance if motif appears in tone
        resonance = 0.5
        
        # Check for tone keywords that align with motif
        for tone_key, keywords in CaptionComposer.TONE_RESONANCE.items():
            if tone_key in tone_lower or tone_key in motif_lower:
                for keyword in keywords:
                    if keyword in tone_lower:
                        resonance += 0.1
        
        return min(resonance, 1.0)
    
    @staticmethod
    def select_caption(motif: str, forecast_tone: str, ticker: str = None) -> str:
        """
        Select the most resonant caption echo for the given motif and tone.
        
        Args:
            motif: The archetypal motif
            forecast_tone: The forecast tone descriptor
            ticker: Optional ticker symbol for context
            
        Returns:
            Poetic caption echo string
        """
        templates = CaptionComposer.CAPTION_TEMPLATES.get(motif, [])
        
        if not templates:
            return "I moved with intention, guided by the market's song."
        
        # Calculate resonance for enhanced selection
        resonance = CaptionComposer.calculate_tone_resonance(forecast_tone, motif)
        
        # For high resonance, prefer captions that echo the tone
        if resonance > 0.7:
            # Filter for captions that contain tone keywords
            tone_lower = forecast_tone.lower()
            resonant_captions = [
                caption for caption in templates
                if any(keyword in caption.lower() for tone_keywords in CaptionComposer.TONE_RESONANCE.values() for keyword in tone_keywords if keyword in tone_lower)
            ]
            if resonant_captions:
                return random.choice(resonant_captions)
        
        # Default: select from all motif templates
        return random.choice(templates)
    
    @staticmethod
    def compose(ticker: str, rsi: float, forecast_tone: str) -> Dict[str, str]:
        """
        Generate a poetic caption echo based on ticker, RSI, and forecast tone.
        
        This is the main ceremonial function that weaves together market signals
        into a mythic narrative echo.
        
        Args:
            ticker: Stock ticker symbol (e.g., "IBIT", "AMZN")
            rsi: Relative Strength Index value (0-100)
            forecast_tone: Forecast tone descriptor (e.g., "Strategic clarity with cinematic rhythm")
            
        Returns:
            Dictionary containing:
                - motif: The archetypal motif name
                - emoji: The motif's symbolic emoji
                - archetype: The trader archetype
                - caption_echo: The poetic caption
                - ticker: The ticker symbol
                - rsi: The RSI value
                - resonance: Tone-motif resonance score
                
        Example:
            >>> result = CaptionComposer.compose("IBIT", 38.16, "Strategic clarity with cinematic rhythm")
            >>> print(f"{result['emoji']} {result['motif']}: {result['caption_echo']}")
            🧘 Patience: I waited not for price, but for peace.
        """
        # Determine the archetypal motif
        motif, emoji, archetype = CaptionComposer.determine_motif(rsi)
        
        # Select the most resonant caption
        caption_echo = CaptionComposer.select_caption(motif, forecast_tone, ticker)
        
        # Calculate resonance for metadata
        resonance = CaptionComposer.calculate_tone_resonance(forecast_tone, motif)
        
        return {
            "motif": motif,
            "emoji": emoji,
            "archetype": archetype,
            "caption_echo": caption_echo,
            "ticker": ticker.upper(),
            "rsi": round(rsi, 2),
            "resonance": round(resonance, 2)
        }


def generate_caption_echo(ticker: str, rsi: float = None, forecast_tone: str = None, stock_data: Dict = None) -> Dict[str, str]:
    """
    Convenience function for generating caption echoes.
    
    If RSI is not provided, it will be fetched automatically.
    If forecast_tone is not provided, it will be generated based on RSI and market data.
    
    Args:
        ticker: Stock ticker symbol
        rsi: Optional RSI value (will be fetched if not provided)
        forecast_tone: Optional forecast tone descriptor (will be generated if not provided)
        stock_data: Optional stock data dictionary (will be fetched if not provided)
        
    Returns:
        Dictionary with motif, emoji, and caption_echo
    """
    # If stock data not provided and we need it, fetch it
    if stock_data is None and (rsi is None or forecast_tone is None):
        stock_data = CaptionComposer.fetch_stock_data(ticker)
        if stock_data is None:
            raise ValueError(f"Could not fetch data for ticker: {ticker}")
    
    # If RSI not provided, get it from stock_data
    if rsi is None:
        if stock_data:
            rsi = stock_data["rsi"]
            print(f"📊 Fetched RSI: {rsi} for {ticker}")
        else:
            raise ValueError("RSI not provided and could not be fetched")
    
    # If forecast tone not provided, generate it with enhanced outlook
    if forecast_tone is None:
        forecast_tone = CaptionComposer.generate_forecast_tone(rsi, ticker, stock_data)
    
    return CaptionComposer.compose(ticker, rsi, forecast_tone)


def generate_from_ticker(ticker: str) -> Dict[str, str]:
    """
    Generate a complete caption echo from just a ticker symbol.
    Automatically fetches RSI and generates forecast tone.
    Returns comprehensive trading intelligence data.
    
    Args:
        ticker: Stock ticker symbol
        
    Returns:
        Dictionary with complete caption echo data and market intelligence
    """
    # Fetch comprehensive stock data
    stock_data = CaptionComposer.fetch_stock_data(ticker)
    
    if stock_data is None:
        raise ValueError(f"Could not fetch data for ticker: {ticker}")
    
    # Extract key data
    rsi = stock_data["rsi"]
    
    # Generate forecast tone with enhanced outlook
    forecast_tone = CaptionComposer.generate_forecast_tone(rsi, ticker, stock_data)
    
    # Generate market outlook analysis
    outlook_data = CaptionComposer.analyze_market_outlook(stock_data, rsi)
    
    # Generate the caption echo
    caption_result = CaptionComposer.compose(ticker, rsi, forecast_tone)
    
    # Combine all data into comprehensive result
    result = {
        # Caption data
        **caption_result,
        
        # Market data
        "price": stock_data.get("price"),
        "data_source": stock_data.get("data_source", "unknown"),
        
        # Analyst consensus
        "consensus_rating": stock_data.get("consensus_rating", "N/A"),
        "target_price": stock_data.get("target_price"),
        "num_analysts": stock_data.get("num_analysts", 0),
        
        # Earnings calendar
        "earnings_date": stock_data.get("earnings_date"),
        "days_to_earnings": stock_data.get("days_to_earnings"),
        
        # Strategic levels
        "entry_point": stock_data.get("entry_point"),
        "exit_point": stock_data.get("exit_point"),
        "stop_loss": stock_data.get("stop_loss"),
        "upside_potential": stock_data.get("upside_potential"),
        
        # Market outlook
        "sentiment": outlook_data.get("overall_sentiment"),
        "trend": outlook_data.get("trend"),
        "trend_emoji": outlook_data.get("trend_emoji"),
        "analyst_view": outlook_data.get("analyst_view"),
        "rsi_signal": outlook_data.get("rsi_signal"),
        "recommended_action": outlook_data.get("action"),
        "outlook_description": outlook_data.get("outlook"),
        "forecast_tone": forecast_tone,
        "earnings_warning": outlook_data.get("earnings_warning"),
    }
    
    return result


def interactive_mode():
    """
    Interactive ceremonial interface for generating caption echoes.
    Prompts the user for ticker symbol and automatically fetches comprehensive trading intelligence.
    """
    print("=" * 80)
    print("✨ Caption Composer - TradeGPT-Aladdin Trading Intelligence ✨")
    print("=" * 80)
    print()
    print("Welcome, Trader. Let us weave your market moment into myth.")
    print()
    
    try:
        # Get ticker symbol
        ticker = input("🎯 Enter ticker symbol (e.g., IBIT, AMZN, TSLA): ").strip().upper()
        
        if not ticker:
            print("⚠️  Ticker cannot be empty. Exiting ceremony.")
            return
        
        print()
        print("─" * 80)
        print(f"🔮 Fetching comprehensive market intelligence for {ticker}...")
        print("─" * 80)
        print()
        
        # Fetch stock data
        stock_data = CaptionComposer.fetch_stock_data(ticker)
        
        if stock_data is None:
            print(f"⚠️  Could not fetch data for {ticker}. Please check the ticker symbol.")
            return
        
        # Extract data
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
        data_source = stock_data.get("data_source", "unknown")
        
        # Generate forecast tone with enhanced outlook
        forecast_tone = CaptionComposer.generate_forecast_tone(rsi, ticker, stock_data)
        
        # Generate market outlook analysis
        outlook_data = CaptionComposer.analyze_market_outlook(stock_data, rsi)
        
        # Generate the caption echo
        result = generate_caption_echo(ticker, rsi, forecast_tone)
        
        # Display comprehensive trading intelligence
        print("╔" + "═" * 78 + "╗")
        print(f"║ {'TRADING INTELLIGENCE - ' + result['ticker']:^76} ║")
        print("╠" + "═" * 78 + "╣")
        
        # Market Data Section
        print(f"║ {'📊 MARKET DATA':^76} ║")
        print("╟" + "─" * 78 + "╢")
        if data_source != "simulated":
            print(f"║ Current Price:        ${price:<55} ║")
        else:
            print(f"║ Current Price:        ${price} (simulated) {'':<39} ║")
        print(f"║ RSI (14-period):      {rsi:<58} ║")
        print(f"║ Motif:                {result['emoji']} {result['motif']} ({result['archetype']}) {'':<42} ║")
        
        # Analyst Intelligence Section
        print("╟" + "─" * 78 + "╢")
        print(f"║ {'🎯 ANALYST CONSENSUS':^76} ║")
        print("╟" + "─" * 78 + "╢")
        consensus_display = consensus.upper() if consensus != "N/A" else "N/A"
        print(f"║ Rating:               {consensus_display:<58} ║")
        if target_price:
            upside_to_target = ((target_price - price) / price * 100) if price > 0 else 0
            print(f"║ Price Target:         ${target_price} ({upside_to_target:+.1f}%) {'':<40} ║")
        else:
            print(f"║ Price Target:         N/A{'':<56} ║")
        print(f"║ Analysts Covering:    {num_analysts:<58} ║")
        
        # Earnings Intelligence Section
        print("╟" + "─" * 78 + "╢")
        print(f"║ {'📅 EARNINGS CALENDAR':^76} ║")
        print("╟" + "─" * 78 + "╢")
        if earnings_date and earnings_date != "N/A":
            print(f"║ Next Earnings:        {earnings_date:<58} ║")
            if days_to_earnings is not None:
                if days_to_earnings < 0:
                    print(f"║ Days Until:           Earnings already reported{'':<31} ║")
                else:
                    print(f"║ Days Until:           {days_to_earnings} days{'':<54} ║")
        else:
            print(f"║ Next Earnings:        Not available{'':<46} ║")
        
        # Technical Levels Section
        print("╟" + "─" * 78 + "╢")
        print(f"║ {'🎲 RECOMMENDED LEVELS':^76} ║")
        print("╟" + "─" * 78 + "╢")
        if entry_point:
            print(f"║ Entry Point:          ${entry_point:<56} ║")
        else:
            print(f"║ Entry Point:          Wait for pullback (RSI overbought){'':<25} ║")
        if exit_point:
            print(f"║ Exit Target:          ${exit_point:<56} ║")
        if stop_loss:
            print(f"║ Stop Loss:            ${stop_loss:<56} ║")
        if upside > 0:
            print(f"║ Upside Potential:     {upside}%{'':<56} ║")
        
        # Market Outlook Section
        print("╟" + "─" * 78 + "╢")
        print(f"║ {'🔮 MARKET OUTLOOK':^76} ║")
        print("╟" + "─" * 78 + "╢")
        print(f"║ Sentiment:            {outlook_data['overall_sentiment']:<58} ║")
        print(f"║ Trend:                {outlook_data['trend_emoji']} {outlook_data['trend']:<54} ║")
        print(f"║ Analyst View:         {outlook_data['analyst_sentiment']:<58} ║")
        print(f"║ RSI Signal:           {outlook_data['rsi_sentiment']:<58} ║")
        
        # Strategic action
        print("╟" + "─" * 78 + "╢")
        action_words = outlook_data['action'].split()
        action_line = ""
        for word in action_words:
            if len(action_line) + len(word) + 1 <= 56:
                action_line += word + " "
            else:
                break
        print(f"║ Recommended Action:   {action_line.strip():<56} ║")
        
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
        
        # Earnings warning if applicable
        if outlook_data['earnings_warning']:
            print("╟" + "─" * 78 + "╢")
            print(f"║ {outlook_data['earnings_warning']:<76} ║")
        
        # Forecast Tone
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
        
        # Word wrap the caption for display
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
        
        if data_source == "simulated":
            print("⚠️  Note: Using simulated data. Install yfinance for real market data:")
            print("   pip install yfinance pandas")
            print()
        
        print("✨ May your trades be guided by wisdom, not whim. ✨")
        print()
        
        # Ask if user wants to generate another
        print()
        another = input("🔄 Analyze another ticker? (y/n): ").strip().lower()
        if another == 'y' or another == 'yes':
            print("\n" * 2)
            interactive_mode()
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Ceremony interrupted. May you find clarity in silence.")
    except Exception as e:
        print(f"\n⚠️  An error occurred: {e}")
        import traceback
        traceback.print_exc()
        print("The ceremony cannot complete. Please try again.")


def demo_mode():
    """
    Demonstration mode showing comprehensive trading intelligence with auto-fetched data.
    """
    print("=" * 80)
    print("Caption Composer - Demo Mode (Comprehensive Intelligence)")
    print("=" * 80)
    print()
    
    # Example tickers
    tickers = ["AAPL", "NVDA"]
    
    for ticker in tickers:
        try:
            print(f"🔮 Generating trading intelligence for {ticker}...")
            print()
            
            # Fetch comprehensive data
            stock_data = CaptionComposer.fetch_stock_data(ticker)
            if not stock_data:
                print(f"⚠️  Could not fetch data for {ticker}")
                print()
                continue
            
            # Generate caption
            result = generate_caption_echo(
                ticker, 
                stock_data["rsi"],
                CaptionComposer.generate_forecast_tone(stock_data["rsi"], ticker, stock_data)
            )
            
            # Generate outlook
            outlook_data = CaptionComposer.analyze_market_outlook(stock_data, stock_data["rsi"])
            
            # Display compact intelligence
            print(f"{'─' * 80}")
            print(f"🎯 {result['ticker']} - ${stock_data['price']} | RSI: {stock_data['rsi']}")
            print(f"{result['emoji']} {result['motif']}: \"{result['caption_echo']}\"")
            print()
            
            # Market outlook
            print(f"   {outlook_data['overall_sentiment']} | {outlook_data['trend_emoji']} {outlook_data['trend']}")
            print(f"   → {outlook_data['action']}")
            print()
            
            if stock_data.get('consensus_rating') != 'N/A':
                print(f"   Analyst Rating: {stock_data['consensus_rating'].upper()}", end="")
                if stock_data.get('target_price'):
                    upside = ((stock_data['target_price'] - stock_data['price']) / stock_data['price'] * 100)
                    print(f" | Target: ${stock_data['target_price']} ({upside:+.1f}%)")
                else:
                    print()
            
            if stock_data.get('days_to_earnings') is not None and stock_data.get('days_to_earnings') >= 0:
                print(f"   Next Earnings: {stock_data['earnings_date']} ({stock_data['days_to_earnings']} days)")
                if outlook_data['earnings_warning']:
                    print(f"   {outlook_data['earnings_warning']}")
            
            if stock_data.get('entry_point'):
                print(f"   Entry: ${stock_data['entry_point']} | Exit: ${stock_data['exit_point']} | Stop: ${stock_data['stop_loss']}")
                print(f"   Upside Potential: {stock_data['upside_potential']}%")
            
            print()
            
        except Exception as e:
            print(f"⚠️  Could not generate intelligence for {ticker}: {e}")
            print()
    
    print("=" * 80)
    print("May your trades be guided by wisdom, not whim.")
    print("=" * 80)


# Main entry point
if __name__ == "__main__":
    import sys
    
    # Check if demo mode is requested
    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        demo_mode()
    else:
        interactive_mode()
