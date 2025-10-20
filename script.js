// Caption Composer - Web Interface JavaScript

// Get DOM elements
const tickerInput = document.getElementById('tickerInput');
const analyzeBtn = document.getElementById('analyzeBtn');
const loading = document.getElementById('loading');
const error = document.getElementById('error');
const errorMessage = document.getElementById('errorMessage');
const results = document.getElementById('results');

// Add event listeners
analyzeBtn.addEventListener('click', analyzeTicker);
tickerInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        analyzeTicker();
    }
});

// Main function to analyze ticker
async function analyzeTicker() {
    const ticker = tickerInput.value.trim().toUpperCase();
    
    // Validate input
    if (!ticker) {
        showError('Please enter a ticker symbol');
        return;
    }
    
    if (ticker.length > 10) {
        showError('Ticker symbol too long (max 10 characters)');
        return;
    }
    
    // Show loading, hide error and results
    loading.classList.remove('hidden');
    error.classList.add('hidden');
    results.classList.add('hidden');
    
    try {
        // Fetch data from API
        const response = await fetch(`/api/caption/${ticker}`);
        const data = await response.json();
        
        // Hide loading
        loading.classList.add('hidden');
        
        // Check for errors
        if (!response.ok || data.error) {
            showError(data.message || 'Failed to fetch data');
            return;
        }
        
        // Display results
        displayResults(data);
        
    } catch (err) {
        loading.classList.add('hidden');
        showError('Network error. Please check your connection and try again.');
        console.error('Error:', err);
    }
}

// Display results
function displayResults(data) {
    // Market Data
    document.getElementById('ticker').textContent = data.ticker || 'N/A';
    document.getElementById('price').textContent = formatPrice(data.price);
    document.getElementById('rsi').textContent = formatNumber(data.rsi);
    document.getElementById('motif').textContent = `${data.emoji} ${data.motif} (${data.archetype})`;
    
    // Analyst Consensus
    const rating = document.getElementById('rating');
    rating.textContent = formatRating(data.consensus_rating);
    rating.className = 'value rating ' + (data.consensus_rating || 'hold').toLowerCase().replace(' ', '_');
    
    document.getElementById('target').textContent = formatPriceTarget(data.price, data.target_price);
    document.getElementById('numAnalysts').textContent = data.num_analysts || '0';
    
    // Earnings Calendar
    document.getElementById('earningsDate').textContent = data.earnings_date || 'Not available';
    document.getElementById('daysToEarnings').textContent = 
        data.days_to_earnings !== null && data.days_to_earnings !== undefined 
        ? `${data.days_to_earnings} days` 
        : 'N/A';
    
    // Strategic Levels
    document.getElementById('entry').textContent = formatPrice(data.entry_point);
    document.getElementById('exit').textContent = formatPrice(data.exit_point);
    document.getElementById('stop').textContent = formatPrice(data.stop_loss);
    document.getElementById('upside').textContent = formatPercent(data.upside_potential);
    
    // Market Outlook
    document.getElementById('sentiment').textContent = data.sentiment || 'N/A';
    document.getElementById('trend').textContent = data.trend || 'N/A';
    document.getElementById('action').textContent = data.recommended_action || 'N/A';
    document.getElementById('outlook').textContent = data.outlook_description || 'N/A';
    document.getElementById('forecastTone').textContent = data.forecast_tone || 'N/A';
    
    // Poetic Caption
    document.getElementById('captionEmoji').textContent = data.emoji || '🎭';
    document.getElementById('caption').textContent = data.caption_echo || 'No caption available';
    
    // Show results
    results.classList.remove('hidden');
    
    // Scroll to results
    results.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// Show error message
function showError(message) {
    errorMessage.textContent = message;
    error.classList.remove('hidden');
    results.classList.add('hidden');
}

// Formatting functions
function formatPrice(price) {
    if (price === null || price === undefined || isNaN(price)) {
        return 'N/A';
    }
    return '$' + parseFloat(price).toFixed(2);
}

function formatPriceTarget(currentPrice, targetPrice) {
    if (targetPrice === null || targetPrice === undefined || isNaN(targetPrice)) {
        return 'N/A';
    }
    
    const target = parseFloat(targetPrice);
    const current = parseFloat(currentPrice);
    
    if (isNaN(current) || current === 0) {
        return '$' + target.toFixed(2);
    }
    
    const change = ((target - current) / current) * 100;
    const sign = change >= 0 ? '+' : '';
    
    return `$${target.toFixed(2)} (${sign}${change.toFixed(1)}%)`;
}

function formatNumber(num) {
    if (num === null || num === undefined || isNaN(num)) {
        return 'N/A';
    }
    return parseFloat(num).toFixed(2);
}

function formatPercent(num) {
    if (num === null || num === undefined || isNaN(num)) {
        return 'N/A';
    }
    return parseFloat(num).toFixed(2) + '%';
}

function formatRating(rating) {
    if (!rating) {
        return 'N/A';
    }
    
    // Convert snake_case to Title Case with spaces
    return rating
        .split('_')
        .map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
        .join(' ');
}

// Auto-focus on input when page loads
window.addEventListener('load', () => {
    tickerInput.focus();
});
