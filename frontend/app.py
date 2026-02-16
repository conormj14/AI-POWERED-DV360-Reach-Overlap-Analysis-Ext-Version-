
# Add the parent directory to the Python path to import the main module
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from pathlib import Path
import streamlit as st
from datetime import date, timedelta
import pandas as pd
from analysis.visualisations import *
from analysis.model import sys_instruct, create_gemini_report
from main.main import main
from analysis.helpers import OverlapInsights

# Page Configuration
st.set_page_config(
    page_title="AI-Powered DV360 Reach Analysis",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Premium Look
st.markdown("""
<style>
    .main {
        background-color: #f8f9fa;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    /* Premium Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: #f0f2f6;
        padding: 8px 8px 0 8px;
        border-radius: 12px 12px 0 0;
        border-bottom: 2px solid #e0e0e0;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: transparent;
        border-radius: 8px 8px 0 0;
        color: #5f6368;
        font-weight: 500;
        transition: all 0.2s ease;
    }
    .stTabs [data-baseweb="tab"]:hover {
        background-color: rgba(255, 255, 255, 0.5);
        color: #4e8cff;
    }
    .stTabs [aria-selected="true"] {
        background-color: #ffffff !important;
        border-bottom: 3px solid #4e8cff !important;
        color: #4e8cff !important;
        font-weight: 700 !important;
        box-shadow: 0 -2px 10px rgba(0,0,0,0.05);
    }
    
    div[data-testid="stExpander"] {
        border: none;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        background-color: white;
        border-radius: 10px;
    }
    
    /* Tab Content Area Styling */
    div[data-testid="stTab"] {
        background-color: #ffffff;
        padding: 25px;
        border-radius: 0 0 12px 12px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05);
        border: 1px solid #e0e0e0;
        border-top: none;
    }

    /* Simplified Sidebar Input Styling */
    section[data-testid="stSidebar"] div[data-baseweb="input"] {
        border: 1.5px solid #d1d1d1 !important;
        border-radius: 8px !important;
        transition: all 0.2s ease !important;
        background-color: white !important;
        padding-left: 5px !important;
    }

    section[data-testid="stSidebar"] div[data-baseweb="input"]:focus-within {
        border-color: #4e8cff !important;
        box-shadow: 0 0 0 2px rgba(78, 140, 255, 0.2) !important;
    }

    /* Remove ALL other borders in the sidebar inputs to prevent clashing */
    section[data-testid="stSidebar"] [data-baseweb="base-input"] {
        border: none !important;
    }
</style>
""", unsafe_allow_html=True)

script_dir = Path(__file__).parent
logo = script_dir / "DV360-logo.png"

# Sidebar - Report Parameters
with st.sidebar:
    st.image(logo, width=300)
    st.title("Report Parameters")
    
    with st.expander("📅 Date Range", expanded=True):
        today = date.today()
        start_date = st.date_input("Start Date", today - timedelta(days=9))
        end_date = st.date_input("End Date", today - timedelta(days=3))
    
    with st.expander("Analysis Inputs", expanded=True):
        partner_id = st.text_input("Partner IDs", "5073132", help="Comma-separated IDs")
        advertiser_id = st.text_input("Advertiser IDs", "5590853", help="DV360 advertiser ids")
        campaign_id = st.text_input("Campaign IDs", "3835426", help="DV360 campaign ids")
        country = st.text_input("Country Codes", "AU", help="2-letter codes, comma-separated")
        campaign_name = st.text_input("Campaign Name for Analysis", "Optional - leave blank to skip")
    
    with st.expander("🔍 Venn Diagram Setup", expanded=False):
        VENN_DIAGRAM_IO_ONE = st.text_input("IO #1", "Bupa_PHI_DOM_CNV_Health Insurance_Domestic - YT - Awareness - YSC")
        VENN_DIAGRAM_IO_TWO = st.text_input("IO #2", "Bupa_PHI_DOM_CNV_Health Insurance_Domestic - Demand Gen - Consideration - YSC")

    run_report = st.sidebar.button("🚀 Run Analysis Report", use_container_width=True, type="primary")

# Main Content Area
st.title("AI-Powered DV360 Media Unification & Reach Overlap Analysis")
st.markdown("---")

if run_report:
    # Extract dates
    start_year, start_month, start_day = str(start_date.year), str(start_date.month), str(start_date.day)
    end_year, end_month, end_day = str(end_date.year), str(end_date.month), str(end_date.day)

    # Process lists
    partner_id_list = [p.strip() for p in partner_id.split(',')]
    advertiser_id_list = [a.strip() for a in advertiser_id.split(',')]
    campaign_id_list = [c.strip() for c in campaign_id.split(',')]
    country_list = [c.strip() for c in country.split(',')]

    status_container = st.status("Initializing Analysis...", expanded=True)
    
    try:
        status_container.write("Fetching DV360 data...")
        dfs = main(
            start_year, start_month, start_day,
            end_year, end_month, end_day,
            partner_id_list, advertiser_id_list, campaign_id_list, country_list
        )
        status_container.write("Processing dataframes and generating visualizations...")
        
        # 1. Topline Metrics
        mu_df = dfs['mu_df']
        total_reach_savings, total_added_reach_pct, total_media_fees = calculate_topline_mvq_metrics(mu_df)
        
        m_col1, m_col2, m_col3 = st.columns(3)
        m_col1.metric("Total Reach Savings", f"${total_reach_savings:,.2f}", delta="Media Value Quantification", help="Savings from frequency cap optimization")
        m_col2.metric("Total Added Reach %", f"{total_added_reach_pct:.2%}", help="Percentage of reach added via frequency caps")
        m_col3.metric("Total Media Fees", f"${total_media_fees:,.2f}", help="Total investment analyzed")

        st.markdown("---")

        # Create Tabs for Results
        tab1, tab2, tab3, tab4 = st.tabs(["📊 Executive Dashboard", "📈 Detailed Reach Analysis", "🤖 AI Narrative Report", "📑 Raw Data"])

        with tab1:
            st.subheader("Media Unification & Weekly Reach & Frequency Trends")
            
            # Campaign selector for the chart - handle potential mixed types/NaNs
            weekly_df = dfs['weekly_reach_df']
            unique_campaigns = weekly_df['Campaign'].dropna().unique()
            campaign_options = sorted([str(c) for c in unique_campaigns])
            
            selected_campaign = st.selectbox(
                "📈 Select Campaign for Reach & Frequency Analysis",
                options=campaign_options,
                index=campaign_options.index(campaign_name) if campaign_name in campaign_options else 0,
                key="weekly_rf_campaign_selector"
            )
            
            col_a, col_b = st.columns([2, 1])
            
            with col_a:
                weekly_rf_fig = plot_rf_weekly_ts(weekly_df, selected_campaign)
                if hasattr(weekly_rf_fig, 'to_dict'):
                    st.plotly_chart(weekly_rf_fig, use_container_width=True)
                else:
                    st.warning("Could not generate Reach and Frequency chart.")
            
            with col_b:
                st.info(f"**Current View:** {selected_campaign}\n\n**Key Insight:** Weekly trends highlight the efficiency of reach accumulation over time. Spikes in incremental reach often correlate with high-performance flighting windows.")

            st.markdown("---")
            
            col_c, col_d = st.columns(2)
            with col_c:
                st.plotly_chart(plot_added_reach_stacked_bar_chart(mu_df), use_container_width=True)
            with col_d:
                st.plotly_chart(plot_reach_savings_fees(mu_df), use_container_width=True)

        with tab2:
            st.subheader("Exclusive vs. Duplicate Reach Analysis")
            
            exc_dup_df = dfs['exc_dup_reach_df']
            exc_fig, dup_fig = plot_reach_bar_charts(exc_dup_df)
            
            col_e, col_f = st.columns(2)
            with col_e:
                st.plotly_chart(exc_fig, use_container_width=True)
            with col_f:
                st.plotly_chart(dup_fig, use_container_width=True)

            st.markdown("---")
            st.subheader("Reach Overlap Heatmap")
            overlap_df = dfs['reach_overlap_df']
            st.pyplot(fig=visualize_reach_overlap_heatmap(overlap_df), clear_figure=True)
            
            if VENN_DIAGRAM_IO_ONE and VENN_DIAGRAM_IO_TWO:
                st.markdown("---")
                st.subheader("Venn Diagram Comparison")
                vd_fig, vd_df = plot_venn_diagrams(VENN_DIAGRAM_IO_ONE, VENN_DIAGRAM_IO_TWO, overlap_df)
                v_col1, v_col2 = st.columns([1, 1])
                with v_col1:
                    st.pyplot(vd_fig, clear_figure=True)
                with v_col2:
                    st.write("Venn Metrics Table")
                    st.dataframe(vd_df, use_container_width=True)

        with tab3:
            st.subheader("AI-Generated Insights (Gemini 3)")
            
            mu_data_csv = mu_df.to_csv(index=False)
            overlap_data_csv = overlap_df.to_csv(index=False)

            full_prompt = f"""
            Analyze the following DV360 data to provide a comprehensive reach and overlap report.
            The report should be structured with an introduction, key findings as bullet points for each section, and an overall summary. Ensure the tone is consistent with the system instruction (Assertive, specific, ROI-focused).
            Only use bold and normal text formatting in the response. Do not use italics or unnecessary capital letters.

            --- START DATA ---

            ### 1. Media Unification Data:
            {mu_data_csv}

            ### 2. Reach Overlap Data:
            {overlap_data_csv}

            --- END DATA ---

            Please provide a concise, structured report with:
            1. Executive Summary
            2. Media Unification Analysis (Efficiency/Savings)
            3. Exclusive vs Duplicate Reach Analysis
            4. Strategic Recommendations for Budget Optimization
            """
            
            with st.spinner("Gemini is analyzing your data..."):
                report_content = create_gemini_report(mu_data_csv, overlap_data_csv, full_prompt)
                st.markdown(report_content)
                
            st.download_button(
                label="📥 Download AI Report as Text",
                data=report_content,
                file_name=f"DV360_Analysis_{date.today()}.txt",
                mime="text/plain"
            )

        with tab4:
            st.subheader("Raw Data Exports")
            with st.expander("Weekly Reach Data"):
                st.dataframe(dfs['weekly_reach_df'], use_container_width=True)
                st.download_button("Download Weekly Reach CSV", dfs['weekly_reach_df'].to_csv(index=False), "weekly_reach.csv", "text/csv")
                
            with st.expander("Media Unification Data"):
                st.dataframe(mu_df, use_container_width=True)
                st.download_button("Download MU Data CSV", mu_df.to_csv(index=False), "media_unification.csv", "text/csv")
                
            with st.expander("Overlap Data"):
                st.dataframe(overlap_df, use_container_width=True)
                st.download_button("Download Overlap CSV", overlap_df.to_csv(index=False), "reach_overlap.csv", "text/csv")

        status_container.update(label="Analysis Complete!", state="complete", expanded=False)
        st.success("Analysis report generated successfully.")
        
    except Exception as e:
        st.error(f"An error occurred during report generation: {e}")
        st.exception(e)
else:
    st.info("👈 Enter your report parameters in the sidebar and click 'Run Analysis Report' to begin.")
    
    # Placeholder/Marketing Content
    st.subheader("How it works")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write("🔍 **Data Integration**")
        st.write("Directly pulls DV360 reach reports via the reporting API")
    with col2:
        st.write("📊 **Advanced Visualisaton**")
        st.write("Calculates and visualises incremental reach, reach savings, and overlap percentages across insertion orders.")
    with col3:
        st.write("🤖 **AI Insights**")
        st.write("Uses Gemini 3 to analyze complex data patterns and provide actionable strategic recommendations.")
