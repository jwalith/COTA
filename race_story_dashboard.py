"""
Race Story Teller - Interactive Dashboard
A narrative dashboard that tells the story of the COTA race through data visualization.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="Race Story Teller - COTA Race 1",
    page_icon="🏁",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .story-section {
        background-color: #1e1e1e;
        color: #ffffff;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border: 1px solid #444;
    }
    .story-section h4 {
        color: #4CAF50;
        margin-top: 0;
    }
    .story-section p {
        color: #e0e0e0;
        margin-bottom: 0.5rem;
    }
    .story-section strong {
        color: #ffffff;
    }
    .metric-card {
        background-color: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown('<h1 class="main-header">🏁 Race Story Teller</h1>', unsafe_allow_html=True)
st.markdown('<h2 style="text-align: center; color: #666;">COTA Race 1 - Narrative Dashboard</h2>', unsafe_allow_html=True)

# Sidebar
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Choose a section:",
    ["Race Overview", "Position Evolution", "Sector Analysis", "Driver Stories", "Key Moments", "Full Timeline"]
)

# Load data function (loads from CSV/JSON files)
@st.cache_data
def load_data():
    """Load pre-computed data structures from CSV/JSON files."""
    data = {}
    data_dir = Path('dashboard_data')
    
    # Load dashboard summary
    summary_file = data_dir / 'dashboard_summary.json'
    if summary_file.exists():
        import json
        with open(summary_file, 'r') as f:
            data['dashboard_summary'] = json.load(f)
    else:
        data['dashboard_summary'] = {}
    
    # Load CSV files
    csv_files = {
        'viz_position': 'viz_position.csv',
        'viz_sectors': 'viz_sectors.csv',
        'driver_comparison': 'driver_comparison.csv',
        'key_moments': 'key_moments.csv',
        'story_texts': 'story_texts.csv',
        'protagonists_df': 'protagonists_df.csv',
        'turning_points_df': 'turning_points_df.csv'
    }
    
    for key, filename in csv_files.items():
        filepath = data_dir / filename
        if filepath.exists():
            data[key] = pd.read_csv(filepath)
        else:
            data[key] = pd.DataFrame()
    
    return data

# Load data
data = load_data()

# Check if data is available
if data['dashboard_summary'] == {}:
    st.warning("⚠️ **Data not loaded yet!** Please run all cells in `COTA_Race_Story_Analysis.ipynb` first, then save the data structures to CSV/JSON files, or run this dashboard from within the notebook environment.")
    st.info("💡 **Tip:** You can also export the dataframes to CSV files and load them here.")
    
    st.markdown("### Quick Setup Instructions:")
    st.markdown("""
    1. Run all cells in `COTA_Race_Story_Analysis.ipynb`
    2. Export key dataframes to CSV:
       - `viz_position.to_csv('viz_position.csv')`
       - `viz_sectors.to_csv('viz_sectors.csv')`
       - `driver_comparison.to_csv('driver_comparison.csv')`
       - `key_moments.to_csv('key_moments.csv')`
       - `story_texts.to_csv('story_texts.csv')`
    3. Save `dashboard_summary` as JSON
    4. Update this dashboard to load from those files
    """)
else:
    # Page routing
    if page == "Race Overview":
        st.header("📊 Race Overview")
        
        # Summary cards
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Drivers", data['dashboard_summary'].get('total_drivers', 'N/A'))
        with col2:
            st.metric("Total Laps", data['dashboard_summary'].get('total_laps', 'N/A'))
        with col3:
            winner = data['dashboard_summary'].get('winner', 'N/A')
            st.metric("Winner", f"Car #{winner}" if winner != 'N/A' else 'N/A')
        with col4:
            fastest = data['dashboard_summary'].get('fastest_lap_time', 'N/A')
            st.metric("Fastest Lap", f"{fastest:.3f}s" if isinstance(fastest, (int, float)) else 'N/A')
        
        # Story snippets
        if not data['story_texts'].empty:
            st.markdown("### 📖 Race Story")
            for _, snippet in data['story_texts'].iterrows():
                st.markdown(f"""
                <div class="story-section">
                    <h4>{snippet['SECTION']}</h4>
                    <p>{snippet['TEXT']}</p>
                </div>
                """, unsafe_allow_html=True)
        
        # Top 5 finishers
        if not data['driver_comparison'].empty:
            st.markdown("### 🏆 Top 5 Finishers")
            top_5 = data['driver_comparison'].head(5)
            st.dataframe(top_5[['CAR_NUMBER', 'FINAL_POSITION', 'AVG_POSITION', 'FASTEST_LAP']], use_container_width=True)
    
    elif page == "Position Evolution":
        st.header("📈 Position Evolution Over Time")
        
        if not data['viz_position'].empty:
            # Driver selector
            selected_cars = st.multiselect(
                "Select cars to display:",
                options=sorted(data['viz_position']['NUMBER'].unique()),
                default=sorted(data['viz_position']['NUMBER'].unique())[:10]  # Default to first 10
            )
            
            if selected_cars:
                filtered_data = data['viz_position'][data['viz_position']['NUMBER'].isin(selected_cars)]
                
                # Create line chart
                fig = px.line(
                    filtered_data,
                    x='LAP_NUMBER',
                    y='POSITION_AT_LAP',
                    color='CAR_NUMBER',
                    title='Position Over Time',
                    labels={'LAP_NUMBER': 'Lap Number', 'POSITION_AT_LAP': 'Position'},
                    hover_data=['NUMBER']
                )
                fig.update_layout(
                    yaxis=dict(autorange="reversed"),  # Lower position number = better
                    height=600
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Please select at least one car to display.")
        else:
            st.info("Position data not available. Please run the analysis notebook first.")
    
    elif page == "Sector Analysis":
        st.header("⚡ Sector Performance Analysis")
        
        if not data['viz_sectors'].empty:
            # Sector comparison chart
            fig = go.Figure()
            
            cars_to_show = st.multiselect(
                "Select cars:",
                options=sorted(data['viz_sectors']['NUMBER'].unique()),
                default=sorted(data['viz_sectors']['NUMBER'].unique())[:5]
            )
            
            if cars_to_show:
                filtered_sectors = data['viz_sectors'][data['viz_sectors']['NUMBER'].isin(cars_to_show)]
                
                for _, row in filtered_sectors.iterrows():
                    fig.add_trace(go.Scatterpolar(
                        r=[row['S1_avg'], row['S2_avg'], row['S3_avg']],
                        theta=['Sector 1', 'Sector 2', 'Sector 3'],
                        fill='toself',
                        name=f"Car #{int(row['NUMBER'])}"
                    ))
                
                fig.update_layout(
                    polar=dict(radialaxis=dict(visible=True)),
                    showlegend=True,
                    title="Sector Performance Comparison (Average Times)"
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # Sector stats table
                st.markdown("### Sector Statistics")
                st.dataframe(filtered_sectors[['CAR_NUMBER', 'S1_avg', 'S2_avg', 'S3_avg', 'S1_RANK', 'S2_RANK', 'S3_RANK']], use_container_width=True)
        else:
            st.info("Sector data not available. Please run the analysis notebook first.")
    
    elif page == "Driver Stories":
        st.header("👤 Individual Driver Stories")
        
        if not data['driver_comparison'].empty:
            selected_driver = st.selectbox(
                "Select a driver:",
                options=sorted(data['driver_comparison']['CAR_NUMBER'].unique())
            )
            
            if selected_driver:
                driver_data = data['driver_comparison'][data['driver_comparison']['CAR_NUMBER'] == selected_driver].iloc[0]
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"### Car #{int(selected_driver)}")
                    st.metric("Final Position", f"P{int(driver_data['FINAL_POSITION'])}")
                    st.metric("Best Position", f"P{int(driver_data['BEST_POSITION'])}")
                    st.metric("Worst Position", f"P{int(driver_data['WORST_POSITION'])}")
                    st.metric("Position Range", f"{int(driver_data['POSITION_RANGE'])} positions")
                
                with col2:
                    st.metric("Average Position", f"{driver_data['AVG_POSITION']:.1f}")
                    st.metric("Fastest Lap", f"{driver_data['FASTEST_LAP']:.3f}s")
                    st.metric("Lap Time Std Dev", f"{driver_data['LAP_TIME_STD']:.3f}s")
                    st.metric("Consistency (CV)", f"{driver_data['CONSISTENCY_CV']:.1f}%")
                
                # Driver's position over time
                if not data['viz_position'].empty:
                    driver_pos = data['viz_position'][data['viz_position']['NUMBER'] == selected_driver]
                    if not driver_pos.empty:
                        fig = px.line(
                            driver_pos,
                            x='LAP_NUMBER',
                            y='POSITION_AT_LAP',
                            title=f'Car #{int(selected_driver)} Position Over Time',
                            markers=True
                        )
                        fig.update_layout(yaxis=dict(autorange="reversed"))
                        st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Driver comparison data not available. Please run the analysis notebook first.")
    
    elif page == "Key Moments":
        st.header("🎯 Key Moments & Turning Points")
        
        if not data['turning_points_df'].empty:
            st.markdown("### Turning Points")
            for idx, tp in data['turning_points_df'].iterrows():
                st.markdown(f"""
                <div class="story-section">
                    <h4>Lap {tp['LAP']}: {tp['TYPE']}</h4>
                    <p><strong>Impact:</strong> {tp['IMPACT']}</p>
                    <p>{tp['DESCRIPTION']}</p>
                </div>
                """, unsafe_allow_html=True)
        
        if not data['key_moments'].empty:
            st.markdown("### Significant Moments Timeline")
            significant = data['key_moments'][data['key_moments']['IS_SIGNIFICANT'] == True]
            st.dataframe(significant[['LAP', 'ACT', 'FLAG', 'NOTES']], use_container_width=True)
        else:
            st.info("Key moments data not available. Please run the analysis notebook first.")
    
    elif page == "Full Timeline":
        st.header("📅 Complete Race Timeline")
        
        if not data['key_moments'].empty:
            st.dataframe(data['key_moments'], use_container_width=True)
        else:
            st.info("Timeline data not available. Please run the analysis notebook first.")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem;">
    <p>Race Story Teller Dashboard | Built for Hack the Track - Toyota GR Cup</p>
    <p>Data from COTA Race 1 Analysis</p>
</div>
""", unsafe_allow_html=True)

