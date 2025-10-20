"""
Example usage of Caption Composer with comprehensive trading intelligence.

This demonstrates how to integrate Caption Composer into your own trading tools.
"""

from caption_composer import generate_from_ticker, CaptionComposer

def analyze_portfolio(tickers):
    """Analyze a portfolio of stocks and generate trading intelligence."""
    print("=" * 80)
    print("📊 Portfolio Trading Intelligence Report")
    print("=" * 80)
    print()
    
    for ticker in tickers:
        print(f"\n{'─' * 80}")
        print(f"Analyzing {ticker}...")
        print('─' * 80)
        
        try:
            # Fetch comprehensive data
            stock_data = CaptionComposer.fetch_stock_data(ticker)
            
            if not stock_data:
                print(f"❌ Could not fetch data for {ticker}")
                continue
            
            # Generate poetic caption
            result = generate_from_ticker(ticker)
            
            # Get market outlook
            outlook = CaptionComposer.analyze_market_outlook(stock_data, stock_data['rsi'])
            
            # Display summary
            print(f"\n🎯 {result['ticker']} - ${stock_data['price']}")
            print(f"{result['emoji']} {result['motif']}: \"{result['caption_echo']}\"")
            print()
            
            # Market outlook
            print("🔮 Market Outlook:")
            print(f"   Sentiment: {outlook['overall_sentiment']}")
            print(f"   Trend: {outlook['trend_emoji']} {outlook['trend']}")
            print(f"   Action: {outlook['action']}")
            print(f"   {outlook['outlook']}")
            print()
            
            # Market intelligence
            print("📈 Market Intelligence:")
            print(f"   RSI: {stock_data['rsi']} ({result['motif']} zone)")
            
            if stock_data['consensus_rating'] != 'N/A':
                rating = stock_data['consensus_rating'].upper().replace('_', ' ')
                print(f"   Analyst Rating: {rating}")
                
                if stock_data['target_price']:
                    current = stock_data['price']
                    target = stock_data['target_price']
                    upside = ((target - current) / current * 100)
                    print(f"   Price Target: ${target} ({upside:+.1f}% from current)")
            
            # Earnings
            if stock_data['days_to_earnings'] is not None and stock_data['days_to_earnings'] >= 0:
                print(f"   Next Earnings: {stock_data['earnings_date']} ({stock_data['days_to_earnings']} days)")
            
            # Trading levels
            print()
            print("🎲 Strategic Trading Levels:")
            if stock_data['entry_point']:
                entry = stock_data['entry_point']
                exit_target = stock_data['exit_point']
                stop = stock_data['stop_loss']
                upside = stock_data['upside_potential']
                
                print(f"   Entry Point: ${entry}")
                print(f"   Exit Target: ${exit_target}")
                print(f"   Stop Loss: ${stop}")
                print(f"   Risk/Reward: {upside:.1f}% upside potential")
                
                # Calculate risk
                risk = ((entry - stop) / entry * 100)
                reward_risk = upside / risk if risk > 0 else 0
                print(f"   Reward-to-Risk Ratio: {reward_risk:.2f}:1")
            else:
                print("   ⚠️  Wait for pullback (RSI overbought)")
            
        except Exception as e:
            print(f"❌ Error analyzing {ticker}: {e}")
    
    print("\n" + "=" * 80)
    print("✨ May your trades be guided by wisdom, not whim. ✨")
    print("=" * 80)


def find_best_opportunity(tickers):
    """Find the ticker with the best risk/reward opportunity."""
    print("\n" + "=" * 80)
    print("🔍 Finding Best Trading Opportunity...")
    print("=" * 80)
    print()
    
    best_ticker = None
    best_score = 0
    opportunities = []
    
    for ticker in tickers:
        try:
            stock_data = CaptionComposer.fetch_stock_data(ticker)
            if not stock_data or not stock_data['entry_point']:
                continue
            
            # Get market outlook
            outlook = CaptionComposer.analyze_market_outlook(stock_data, stock_data['rsi'])
            
            # Score based on multiple factors
            rsi = stock_data['rsi']
            upside = stock_data['upside_potential']
            
            # Prefer bullish alignment and optimal RSI zones
            sentiment_score = 1.5 if "Bullish" in outlook['overall_sentiment'] else 0.8
            rsi_score = 1.3 if 30 <= rsi <= 60 else 0.9 if rsi < 70 else 0.5
            
            # Weight upside potential
            total_score = upside * sentiment_score * rsi_score
            
            opportunities.append({
                'ticker': ticker,
                'score': total_score,
                'upside': upside,
                'rsi': rsi,
                'data': stock_data,
                'outlook': outlook
            })
            
        except:
            continue
    
    # Sort by score
    opportunities.sort(key=lambda x: x['score'], reverse=True)
    
    if opportunities:
        best = opportunities[0]
        result = generate_from_ticker(best['ticker'])
        
        print(f"🏆 Best Opportunity: {best['ticker']}")
        print(f"{result['emoji']} {result['motif']}: \"{result['caption_echo']}\"")
        print()
        print(f"📊 Intelligence Score: {best['score']:.2f}")
        print(f"   {best['outlook']['overall_sentiment']} | {best['outlook']['trend_emoji']} {best['outlook']['trend']}")
        print(f"   → {best['outlook']['action']}")
        print()
        print(f"💰 Financials:")
        print(f"   RSI: {best['rsi']} (optimal zone)")
        print(f"   Upside Potential: {best['upside']}%")
        print(f"   Entry: ${best['data']['entry_point']}")
        print(f"   Exit: ${best['data']['exit_point']}")
        print(f"   Stop: ${best['data']['stop_loss']}")
        
        if best['data']['target_price']:
            print(f"   Analyst Target: ${best['data']['target_price']}")
        
        if best['outlook']['earnings_warning']:
            print(f"\n   {best['outlook']['earnings_warning']}")
    else:
        print("⚠️  No clear opportunities found in this list.")
    
    print()


if __name__ == "__main__":
    # Example portfolio
    my_portfolio = ["AAPL", "NVDA", "TSLA", "MSFT"]
    
    # Analyze all tickers
    analyze_portfolio(my_portfolio)
    
    # Find best opportunity
    find_best_opportunity(my_portfolio)
