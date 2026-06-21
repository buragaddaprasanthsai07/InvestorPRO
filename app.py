import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import time
from datetime import datetime, timedelta
from agent import run_financial_analysis
from tools import (
    get_stock_fundamentals,
    get_recent_news,
    compare_performance,
    analyze_dividend_potential,
    assess_risk_profile,
    analyze_growth_metrics,
    analyze_insider_activity,
    valuation_snapshot,
    calculate_quality_score,
    estimate_price_target
)

# Set page configuration
st.set_page_config(
    page_title="🚀 InvestorPRO - AI Stock Analyzer",
    layout="wide",
    page_icon="📈",
    initial_sidebar_state="expanded"
)

# ============ PREMIUM THEME & STYLING ============
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700;900&family=Space+Mono:wght@400;700&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    :root {
        --primary: #00D4FF;
        --secondary: #FF006E;
        --accent: #8338EC;
        --dark: #0a0e27;
        --darker: #050811;
        --light: #f0f0ff;
        --success: #00FF88;
        --danger: #FF3333;
        --warning: #FFB703;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0a0e27 0%, #1a1d3a 100%);
        color: #e0e0ff;
    }
    
    /* HERO SECTION */
    .hero-container {
        background: linear-gradient(135deg, rgba(0, 212, 255, 0.1), rgba(255, 0, 110, 0.1), rgba(131, 56, 236, 0.1));
        border: 2px solid rgba(0, 212, 255, 0.3);
        border-radius: 20px;
        padding: 40px;
        margin-bottom: 30px;
        animation: glow 3s ease-in-out infinite;
        backdrop-filter: blur(10px);
    }
    
    @keyframes glow {
        0%, 100% { border-color: rgba(0, 212, 255, 0.3); }
        50% { border-color: rgba(0, 212, 255, 0.6); }
    }
    
    .hero-title {
        font-size: 3.5rem;
        font-weight: 900;
        background: linear-gradient(135deg, #00D4FF, #FF006E, #8338EC, #00FF88);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0;
        animation: slideDown 0.8s ease-out;
    }
    
    @keyframes slideDown {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes slideUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .search-container {
        background: rgba(255, 255, 255, 0.05);
        border: 2px solid rgba(0, 212, 255, 0.2);
        border-radius: 15px;
        padding: 25px;
        margin-bottom: 30px;
        backdrop-filter: blur(10px);
        animation: fadeIn 0.8s ease-out 0.2s both;
    }
    
    .search-label {
        font-size: 1.1rem;
        font-weight: 700;
        color: #00D4FF;
        margin-bottom: 15px;
        display: block;
    }
    
    .metric-card {
        background: linear-gradient(135deg, rgba(0, 212, 255, 0.1), rgba(131, 56, 236, 0.1));
        border: 2px solid rgba(0, 212, 255, 0.3);
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        animation: popIn 0.5s ease-out;
    }
    
    @keyframes popIn {
        from {
            opacity: 0;
            transform: scale(0.95);
        }
        to {
            opacity: 1;
            transform: scale(1);
        }
    }
    
    .metric-card:hover {
        border-color: rgba(0, 212, 255, 0.6);
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(0, 212, 255, 0.2);
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #a0a0ff;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 8px;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 900;
        color: #00D4FF;
        font-family: 'Space Mono', monospace;
    }
    
    .positive { color: #00FF88; }
    .negative { color: #FF3333; }
    .neutral { color: #FFB703; }
    
    .status-badge {
        display: inline-block;
        padding: 8px 16px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 700;
        margin: 5px;
    }
    
    .badge-bullish {
        background: rgba(0, 255, 136, 0.2);
        color: #00FF88;
        border: 2px solid #00FF88;
    }
    
    .badge-bearish {
        background: rgba(255, 51, 51, 0.2);
        color: #FF3333;
        border: 2px solid #FF3333;
    }
    
    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(0, 212, 255, 0.2);
        border-radius: 20px;
        padding: 30px;
        margin: 20px 0;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }
    
    .glass-card:hover {
        border-color: rgba(0, 212, 255, 0.5);
        background: rgba(255, 255, 255, 0.05);
        box-shadow: 0 8px 32px rgba(0, 212, 255, 0.1);
    }
    
    .section-title {
        font-size: 1.8rem;
        font-weight: 900;
        color: #00D4FF;
        margin: 30px 0 20px 0;
        padding-bottom: 15px;
        border-bottom: 3px solid rgba(0, 212, 255, 0.3);
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #00D4FF, #8338EC);
        border: none;
        color: white;
        padding: 12px 30px;
        font-size: 1rem;
        font-weight: 700;
        border-radius: 10px;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0, 212, 255, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0, 212, 255, 0.5);
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 20px;
        background-color: transparent;
    }
    
    .stTabs [data-baseweb="tab"] {
        color: #a0a0ff;
        font-weight: 600;
        border-radius: 10px;
    }
    
    .stTabs [aria-selected="true"] {
        color: #00D4FF !important;
        background-color: rgba(0, 212, 255, 0.1) !important;
    }
    
    .divider {
        height: 2px;
        background: linear-gradient(90deg, transparent, rgba(0, 212, 255, 0.3), transparent);
        margin: 30px 0;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    .tool-box {
        background: linear-gradient(135deg, rgba(0, 212, 255, 0.08), rgba(131, 56, 236, 0.08));
        border-left: 4px solid #00D4FF;
        border-radius: 10px;
        padding: 20px;
        margin: 15px 0;
        animation: slideUp 0.6s ease-out;
    }
    
    .tool-title {
        color: #00D4FF;
        font-weight: 700;
        font-size: 1.1rem;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .tool-icon {
        font-size: 1.3rem;
    }
    
    .tool-content {
        color: #e0e0ff;
        font-size: 0.95rem;
        line-height: 1.6;
        white-space: pre-wrap;
    }
    
    .loading-dots {
        animation: dots 1.4s infinite;
    }
    
    @keyframes dots {
        0%, 20% { content: '.'; }
        40% { content: '..'; }
        60%, 100% { content: '...'; }
    }
    </style>
""", unsafe_allow_html=True)

# ============ CACHED DATA FUNCTIONS ============
@st.cache_data(ttl=3600)
def fetch_market_data(ticker):
    stock = yf.Ticker(ticker)
    stock_hist = stock.history(period="1y")
    return stock_hist, stock.info

# ============ MAIN INTERFACE ============
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown('<div class="hero-title">🚀 InvestorPRO</div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div style="text-align: right; color: #a0a0ff; font-size: 0.9rem;">{datetime.now().strftime("%H:%M:%S")}</div>', unsafe_allow_html=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ============ SEARCH SECTION ============
st.markdown('<div class="search-container">', unsafe_allow_html=True)

col1, col2 = st.columns([4, 1])

with col1:
    st.markdown('<label class="search-label">🔍 Search Stock Ticker</label>', unsafe_allow_html=True)
    ticker_input = st.text_input(
        "Enter ticker symbol",
        placeholder="AAPL, GOOGL, RELIANCE.NS, INFY",
        label_visibility="collapsed"
    )

with col2:
    st.markdown('<label class="search-label">&nbsp;</label>', unsafe_allow_html=True)
    search_button = st.button("🔎 SEARCH", use_container_width=True, key="search_btn")

st.markdown('</div>', unsafe_allow_html=True)

ticker = ticker_input.upper().strip() if (ticker_input or search_button) else None

if ticker:
    try:
        with st.spinner(f"⚡ Loading {ticker}..."):
            hist_data, info = fetch_market_data(ticker)
            
        # 🛡️ SAFETY NET: Check if Yahoo Finance blocked the data
        if hist_data.empty:
            raise ValueError(f"Yahoo Finance returned no data. This is usually a temporary Cloud IP block. Please wait 60 seconds and try again!")
            
        # Safe calculations
        current_price = info.get('currentPrice') or info.get('regularMarketPrice') or hist_data['Close'].iloc[-1]
        previous_price = info.get('previousClose') or (hist_data['Close'].iloc[-2] if len(hist_data) > 1 else current_price)
        price_change = current_price - previous_price
        pct_change = (price_change / previous_price) * 100 if previous_price != 0 else 0
        
        # ============ QUICK STATS ============
        st.markdown('<h2 class="section-title">📊 Quick Overview</h2>', unsafe_allow_html=True)
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.markdown(f'''
                <div class="metric-card">
                    <div class="metric-label">💰 Price</div>
                    <div class="metric-value">${current_price:.2f}</div>
                </div>
            ''', unsafe_allow_html=True)
        
        with col2:
            color_class = "positive" if price_change > 0 else "negative"
            st.markdown(f'''
                <div class="metric-card">
                    <div class="metric-label">📈 Change</div>
                    <div class="metric-value {color_class}">{pct_change:+.2f}%</div>
                </div>
            ''', unsafe_allow_html=True)
        
        with col3:
            st.markdown(f'''
                <div class="metric-card">
                    <div class="metric-label">📊 Market Cap</div>
                    <div class="metric-value">${info.get('marketCap', 0)/1e9:.1f}B</div>
                </div>
            ''', unsafe_allow_html=True)
        
        with col4:
            st.markdown(f'''
                <div class="metric-card">
                    <div class="metric-label">📉 P/E</div>
                    <div class="metric-value">{info.get('trailingPE', 0):.1f}</div>
                </div>
            ''', unsafe_allow_html=True)
        
        with col5:
            badge_class = "badge-bullish"
            st.markdown(f'''
                <div class="metric-card">
                    <div class="metric-label">🎯 Status</div>
                    <div class="status-badge {badge_class}">ANALYZING</div>
                </div>
            ''', unsafe_allow_html=True)
        
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

        # ============ ADVANCED CHARTING ============
        st.markdown('<h2 class="section-title">📈 Technical Charts</h2>', unsafe_allow_html=True)
        
        # 1. The Interactive Time Selector
        period_options = ["1D", "1W", "1M", "3M", "6M", "1Y", "5Y", "MAX"]
        selected_period_label = st.radio(
            "Select Time Period", 
            options=period_options, 
            index=5, # Defaults to "1Y" when the page loads
            horizontal=True,
            label_visibility="collapsed"
        )
        
        # 2. Map the label to Yahoo Finance's exact format
        period_mapping = {
            "1D": "1d", "1W": "5d", "1M": "1mo", "3M": "3mo", 
            "6M": "6mo", "1Y": "1y", "5Y": "5y", "MAX": "max"
        }
        selected_period = period_mapping[selected_period_label]
        
        # 3. Fetch specific data for the chart dynamically
        with st.spinner(f"Updating chart for {selected_period_label}..."):
            # Use smaller time intervals for short timeframes to make the chart look detailed
            if selected_period == "1d":
                chart_data = yf.Ticker(ticker).history(period="1d", interval="5m")
            elif selected_period == "5d":
                chart_data = yf.Ticker(ticker).history(period="5d", interval="15m")
            else:
                chart_data = yf.Ticker(ticker).history(period=selected_period, interval="1d")
                
            # Fallback just in case Yahoo blocks the intraday data temporarily
            if chart_data.empty:
                chart_data = hist_data 

        chart_tab1, chart_tab2 = st.tabs(["🕯️ Candlestick", "📉 Clean Trend Line"])
        
        common_layout = dict(
            template="plotly_dark", height=450,
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=0, r=0, t=20, b=0),
            xaxis=dict(gridcolor='rgba(255,255,255,0.05)'),
            yaxis=dict(gridcolor='rgba(255,255,255,0.05)')
        )

        with chart_tab1:
            fig_candle = go.Figure(data=[go.Candlestick(
                x=chart_data.index, open=chart_data['Open'], high=chart_data['High'], low=chart_data['Low'], close=chart_data['Close'],
                increasing_line_color='#00FF88', decreasing_line_color='#FF3333'
            )])
            fig_candle.update_layout(**common_layout)
            # Remove the bulky range slider for a cleaner, modern look
            fig_candle.update_xaxes(rangeslider_visible=False) 
            st.plotly_chart(fig_candle, use_container_width=True)

        with chart_tab2:
            fig_line = go.Figure()
            fig_line.add_trace(go.Scatter(
                x=chart_data.index, y=chart_data['Close'], mode='lines', fill='tozeroy', 
                line=dict(color='#00D4FF', width=2), fillcolor='rgba(0, 212, 255, 0.1)'
            ))
            fig_line.update_layout(yaxis_title="Price (USD)", **common_layout)
            st.plotly_chart(fig_line, use_container_width=True)
            
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        
        # ============ AI TOOLS SECTION - THE MAIN FEATURE ============
        st.markdown('<h2 class="section-title">🤖 10 AI Analysis Tools (Running...)</h2>', unsafe_allow_html=True)
        st.markdown('<p style="color: #a0a0ff; margin-bottom: 20px;">Watch as AI tools analyze your stock from multiple angles:</p>', unsafe_allow_html=True)
        
        # Create 2 columns for tools
        tool_col1, tool_col2 = st.columns(2)
        
        # TOOL 1: Stock Fundamentals
        with tool_col1:
            with st.spinner("⏳ Tool 1: Analyzing fundamentals..."):
                time.sleep(0.5)
                fundamentals = get_stock_fundamentals(ticker)
            st.markdown(f'''
                <div class="tool-box">
                    <div class="tool-title">
                        <span class="tool-icon">1️⃣</span>
                        Stock Fundamentals
                    </div>
                    <div class="tool-content">{fundamentals}</div>
                </div>
            ''', unsafe_allow_html=True)
        
        # TOOL 2: Recent News
        with tool_col2:
            with st.spinner("⏳ Tool 2: Gathering news..."):
                time.sleep(0.5)
                news = get_recent_news(ticker)
            st.markdown(f'''
                <div class="tool-box">
                    <div class="tool-title">
                        <span class="tool-icon">2️⃣</span>
                        News & Sentiment
                    </div>
                    <div class="tool-content">{news}</div>
                </div>
            ''', unsafe_allow_html=True)
        
        # TOOL 3: Performance Comparison
        with tool_col1:
            with st.spinner("⏳ Tool 3: Comparing performance..."):
                time.sleep(0.5)
                performance = compare_performance(ticker)
            st.markdown(f'''
                <div class="tool-box">
                    <div class="tool-title">
                        <span class="tool-icon">3️⃣</span>
                        Performance vs S&P 500
                    </div>
                    <div class="tool-content">{performance}</div>
                </div>
            ''', unsafe_allow_html=True)
        
        # TOOL 4: Dividend Analysis
        with tool_col2:
            with st.spinner("⏳ Tool 4: Analyzing dividends..."):
                time.sleep(0.5)
                dividend = analyze_dividend_potential(ticker)
            st.markdown(f'''
                <div class="tool-box">
                    <div class="tool-title">
                        <span class="tool-icon">4️⃣</span>
                        Dividend Analysis
                    </div>
                    <div class="tool-content">{dividend}</div>
                </div>
            ''', unsafe_allow_html=True)
        
        # TOOL 5: Risk Assessment
        with tool_col1:
            with st.spinner("⏳ Tool 5: Assessing risk..."):
                time.sleep(0.5)
                risk = assess_risk_profile(ticker)
            st.markdown(f'''
                <div class="tool-box">
                    <div class="tool-title">
                        <span class="tool-icon">5️⃣</span>
                        Risk Assessment
                    </div>
                    <div class="tool-content">{risk}</div>
                </div>
            ''', unsafe_allow_html=True)
        
        # TOOL 6: Growth Metrics
        with tool_col2:
            with st.spinner("⏳ Tool 6: Analyzing growth..."):
                time.sleep(0.5)
                growth = analyze_growth_metrics(ticker)
            st.markdown(f'''
                <div class="tool-box">
                    <div class="tool-title">
                        <span class="tool-icon">6️⃣</span>
                        Growth Metrics
                    </div>
                    <div class="tool-content">{growth}</div>
                </div>
            ''', unsafe_allow_html=True)
        
        # TOOL 7: Insider Activity
        with tool_col1:
            with st.spinner("⏳ Tool 7: Checking insider activity..."):
                time.sleep(0.5)
                insider = analyze_insider_activity(ticker)
            st.markdown(f'''
                <div class="tool-box">
                    <div class="tool-title">
                        <span class="tool-icon">7️⃣</span>
                        Insider Activity
                    </div>
                    <div class="tool-content">{insider}</div>
                </div>
            ''', unsafe_allow_html=True)
        
        # TOOL 8: Valuation Snapshot
        with tool_col2:
            with st.spinner("⏳ Tool 8: Creating valuation snapshot..."):
                time.sleep(0.5)
                valuation = valuation_snapshot(ticker)
            st.markdown(f'''
                <div class="tool-box">
                    <div class="tool-title">
                        <span class="tool-icon">8️⃣</span>
                        Valuation Snapshot
                    </div>
                    <div class="tool-content">{valuation}</div>
                </div>
            ''', unsafe_allow_html=True)
        
        # TOOL 9: Quality Score
        with tool_col1:
            with st.spinner("⏳ Tool 9: Calculating quality score..."):
                time.sleep(0.5)
                quality = calculate_quality_score(ticker)
            st.markdown(f'''
                <div class="tool-box">
                    <div class="tool-title">
                        <span class="tool-icon">9️⃣</span>
                        Quality Score (A-F Rating)
                    </div>
                    <div class="tool-content">{quality}</div>
                </div>
            ''', unsafe_allow_html=True)
        
        # TOOL 10: Price Target
        with tool_col2:
            with st.spinner("⏳ Tool 10: Estimating price targets..."):
                time.sleep(0.5)
                targets = estimate_price_target(ticker)
            st.markdown(f'''
                <div class="tool-box">
                    <div class="tool-title">
                        <span class="tool-icon">🔟</span>
                        Price Target Estimation
                    </div>
                    <div class="tool-content">{targets}</div>
                </div>
            ''', unsafe_allow_html=True)
        
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        
        # ============ COMPREHENSIVE AI SYNTHESIS ============
        st.markdown('<h2 class="section-title">🧠 AI Synthesis - All Tools Combined</h2>', unsafe_allow_html=True)
        st.markdown('<p style="color: #a0a0ff; margin-bottom: 20px;">Google Gemini AI synthesizes all 10 tools into comprehensive insights:</p>', unsafe_allow_html=True)
        
        with st.spinner("🔄 Generating comprehensive AI analysis..."):
            ai_report = run_financial_analysis(ticker)
        
        st.markdown(f'''
            <div class="glass-card">
                <h3 style="color: #00D4FF; margin-top: 0;">📋 Comprehensive Analysis Report</h3>
                <div style="color: #e0e0ff; line-height: 1.8;">
                    {ai_report}
                </div>
            </div>
        ''', unsafe_allow_html=True)
        
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        
        # ============ INTERACTIVE CHAT ============
        st.markdown('<h2 class="section-title">💬 Ask InvestorPRO</h2>', unsafe_allow_html=True)
        
        col1, col2 = st.columns([4, 1])
        with col1:
            user_question = st.text_input(f"Ask about {ticker}...", placeholder="e.g., 'Why should I buy?' or 'What's the risk?'")
        with col2:
            ask_button = st.button("🎯 Ask", use_container_width=True)
        
        if ask_button and user_question:
            with st.spinner("Thinking..."):
                response = run_financial_analysis(ticker, user_query=user_question)
                st.markdown(f'''
                    <div class="glass-card">
                        <h3 style="color: #00D4FF;">Your Question:</h3>
                        <p>{user_question}</p>
                        <h3 style="color: #00D4FF; margin-top: 20px;">AI Response:</h3>
                        <div style="color: #e0e0ff; line-height: 1.8;">
                            {response}
                        </div>
                    </div>
                ''', unsafe_allow_html=True)
        
    except Exception as e:
        st.markdown(f'''
            <div style="background: rgba(255, 51, 51, 0.1); border-left: 4px solid #FF3333; padding: 20px; border-radius: 10px;">
                <h3 style="color: #FF3333;">❌ Error</h3>
                <p>Unable to fetch data for <strong>{ticker}</strong></p>
                <p style="color: #a0a0ff;">Details: {str(e)}</p>
                <p style="color: #FFB703;">Try with: AAPL, GOOGL, MSFT, RELIANCE.NS, INFY</p>
            </div>
        ''', unsafe_allow_html=True)

else:
    st.markdown('''
        <div style="background: rgba(0, 212, 255, 0.1); border-left: 4px solid #00D4FF; padding: 20px; border-radius: 10px;">
            <h3 style="color: #00D4FF;">👋 Welcome to InvestorPRO</h3>
            <p style="color: #e0e0ff;">Enter a stock ticker to see 10 AI tools analyze it from every angle!</p>
            <p style="color: #a0a0ff;"><strong>Try:</strong> AAPL, GOOGL, MSFT, TSLA, RELIANCE.NS, INFY</p>
        </div>
    ''', unsafe_allow_html=True)

# ============ FOOTER ============
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
st.markdown('''
    <div style="text-align: center; color: #a0a0ff; padding: 20px; font-size: 0.9rem;">
        <strong>InvestorPRO™</strong> | AI-Powered Stock Analysis<br>
        <span style="color: #00D4FF; font-size: 0.8rem;">10 AI Tools • Real-time Data • Professional Analysis</span><br>
        <span style="color: #FF006E; font-size: 0.8rem;">⚠️ Educational purpose only. Not financial advice.</span>
    </div>
''', unsafe_allow_html=True)
