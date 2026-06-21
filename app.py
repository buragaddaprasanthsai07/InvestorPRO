import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots
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
    </style>
""", unsafe_allow_html=True)

# ============ CACHED DATA FUNCTIONS ============
@st.cache_data(ttl=3600)
def fetch_market_data(ticker):
    stock = yf.Ticker(ticker)
    stock_hist = stock.history(period="1y")
    return stock_hist, stock.info

@st.cache_data(ttl=300) # Caches for 5 minutes so it doesn't break API limits
def fetch_market_indices():
    indices = {
        "NIFTY 50": "^NSEI",
        "SENSEX": "^BSESN",
        "BANKNIFTY": "^NSEBANK"
    }
    results = {}
    for name, ticker in indices.items():
        try:
            hist = yf.Ticker(ticker).history(period="5d")
            if not hist.empty and len(hist) >= 2:
                current = hist['Close'].iloc[-1]
                prev = hist['Close'].iloc[-2]
                change = current - prev
                pct = (change/prev) * 100
                results[name] = {"price": current, "change": change, "pct": pct}
        except:
            pass
    return results

# ============ MAIN INTERFACE ============
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown('<div class="hero-title">🚀 InvestorPRO</div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div style="text-align: right; color: #a0a0ff; font-size: 0.9rem;">{datetime.now().strftime("%H:%M:%S")}</div>', unsafe_allow_html=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ============ LIVE MARKET TICKER ============
market_data = fetch_market_indices()
if market_data:
    ticker_html = '<div style="display: flex; justify-content: space-around; flex-wrap: wrap; background: rgba(0, 212, 255, 0.05); border: 1px solid rgba(0, 212, 255, 0.2); padding: 15px 20px; border-radius: 10px; margin-bottom: 25px; backdrop-filter: blur(5px);">'
    for name, data in market_data.items():
        color = "#00FF88" if data['change'] >= 0 else "#FF3333" 
        sign = "+" if data['change'] >= 0 else ""
        ticker_html += f'''
            <div style="font-family: 'Space Mono', monospace; font-size: 0.95rem; margin: 5px 10px;">
                <span style="color: #a0a0ff; font-weight: 700; margin-right: 8px;">{name}</span>
                <span style="color: #e0e0ff; font-weight: 600; margin-right: 8px;">{data['price']:,.2f}</span>
                <span style="color: {color}; font-weight: 600;">{sign}{data['change']:,.2f} ({sign}{data['pct']:.2f}%)</span>
            </div>
        '''
    ticker_html += '</div>'
    st.markdown(ticker_html, unsafe_allow_html=True)

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
            if selected_period == "1d":
                chart_data = yf.Ticker(ticker).history(period="1d", interval="5m")
            elif selected_period == "5d":
                chart_data = yf.Ticker(ticker).history(period="5d", interval="15m")
            else:
                chart_data = yf.Ticker(ticker).history(period=selected_period, interval="1d")
                
            if chart_data.empty:
                chart_data = hist_data 

        chart_tab1, chart_tab2 = st.tabs(["🕯️ Candlestick + Volume", "📉 Clean Trend Line"])
        
        common_layout = dict(
            template="plotly_dark", height=550,
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=0, r=0, t=20, b=0),
            xaxis=dict(gridcolor='rgba(255,255,255,0.05)'),
            yaxis=dict(gridcolor='rgba(255,255,255,0.05)')
        )

        with chart_tab1:
            # Create subplots: 2 rows (Top for Candle, Bottom for Volume)
            fig_candle = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                                       vertical_spacing=0.03, subplot_titles=('', ''),
                                       row_width=[0.2, 0.7])

            # Add Candlestick trace
            fig_candle.add_trace(go.Candlestick(
                x=chart_data.index, open=chart_data['Open'], high=chart_data['High'], low=chart_data['Low'], close=chart_data['Close'],
                increasing_line_color='#00FF88', decreasing_line_color='#FF3333',
                name='Price'
            ), row=1, col=1)

            # Add Volume trace
            colors = ['#00FF88' if row['Close'] >= row['Open'] else '#FF3333' for index, row in chart_data.iterrows()]
            fig_candle.add_trace(go.Bar(
                x=chart_data.index, y=chart_data['Volume'],
                marker_color=colors,
                name='Volume'
            ), row=2, col=1)

            fig_candle.update_layout(**common_layout, showlegend=False)
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
        
        # ============ MULTI-TOOL DATA TERMINAL ============
        st.markdown('<h2 class="section-title">📊 Granular Data Terminal</h2>', unsafe_allow_html=True)
        st.markdown('<p style="color: #a0a0ff; margin-top: -15px; margin-bottom: 20px;">Click through the tabs below to inspect raw metrics pulled from the 10 analysis tools.</p>', unsafe_allow_html=True)
        
        # Create tabs matching the layout of professional terminals
        terminal_tabs = st.tabs([
            "📋 Fundamentals", 
            "📰 Recent News", 
            "📈 Dividends", 
            "⚠️ Risk Profile", 
            "📊 Growth Metrics", 
            "👥 Insider Activity",
            "💎 Valuation Snapshot",
            "🎯 Price Targets & Quality"
        ])
        
        with terminal_tabs[0]:
            st.markdown("### Core Financial Fundamentals")
            try:
                fundamentals_raw = get_stock_fundamentals(ticker)
                st.text_area("Raw Data Output", value=fundamentals_raw, height=250, label_visibility="collapsed")
            except Exception as e:
                st.error(f"Could not load fundamentals: {e}")
                
        with terminal_tabs[1]:
            st.markdown("### Market News & Sentiment Headlines")
            try:
                news_raw = get_recent_news(ticker)
                st.text_area("Raw Data Output", value=news_raw, height=250, label_visibility="collapsed")
            except Exception as e:
                st.error(f"Could not load news: {e}")
                
        with terminal_tabs[2]:
            st.markdown("### Dividend History & Yield Analysis")
            try:
                dividend_raw = analyze_dividend_potential(ticker)
                st.text_area("Raw Data Output", value=dividend_raw, height=250, label_visibility="collapsed")
            except Exception as e:
                st.error(f"Could not load dividend metrics: {e}")
                
        with terminal_tabs[3]:
            st.markdown("### Mathematical Risk & Volatility Assessment")
            try:
                risk_raw = assess_risk_profile(ticker)
                st.text_area("Raw Data Output", value=risk_raw, height=250, label_visibility="collapsed")
            except Exception as e:
                st.error(f"Could not load risk metrics: {e}")
                
        with terminal_tabs[4]:
            st.markdown("### Historical Growth & Operational Performance")
            try:
                growth_raw = analyze_growth_metrics(ticker)
                st.text_area("Raw Data Output", value=growth_raw, height=250, label_visibility="collapsed")
            except Exception as e:
                st.error(f"Could not load growth metrics: {e}")
                
        with terminal_tabs[5]:
            st.markdown("### Corporate Insider Trading Activity")
            try:
                insider_raw = analyze_insider_activity(ticker)
                st.text_area("Raw Data Output", value=insider_raw, height=250, label_visibility="collapsed")
            except Exception as e:
                st.error(f"Could not load insider activity: {e}")
                
        with terminal_tabs[6]:
            st.markdown("### Valuation & Multiples Snapshot")
            try:
                valuation_raw = valuation_snapshot(ticker)
                st.text_area("Raw Data Output", value=valuation_raw, height=250, label_visibility="collapsed")
            except Exception as e:
                st.error(f"Could not load valuation snapshot: {e}")
                
        with terminal_tabs[7]:
            col_t1, col_t2 = st.columns(2)
            with col_t1:
                st.markdown("### Quantitative Quality Score")
                try:
                    quality_raw = calculate_quality_score(ticker)
                    st.info(quality_raw)
                except Exception as e:
                    st.error(f"Could not compute score: {e}")
            with col_t2:
                st.markdown("### Target Pricing Projections")
                try:
                    target_raw = estimate_price_target(ticker)
                    st.success(target_raw)
                except Exception as e:
                    st.error(f"Could not compute target targets: {e}")
                    
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
