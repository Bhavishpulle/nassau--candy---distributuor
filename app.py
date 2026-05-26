import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Nassau Candy Distributor",
    page_icon="🍫",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

# Title and description
st.title("🍫 Nassau Candy Distributor Analysis")
st.markdown("""
    <p style='font-size: 18px; color: #555;'>
    📊 Comprehensive Sales Analytics of Wonka Bar Products - Unified Mentor Project
    </p>
""", unsafe_allow_html=True)

# Load data with caching
@st.cache_data
def load_data():
    """Load and process the Nassau Candy Distributor dataset"""
    try:
        df = pd.read_csv("Nassau_Candy_Distributor.csv")
        df['Order Date'] = pd.to_datetime(df['Order Date'], format='%d-%m-%Y')
        df['Ship Date'] = pd.to_datetime(df['Ship Date'], format='%d-%m-%Y')
        return df
    except FileNotFoundError:
        st.error("❌ Error: CSV file not found. Please upload 'Nassau_Candy_Distributor.csv'")
        return None

# Load data
df = load_data()

if df is not None:
    # ============================================================================
    # SIDEBAR - FILTERS
    # ============================================================================
    with st.sidebar:
        st.header("🎯 Filters")
        
        # Division filter
        divisions = ["All"] + sorted(df['Division'].unique().tolist())
        selected_division = st.selectbox("Select Division:", divisions)
        
        # Region filter
        regions = ["All"] + sorted(df['Region'].unique().tolist())
        selected_region = st.selectbox("Select Region:", regions)
        
        # Ship Mode filter
        ship_modes = ["All"] + sorted(df['Ship Mode'].unique().tolist())
        selected_ship_mode = st.selectbox("Select Ship Mode:", ship_modes)
        
        st.markdown("---")
        st.markdown("### 📌 Project Info")
        st.markdown("""
        - **Dataset:** Nassau Candy Distributor
        - **Product:** Wonka Bars
        - **Records:** 500+ transactions
        - **Time Period:** 2024-2026
        """)
    
    # Apply filters
    filtered_df = df.copy()
    
    if selected_division != "All":
        filtered_df = filtered_df[filtered_df['Division'] == selected_division]
    if selected_region != "All":
        filtered_df = filtered_df[filtered_df['Region'] == selected_region]
    if selected_ship_mode != "All":
        filtered_df = filtered_df[filtered_df['Ship Mode'] == selected_ship_mode]
    
    # ============================================================================
    # KEY METRICS
    # ============================================================================
    st.header("📈 Key Performance Indicators")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(
            label="Total Orders",
            value=f"{len(filtered_df):,}",
            delta=f"{len(filtered_df)} records",
            delta_color="off"
        )
    
    with col2:
        total_sales = filtered_df['Sales'].sum()
        st.metric(
            label="Total Sales",
            value=f"${total_sales:,.0f}",
            delta=f"Units: {filtered_df['Units'].sum():,}",
            delta_color="off"
        )
    
    with col3:
        total_profit = filtered_df['Gross Profit'].sum()
        st.metric(
            label="Total Profit",
            value=f"${total_profit:,.0f}",
            delta=f"Cost: ${filtered_df['Cost'].sum():,.0f}",
            delta_color="off"
        )
    
    with col4:
        if total_sales > 0:
            profit_margin = (total_profit / total_sales * 100)
            st.metric(
                label="Profit Margin",
                value=f"{profit_margin:.1f}%",
                delta="Performance",
                delta_color="off"
            )
        else:
            st.metric(label="Profit Margin", value="N/A")
    
    with col5:
        avg_order_value = filtered_df['Sales'].mean()
        st.metric(
            label="Avg Order Value",
            value=f"${avg_order_value:,.2f}",
            delta="Per transaction",
            delta_color="off"
        )
    
    st.markdown("---")
    
    # ============================================================================
    # SECTION 1: SALES ANALYSIS
    # ============================================================================
    st.header("📊 Sales Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Sales by Division")
        sales_by_division = filtered_df.groupby('Division')['Sales'].sum().sort_values(ascending=False)
        fig1 = px.bar(
            sales_by_division,
            title="Total Sales by Product Division",
            labels={'value': 'Sales ($)', 'Division': 'Division'},
            color=sales_by_division,
            color_continuous_scale='Viridis'
        )
        fig1.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        st.subheader("Sales by Region")
        sales_by_region = filtered_df.groupby('Region')['Sales'].sum().sort_values(ascending=False)
        fig2 = px.bar(
            sales_by_region,
            title="Total Sales by Region",
            labels={'value': 'Sales ($)', 'Region': 'Region'},
            color=sales_by_region,
            color_continuous_scale='Blues'
        )
        fig2.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig2, use_container_width=True)
    
    # ============================================================================
    # SECTION 2: PROFIT ANALYSIS
    # ============================================================================
    st.header("💰 Profit Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Profit by Division")
        profit_by_division = filtered_df.groupby('Division')['Gross Profit'].sum().sort_values(ascending=False)
        fig3 = px.bar(
            profit_by_division,
            title="Total Profit by Division",
            labels={'value': 'Profit ($)', 'Division': 'Division'},
            color=profit_by_division,
            color_continuous_scale='Greens'
        )
        fig3.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig3, use_container_width=True)
    
    with col2:
        st.subheader("Profit by Region")
        profit_by_region = filtered_df.groupby('Region')['Gross Profit'].sum().sort_values(ascending=False)
        fig4 = px.bar(
            profit_by_region,
            title="Total Profit by Region",
            labels={'value': 'Profit ($)', 'Region': 'Region'},
            color=profit_by_region,
            color_continuous_scale='Reds'
        )
        fig4.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig4, use_container_width=True)
    
    # ============================================================================
    # SECTION 3: PRODUCT PERFORMANCE
    # ============================================================================
    st.header("🎯 Top Performing Products")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Top 10 Products by Sales")
        top_products_sales = filtered_df.groupby('Product Name')['Sales'].sum().sort_values(ascending=False).head(10)
        fig5 = px.barh(
            top_products_sales,
            title="Top 10 Products by Sales",
            labels={'value': 'Sales ($)', 'Product Name': 'Product'},
            color=top_products_sales,
            color_continuous_scale='Blues'
        )
        fig5.update_layout(height=400)
        st.plotly_chart(fig5, use_container_width=True)
    
    with col2:
        st.subheader("Top 10 Products by Profit")
        top_products_profit = filtered_df.groupby('Product Name')['Gross Profit'].sum().sort_values(ascending=False).head(10)
        fig6 = px.barh(
            top_products_profit,
            title="Top 10 Products by Profit",
            labels={'value': 'Profit ($)', 'Product Name': 'Product'},
            color=top_products_profit,
            color_continuous_scale='Greens'
        )
        fig6.update_layout(height=400)
        st.plotly_chart(fig6, use_container_width=True)
    
    # ============================================================================
    # SECTION 4: GEOGRAPHIC ANALYSIS
    # ============================================================================
    st.header("🗺️ Geographic Analysis")
    
    st.subheader("Top 15 Cities by Sales")
    top_cities = filtered_df.groupby('City')['Sales'].sum().sort_values(ascending=False).head(15)
    fig7 = px.bar(
        top_cities,
        title="Top 15 Cities by Total Sales",
        labels={'value': 'Sales ($)', 'City': 'City'},
        color=top_cities,
        color_continuous_scale='Teal'
    )
    fig7.update_layout(height=400)
    st.plotly_chart(fig7, use_container_width=True)
    
    # ============================================================================
    # SECTION 5: SHIPPING ANALYSIS
    # ============================================================================
    st.header("📦 Shipping Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Sales by Ship Mode")
        sales_by_ship = filtered_df.groupby('Ship Mode')['Sales'].sum().sort_values(ascending=False)
        fig8 = px.pie(
            values=sales_by_ship,
            names=sales_by_ship.index,
            title="Sales Distribution by Ship Mode",
            hole=0.3
        )
        st.plotly_chart(fig8, use_container_width=True)
    
    with col2:
        st.subheader("Orders by Ship Mode")
        orders_by_ship = filtered_df['Ship Mode'].value_counts()
        fig9 = px.pie(
            values=orders_by_ship,
            names=orders_by_ship.index,
            title="Order Count by Ship Mode",
            hole=0.3
        )
        st.plotly_chart(fig9, use_container_width=True)
    
    # ============================================================================
    # SECTION 6: TIME SERIES ANALYSIS
    # ============================================================================
    st.header("📅 Time Series Analysis")
    
    st.subheader("Sales Trend Over Time")
    daily_sales = filtered_df.groupby(filtered_df['Order Date'].dt.date)['Sales'].sum()
    fig10 = px.line(
        x=daily_sales.index,
        y=daily_sales.values,
        title="Daily Sales Trend",
        labels={'x': 'Date', 'y': 'Sales ($)'},
        markers=True
    )
    fig10.update_layout(height=400)
    st.plotly_chart(fig10, use_container_width=True)
    
    # ============================================================================
    # SECTION 7: DATA TABLE
    # ============================================================================
    st.header("📋 Detailed Data View")
    
    # Display options
    col1, col2 = st.columns(2)
    with col1:
        show_rows = st.slider("Number of rows to display:", 5, 100, 20)
    with col2:
        sort_by = st.selectbox("Sort by:", ["Order Date", "Sales", "Gross Profit", "Units"])
    
    # Display table
    display_df = filtered_df.sort_values(by=sort_by, ascending=False).head(show_rows)
    st.dataframe(
        display_df[[
            'Order ID', 'Order Date', 'Customer ID', 'Product Name', 
            'Division', 'Region', 'City', 'Sales', 'Units', 'Gross Profit', 'Cost'
        ]],
        use_container_width=True,
        height=400
    )
    
    # ============================================================================
    # DOWNLOAD SECTION
    # ============================================================================
    st.header("💾 Download Data")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Download filtered data as CSV
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            label="📥 Download Filtered Data (CSV)",
            data=csv,
            file_name=f"Nassau_Candy_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
    
    with col2:
        # Download summary statistics
        summary_stats = {
            'Metric': ['Total Sales', 'Total Profit', 'Total Cost', 'Profit Margin (%)', 'Total Orders', 'Total Units'],
            'Value': [
                f"${filtered_df['Sales'].sum():,.2f}",
                f"${filtered_df['Gross Profit'].sum():,.2f}",
                f"${filtered_df['Cost'].sum():,.2f}",
                f"{(filtered_df['Gross Profit'].sum() / filtered_df['Sales'].sum() * 100):.2f}" if filtered_df['Sales'].sum() > 0 else "N/A",
                len(filtered_df),
                filtered_df['Units'].sum()
            ]
        }
        summary_df = pd.DataFrame(summary_stats)
        csv_summary = summary_df.to_csv(index=False)
        st.download_button(
            label="📊 Download Summary Statistics",
            data=csv_summary,
            file_name=f"Summary_Stats_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
    
    # ============================================================================
    # FOOTER
    # ============================================================================
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 20px;'>
        <p>🍫 <strong>Nassau Candy Distributor Analysis</strong> - Wonka Bar Sales Dashboard</p>
        <p>Built with Streamlit | Unified Mentor Project | Data Period: 2024-2026</p>
        <p style='font-size: 12px; color: #999;'>Last Updated: 2026 | All metrics are calculated based on filtered data</p>
    </div>
    """, unsafe_allow_html=True)

else:
    st.error("❌ Unable to load data. Please ensure the CSV file is in the correct location.")
