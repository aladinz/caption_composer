// ===========================
// TradeGPT-Aladdin Script
// Caption Composer Interface
// DYNAMIC VERSION - Fetches real-time data from Flask API
// ===========================

// === Configuration ===
// Use relative URL for API - works in both local and production
const API_BASE_URL = window.location.hostname === 'localhost' 
    ? 'http://localhost:5000' 
    : '';  // Empty string for production (same origin)
const API_TIMEOUT = 30000; // 30 seconds timeout for API calls

// === Helper Functions ===

function formatPrice(price) {
    return '$' + price.toFixed(2);
}

function getSentimentClass(sentiment) {
    if (sentiment.includes('Bullish')) return 'bullish';
    if (sentiment.includes('Bearish')) return 'bearish';
    if (sentiment.includes('Conflicting')) return 'conflicting';
    return 'neutral';
}

// === Main Composition Function ===

async function composeCaption(ticker) {
    try {
        // Call API endpoint - uses query parameter format for Vercel
        const apiUrl = window.location.hostname === 'localhost' 
            ? `http://localhost:5000/api/caption/${ticker}`
            : `/api/caption?ticker=${ticker}`;
            
        const response = await fetch(apiUrl, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            },
            signal: AbortSignal.timeout(API_TIMEOUT)
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || `Failed to fetch data for ${ticker}`);
        }
        
        const data = await response.json();
        
        // Return the data (already formatted by API)
        return data;
        
    } catch (error) {
        if (error.name === 'TimeoutError') {
            throw new Error(`Request timed out. The server took too long to respond for ${ticker}.`);
        } else if (error.name === 'TypeError' && error.message.includes('fetch')) {
            throw new Error(`Cannot connect to server. Make sure API is available.`);
        } else {
            throw error;
        }
    }
}

// === UI Rendering Functions ===

function hideAllSections() {
    document.getElementById('loadingIndicator').style.display = 'none';
    document.getElementById('outputSection').style.display = 'none';
}

function showLoading() {
    hideAllSections();
    document.getElementById('loadingIndicator').style.display = 'block';
}

function showOutput() {
    hideAllSections();
    document.getElementById('outputSection').style.display = 'block';
}

