import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib_venn import venn2
from datetime import datetime
#from IPython.display import display, Markdown
#import ipywidgets as widgets
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
from analysis.helpers import overlap_col_cleaner

def plot_rf_weekly_ts(df, campaign):
    """Takes in dataframe and outputs a weekly reach and frequency graph based on a selected campaign input.

  Args:
    df: The input pandas DataFrame.
    campaign: A string value representing the name of the DV360 campaign

  Returns:
    A plotly combo chart with columns for unique reach, incremental reach and avg. frequency"""
    
    # Drop rows where 'Week_Start_Date' is NaT (invalid date entries)
    df = df.dropna(subset=['Week_Start_Date'])
    
    # Filter the DataFrame based on the selected campaign
    filtered_df = df[df['Campaign'] == campaign]

    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add bars for Impression Reach
    fig.add_trace(
        go.Bar(x=filtered_df['Week_Start_Date'], y=filtered_df['Unique Reach: Impression Reach'], name='Unique Reach'),
        secondary_y=False,
    )

    # Add bars for Incremental Reach
    fig.add_trace(
        go.Bar(x=filtered_df['Week_Start_Date'], y=filtered_df['Unique Reach: Incremental Impression Reach'], name='Incremental Reach'),
        secondary_y=False,
    )

    # Add lines for Average Impression Frequency
    fig.add_trace(
        go.Scatter(x=filtered_df['Week_Start_Date'], y=filtered_df['Unique Reach: Average Impression Frequency'], name='Average Frequency', marker=dict(size=10)),
        secondary_y=True,
    )

    # Add figure title
    fig.update_layout(
        title_text="Reach and Frequency Over Time: " + campaign
    )

    # Set x-axis title
    fig.update_xaxes(title_text="Week")

    # Set y-axes titles
    fig.update_yaxes(title_text="Unique Reach (Users)", secondary_y=False)
    fig.update_yaxes(title_text="Average Frequency", secondary_y=True)

    return fig


def create_mu_df(ar_df, spend_df):
    mu_df = ar_df.merge(spend_df, on='Campaign ID', how='left', suffixes=(None, "_y")).drop(columns=['Advertiser_y', 'Advertiser ID_y', 'Campaign_y'])
    mu_df = mu_df.replace('-', 0,inplace=False)
    mu_df = mu_df.astype({'Unique Reach: Added Impression Reach From Frequency Cap': int, 'Unique Reach: Impression Reach':int,'Unique Reach: Impression Reach (Co-Viewed)':int, 'Revenue (Adv Currency)':float, 'Media Cost (Advertiser Currency)':float, 'Platform Fee (Adv Currency)':float})
    #mu_df = pd.to_numeric(mu_df[['Unique Reach: Added Impression Reach From Frequency Cap', 'Unique Reach: Impression Reach']], errors='coerce')
    #dropping rows with 0 reach
    mu_df = mu_df[mu_df['Unique Reach: Impression Reach'] != 0].reset_index(drop=True)
    #dropping rows with 0 spend
    mu_df = mu_df.dropna(subset=['Revenue (Adv Currency)']).reset_index(drop=True)
    #rounding revenue spend to 2 decimals
    mu_df['Revenue (Adv Currency)'] = round(mu_df['Revenue (Adv Currency)'],2)
    #adding baseline_reach
    mu_df['baseline_reach'] = mu_df['Unique Reach: Impression Reach'] - mu_df['Unique Reach: Added Impression Reach From Frequency Cap']
    #adding CPU baseline
    mu_df['CPU_baseline'] = round(mu_df['Revenue (Adv Currency)'] / mu_df['baseline_reach'],2)
    #adding reach savings
    mu_df['reach_savings'] = round(mu_df['Unique Reach: Added Impression Reach From Frequency Cap'] * mu_df['CPU_baseline'],2)
    #adding added reach percentage
    mu_df['added_reach_percentage'] = round(mu_df['Unique Reach: Added Impression Reach From Frequency Cap'] / mu_df['Unique Reach: Impression Reach'],2)
    #adding media_fees
    mu_df['media_fees'] = round(mu_df['Revenue (Adv Currency)'] - mu_df['Media Cost (Advertiser Currency)'],2)
    #checking output df
    return mu_df

