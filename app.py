import streamlit as st
import plotly.graph_objects as go
from data_fetcher import get_stock_data
from risk_engine import calculate_volatility, classify_risk

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

# ---------------- SIDEBAR ----------------
st.sidebar.header("🔍 Stock Search")
symbol = st.sidebar.text_input(
    "Enter FULL Stock Symbol",
    placeholder="RELIANCE.NS | TCS.NS | AAPL | MSFT"
)
analyze = st.sidebar.button("🚀 Analyze Stock")

# ---------------- MAIN LOGIC ----------------
if analyze:
    try:
        symbol = symbol.upper().strip()

        if symbol == "":
            st.warning("Please enter a stock symbol.")
        else:
            data = get_stock_data(symbol)

            if data.empty:
                st.error("No data found. Please check the stock symbol.")
            else:
                st.caption(f"Analyzing symbol: **{symbol}**")

                # --------- AI CALCULATION ---------
                volatility = calculate_volatility(data)
                risk = classify_risk(volatility)

                # --------- METRICS ---------
                col1, col2, col3 = st.columns(3)

                col1.metric("Risk Level", risk)
                col2.metric("Volatility", round(volatility, 4))
                col3.metric("Data Period", "Last 6 Months")

                st.markdown("---")

                # --------- TABS ---------
                tab1, tab2, tab3 = st.tabs(
                    ["📊 Price Chart", "🤖 Risk Analysis", "ℹ️ About"]
                )

                # --------- TAB 1: CANDLESTICK ---------
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

                # --------- TAB 2: RISK ---------
                with tab2:
                    st.subheader("🤖 AI Risk Assessment")

                    if risk == "Low Risk":
                        st.success(
                            "🟢 Low Risk Stock\n\n"
                            "This stock shows relatively stable price movement "
                            "and may be suitable for cautious investors."
                        )
                    elif risk == "Medium Risk":
                        st.warning(
                            "🟠 Medium Risk Stock\n\n"
                            "This stock shows moderate volatility. "
                            "Risk management strategies are recommended."
                        )
                    else:
                        st.error(
                            "🔴 High Risk Stock\n\n"
                            "This stock is highly volatile and may not be "
                            "suitable for beginners."
                        )

                # --------- TAB 3: ABOUT ---------
                with tab3:
                    st.markdown("""
### 📌 About This Project

**AI Stock Risk Analyzer** is a decision-support tool that helps investors
understand the **risk level** of a stock using historical price data.

#### 🔍 Key Features
- Automatic stock data fetching  
- Professional candlestick charts  
- Volatility-based risk analysis  
- Clean, fintech-style UI  

⚠️ **Disclaimer**  
This application is for **educational and analysis purposes only**.
It does **not** provide financial advice or predict future prices.
                    """)

    except Exception:
        st.error("Unexpected error occurred. Please try again.")
