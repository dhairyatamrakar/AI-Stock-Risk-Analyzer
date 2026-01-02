import streamlit as st
import plotly.graph_objects as go

from data_fetcher import get_stock_data
from risk_engine import calculate_volatility, classify_risk
from stock_search import search_stocks


# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Stock Risk Analyzer",
    page_icon="📊",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
.main {
    background-color: #0E1117;
    color: white;
}
.block-container {
    padding-top: 2rem;
}
div[data-testid="stMetric"] {
    background-color: #161B22;
    padding: 15px;
    border-radius: 12px;
}
hr {
    border: 1px solid #30363d;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("## 📈 AI Stock Risk Analyzer")
st.markdown(
    "##### Automatic, Explainable Risk Analysis using Real Market Data"
)
st.markdown("---")


# ---------------- SIDEBAR : SMART SEARCH ----------------
st.sidebar.header("🔍 Stock Search")

query = st.sidebar.text_input(
    "Search stock (name or symbol)",
    placeholder="Reliance, TCS, Apple, AAPL"
)

# Fetch matching stocks from Yahoo Finance
options = search_stocks(query)

selected_stock = None
if options:
    selected_stock = st.sidebar.selectbox(
        "Matching Results",
        options
    )

analyze = st.sidebar.button("🚀 Analyze Stock")


# ---------------- MAIN LOGIC ----------------
if analyze or selected_stock:
    if not selected_stock:
        st.warning("Please select a stock from the suggestions.")
    else:
        try:
            # Extract symbol from "SYMBOL — Company Name"
            symbol = selected_stock.split(" — ")[0]

            with st.spinner("Fetching market data..."):
                data = get_stock_data(symbol)

            if data.empty:
                st.error("No data available for this stock.")
            else:
                st.caption(f"Analyzing symbol: **{symbol}**")

                # ---------------- AI CALCULATION ----------------
                volatility = calculate_volatility(data)
                risk = classify_risk(volatility)

                # ---------------- METRICS ----------------
                col1, col2, col3 = st.columns(3)

                col1.metric("Risk Level", risk)
                col2.metric("Volatility", round(volatility, 4))
                col3.metric("Data Period", "Last 6 Months")

                st.markdown("---")

                # ---------------- TABS ----------------
                tab1, tab2, tab3 = st.tabs(
                    ["📊 Price Chart", "🤖 Risk Analysis", "ℹ️ About"]
                )

                # -------- TAB 1: CANDLESTICK CHART --------
                with tab1:
                    st.subheader("📊 Candlestick Chart")

                    fig = go.Figure(
                        data=[
                            go.Candlestick(
                                x=data.index,
                                open=data["Open"],
                                high=data["High"],
                                low=data["Low"],
                                close=data["Close"],
                                name="Price"
                            )
                        ]
                    )

                    fig.update_layout(
                        xaxis_title="Date",
                        yaxis_title="Price",
                        xaxis_rangeslider_visible=False,
                        template="plotly_dark",
                        height=520
                    )

                    st.plotly_chart(fig, use_container_width=True)

                # -------- TAB 2: AI RISK EXPLANATION --------
                with tab2:
                    st.subheader("🤖 AI Risk Assessment")

                    if risk == "Low Risk":
                        st.success(
                            "🟢 **Low Risk Stock**\n\n"
                            "The price movement is relatively stable, indicating "
                            "lower volatility compared to most stocks."
                        )
                    elif risk == "Medium Risk":
                        st.warning(
                            "🟠 **Medium Risk Stock**\n\n"
                            "The stock shows moderate volatility. "
                            "Risk management strategies are recommended."
                        )
                    else:
                        st.error(
                            "🔴 **High Risk Stock**\n\n"
                            "The stock is highly volatile and may not be suitable "
                            "for beginners."
                        )

                # -------- TAB 3: ABOUT --------
                with tab3:
                    st.markdown("""
### 📌 About This Application

**AI Stock Risk Analyzer** is a decision-support tool designed to help users
understand **stock market risk** using historical price data.

#### 🔍 Key Features
- Smart stock search with autocomplete  
- Real-time data from Yahoo Finance  
- Professional candlestick charts  
- Volatility-based, explainable AI logic  

⚠️ **Disclaimer**  
This application is for **educational and analytical purposes only**.  
It does **not** provide financial advice or predict future prices.
                    """)

        except Exception:
            st.error("An unexpected error occurred. Please try again.")