def plot_added_reach_stacked_bar_chart(mu_df):
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=mu_df['Campaign'],
        y=mu_df['baseline_reach'],
        name='Baseline Reach',
        marker_color='lightgreen'
    ))

    fig.add_trace(go.Bar(
        x=mu_df['Campaign'],
        y=mu_df['Unique Reach: Added Impression Reach From Frequency Cap'],
        name='Added Reach (Frequency Cap)',
        marker_color='darkgreen'
    ))

    fig.update_layout(
        barmode='stack',
        title_text='Baseline Reach and Added Reach by Campaign',
        xaxis_title="Campaign",
        yaxis_title="Reach",
        legend_title="Reach Type"
    )

    return fig

def plot_reach_savings_fees(mu_df):
    # @title
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=mu_df['Campaign'],
        y=mu_df['reach_savings'],
        name='Reach Savings Value',
        marker_color='lightgreen'
    ))

    fig.add_trace(go.Bar(
        x=mu_df['Campaign'],
        y=mu_df['media_fees'],
        name='Total Media Fees',
        marker_color='darkgreen'
    ))

    fig.update_layout(

        title_text='Reach Savings vs Media Fees',
        xaxis_title="Campaign",
        yaxis_title="$ Value",
        legend_title="Media Unification Value Quantification"
    )

    return fig

def calculate_topline_mvq_metrics(mu_df):
    if mu_df.empty:
        return 0, 0, 0
    
    total_reach_savings = mu_df['reach_savings'].sum()
    baseline_sum = mu_df['baseline_reach'].sum()
    total_added_reach_pct = (mu_df['Unique Reach: Added Impression Reach From Frequency Cap'].sum() / baseline_sum) if baseline_sum != 0 else 0
    total_media_fees = mu_df['Revenue (Adv Currency)'].sum() - mu_df['Media Cost (Advertiser Currency)'].sum()

    return total_reach_savings, total_added_reach_pct, total_media_fees

def plot_venn_diagrams(vd_io_one, vd_io_two, overlap_df):
    if vd_io_one != '' and vd_io_two != '':
        io_1 = vd_io_one
        io_2 = vd_io_two

    try:
        vd_metrics_df = overlap_df[overlap_df['Insertion Order'].isin([io_1, io_2])][['Insertion Order','Unique Reach: Duplicate Total Reach', 'Unique Reach: Exclusive Total Reach', io_1 + ': Unique Reach: Overlap Total Reach', io_2 + ': Unique Reach: Overlap Total Reach']]
        vd_metrics_df['Unique Reach'] = vd_metrics_df['Unique Reach: Duplicate Total Reach'] + vd_metrics_df['Unique Reach: Exclusive Total Reach']
        vd_metrics_df = vd_metrics_df.rename(columns={'Unique Reach: Duplicate Total Reach': 'Duplicate Total Reach', 'Unique Reach: Exclusive Total Reach': 'Exclusive Total Reach', io_1 + ': Unique Reach: Overlap Total Reach': io_1 + ': Overlap Reach',io_2 + ': Unique Reach: Overlap Total Reach':  io_2 + ': Overlap Reach' })
        vd_metrics_df = vd_metrics_df.drop(columns=['Duplicate Total Reach', 'Exclusive Total Reach'])

        io_1_df = vd_metrics_df[vd_metrics_df['Insertion Order'] == io_1]
        io_2_df = vd_metrics_df[vd_metrics_df['Insertion Order'] == io_2]

        #plt.figure(figsize=(15,15))

        set_a = io_1_df['Unique Reach'].sum()
        set_b = io_2_df['Unique Reach'].sum()
        set_c = io_1_df[io_2 + ': Overlap Reach'].sum()

        fig, ax = plt.subplots()

        v = venn2(subsets=(set_a,set_b,set_c), set_labels=(io_1+' Unique Reach',io_2+' Unique Reach', 'Reach Overlap'),ax=ax)

        # Customize labels
        for text in v.set_labels:
            text.set_fontsize(12)
        #these are the numbers in the circles
        for text in v.subset_labels:
            if text:
                text.set_fontsize(14)


        ax.set_title('Reach Overlap Venn Diagram (Unique Users)')
        return fig, vd_metrics_df

    except KeyError as e:
        # handling key errors that may arise from the fact that the venn diagram filter input cannot be found in the sheet
        message = f"Could not find the value(s) of vd_io_one and/or vd_io_two filters within your dataset. Invalid input. Details: {e}"
        # Return an empty figure and the message
        fig, ax = plt.subplots()
        ax.text(0.5, 0.5, message, ha='center', va='center', wrap=True)
        return fig, pd.DataFrame()