function renderOutput(result) {
    // Card Header
    document.getElementById('outputTicker').textContent = result.ticker;
    document.getElementById('outputPrice').textContent = formatPrice(result.price);
    
    const sentimentBadge = document.getElementById('sentimentBadge');
    document.getElementById('sentimentText').textContent = result.sentiment;
    sentimentBadge.className = `sentiment-badge ${getSentimentClass(result.sentiment)}`;
    
    // Motif Card
    document.getElementById('motifEmoji').textContent = result.motif.emoji;
    document.getElementById('motifName').textContent = result.motif.name;
    document.getElementById('motifArchetype').textContent = result.motif.archetype;
    document.getElementById('rsiValue').textContent = result.rsi.toFixed(1);
    document.getElementById('rsiIndicator').style.width = result.rsi + '%';
    
    // Outlook Card
    document.getElementById('trendEmoji').textContent = result.trendPhase.emoji;
    document.getElementById('trendName').textContent = result.trendPhase.name;
    document.getElementById('analystView').textContent = result.analystView || result.consensus;
    document.getElementById('recommendedAction').textContent = result.recommendedAction || 'Monitor patiently';
    
    // Levels Card
    document.getElementById('entryLevel').textContent = formatPrice(result.entry);
    document.getElementById('exitLevel').textContent = formatPrice(result.exit);
    document.getElementById('stopLevel').textContent = formatPrice(result.stop);
    document.getElementById('upsideValue').textContent = '+' + result.upside.toFixed(2) + '%';
    
    // Earnings Card - Show it if we have earnings date
    const earningsCard = document.getElementById('earningsCard');
    const earningsAlert = document.getElementById('earningsAlert');
    
    // Show earnings card if we have a valid date (even if days calculation is missing)
    if (result.earningsDate && result.earningsDate !== 'N/A') {
        earningsCard.style.display = 'block';
        
        let daysText, alertClass;
        const days = result.daysUntilEarnings;
        
        // Handle case where days might be null/undefined
        if (days === null || days === undefined) {
            daysText = 'soon';
            alertClass = 'earnings-upcoming';
        } else if (days === 0) {
            daysText = 'Today!';
            alertClass = 'earnings-today';
        } else if (days < 0) {
            daysText = Math.abs(days) === 1 ? '1 day ago' : `${Math.abs(days)} days ago`;
            alertClass = 'earnings-passed';
        } else if (days === 1) {
            daysText = 'Tomorrow';
            alertClass = 'earnings-soon';
        } else if (days <= 7) {
            daysText = `${days} days`;
            alertClass = 'earnings-soon';
        } else if (days <= 30) {
            daysText = `${days} days`;
            alertClass = 'earnings-upcoming';
        } else {
            daysText = `${days} days`;
            alertClass = 'earnings-distant';
        }
        
        document.getElementById('earningsMessage').textContent = `Earnings in ${daysText}`;
        document.getElementById('earningsDate').textContent = result.earningsDate;
        
        // Update alert styling based on proximity
        earningsAlert.className = `earnings-alert ${alertClass}`;
    } else {
        // Hide earnings card only if no date available at all
        earningsCard.style.display = 'none';
    }
    
    // AI Insights Card - Populate with intelligent recommendations
    if (result.aiInsights) {
        const insights = result.aiInsights;
        document.getElementById('aiRecommendation').textContent = insights.recommendation;
        document.getElementById('aiConfidenceLevel').style.width = insights.confidence + '%';
        document.getElementById('aiConfidenceText').textContent = insights.confidence + '%';
        document.getElementById('aiReasoning').textContent = insights.reasoning;
        
        // Color-code recommendation
        const recommendationEl = document.getElementById('aiRecommendation');
        if (insights.recommendation.includes('Strong Buy') || insights.recommendation.includes('Buy')) {
            recommendationEl.style.color = '#10b981';
        } else if (insights.recommendation.includes('Strong Sell') || insights.recommendation.includes('Sell')) {
            recommendationEl.style.color = '#ef4444';
        } else if (insights.recommendation.includes('Hold')) {
            recommendationEl.style.color = '#fbbf24';
        } else {
            recommendationEl.style.color = '#93c5fd';
        }
    }
    
    // Forecast Section
    document.getElementById('forecastToneDisplay').textContent = `"${result.forecastTone}"`;
    
    // Caption Section
    document.getElementById('captionEcho').textContent = `"${result.caption}"`;
}

// === Event Handlers ===

async function handleCompose() {
    const tickerInput = document.getElementById('tickerInput');
    const ticker = tickerInput.value.trim().toUpperCase();
    
    if (!ticker) {
        alert('Please enter a ticker symbol');
        return;
    }
    
    showLoading();
    
    try {
        // Fetch real-time data from Flask API
        const result = await composeCaption(ticker);
        renderOutput(result);
        showOutput();
    } catch (error) {
        console.error('Error fetching caption:', error);
        alert(error.message);
        hideAllSections();
    }
}

function handleKeyPress(event) {
    if (event.key === 'Enter') {
        handleCompose();
    }
}

// === Initialization ===

document.addEventListener('DOMContentLoaded', () => {
    // Bind event listeners
    document.getElementById('composeBtn').addEventListener('click', handleCompose);
    document.getElementById('tickerInput').addEventListener('keypress', handleKeyPress);
    
    // Hide output sections initially
    hideAllSections();
    
    // Focus on input
    document.getElementById('tickerInput').focus();
    
    console.log('🪔 TradeGPT-Aladdin initialized (Dynamic Mode)');
    console.log('🌐 API Server:', API_BASE_URL);
    console.log('💡 Enter any valid ticker symbol to fetch real-time data');
});