def plot_reach_bar_charts(overlap_df,COMPARISON_DIMENSION = 'Insertion Order', BAR_CHARTS_HEIGHT_IN_PIXELS = 1000, BAR_CHARTS_WIDTH_IN_PIXELS=1700):
    #Create the bar plot
    excl_fig = px.bar(overlap_df, x=COMPARISON_DIMENSION, y='Unique Reach: Exclusive Total Reach', color='Unique Reach: Exclusive Total Reach', title=COMPARISON_DIMENSION + ' Exclusive Reach', width=BAR_CHARTS_WIDTH_IN_PIXELS, height=BAR_CHARTS_HEIGHT_IN_PIXELS, color_continuous_scale='darkmint')
    dup_fig = px.bar(overlap_df, x=COMPARISON_DIMENSION, y='Unique Reach: Duplicate Total Reach', color='Unique Reach: Duplicate Total Reach', title=COMPARISON_DIMENSION + ' Exclusive Reach', width=BAR_CHARTS_WIDTH_IN_PIXELS, height=BAR_CHARTS_HEIGHT_IN_PIXELS, color_continuous_scale='darkmint')
    return excl_fig, dup_fig

 
def visualize_reach_overlap_heatmap(df, ALL_IOs_HEATMAP_SIZE = 'Medium'):
    """
    Visualizes the reach overlap data as a heatmap.

    Args:
        df (pd.DataFrame): The DataFrame containing reach overlap data.
    Returns:
        matplotlib.figure.Figure: The matplotlib Figure object.
    """
    # Convert the relevant column to numeric, coercing errors
    df['Unique Reach: Overlap Total Reach %'] = pd.to_numeric(
        df['Unique Reach: Overlap Total Reach %'], errors='coerce'
    )

    # Drop rows where 'Unique Reach: Overlap Total Reach %' is NaN after conversion
    # This handles values like '-' that could not be converted to numbers.
    df_cleaned = df.dropna(subset=['Unique Reach: Overlap Total Reach %'])

    # Create a pivot table for the heatmap
    # Use 'Unique Reach: Overlap Total Reach %' as values
    heatmap_data = df_cleaned.pivot_table(
        index='Insertion Order',
        columns='Other Insertion Order',
        values='Unique Reach: Overlap Total Reach %'
    )

    # Fill NaN values with 0 for better visualization of no overlap
    heatmap_data = heatmap_data.fillna(0)

    fig, ax = plt.subplots(figsize=(16, 12))
    sns.heatmap(
        heatmap_data,
        cmap="Greens", # Choose a colormap
        annot=True, # Annotate the heatmap with the data values
        fmt=".0%",  # Format annotations to two decimal places
        linewidths=.5, # Add lines between cells
        ax=ax
    )
    ax.set_title('Unique Reach Overlap (%) Between Insertion Orders')
    ax.set_xlabel('Other Insertion Order')
    ax.set_ylabel('Insertion Order')
    plt.xticks(rotation=90)
    plt.yticks(rotation=0)
    plt.tight_layout() # Adjust layout to prevent labels from being cut off
    # plt.show() # Removed as the figure object is being returned

    return fig


