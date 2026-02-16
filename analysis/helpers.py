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
from pydantic import BaseModel, Field


def clean_weekly_reach_df(df):
    """
    Converts the 'Week' column to datetime and 'Unique Reach:' columns to specified types.

    Args:
        df: The input pandas DataFrame with weekly reach data.

    Returns:
        A cleaned pandas DataFrame.
    """
    # Convert 'Week' column to datetime, coercing errors to NaT
    df['Week_Start_Date'] = pd.to_datetime(df['Week'].apply(lambda x: x.split(' - ')[0] if isinstance(x, str) and ' - ' in x else None), format='%Y/%m/%d', errors='coerce')

    # Define columns to convert to integer, excluding 'Unique Reach: Average Impression Frequency'
    int_cols = [col for col in df.columns if 'Unique Reach:' in col and col != 'Unique Reach: Average Impression Frequency']

    # Convert specified columns to integer, coercing errors to NaN and then filling NaN with 0
    for col in int_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)

    # Convert 'Unique Reach: Average Impression Frequency' to float, coercing errors to NaN and then filling NaN with 0
    df['Unique Reach: Average Impression Frequency'] = pd.to_numeric(df['Unique Reach: Average Impression Frequency'], errors='coerce').fillna(0).astype(float)

    return df

def set_dtypes(df):
  """Takes in a dataframe and converts metric columns to numeric data types
  Args:
    df: The input pandas DataFrame.
  Returns:
    A pandas dataframe"""

  dimension_cols = ['Partner', 'Partner ID', 'Country', 'Advertiser', 'Advertiser ID', 'Campaign', 'Campaign ID', 'Insertion Order', 'Insertion Order ID', 'Advertiser Currency']
  for col in df.columns:
    if col not in dimension_cols:
      try:
        # Attempt to convert to numeric, coercing errors to NaN
        df[col] = pd.to_numeric(df[col], errors='coerce')
        # Replace NaN with 0 after numeric conversion
        df[col] = df[col].fillna(0)
      except Exception as e:
        print(f"Could not convert column {col} to numeric: {e}")
        # If conversion fails, keep the column as is or handle differently
        # For now, we'll keep it as is, it might be object or string
        pass # Or add other handling like df[col] = df[col].astype(str).fillna('')
  return df


def overlap_col_cleaner(df):
  '''Docstring: This function takes in a Dataframe truncates the irrelevant parts of the column names and then replaces any hyphenated values where no reach overlap was observed to a 0.0 float data type. Ouput: Dataframe'''
  new_col_list = []

  for col in df.columns:
    col = col.split(':')[0]
    new_col_list.append(col)

  df.columns = new_col_list

  df = df.apply(lambda x: pd.to_numeric(x.astype(str).str.replace('-', '0.0', regex=False), errors='coerce'))

  return df

#defining a function to filter insertion order names for a given input string so that users can focus the analysis on one part of a clients activity based on their naming conventions
def filter_io_rows(df, row_filter, rows_to_exclude=None):
    """
    Takes in a dataframe and filters it based on inclusion and exclusion filtering critera

    Args:
      df (dataframe): input pandas dataframe
      row_filter (str): Some criteria to filter the rows of the dataframe based on whether the substring is found within the column header string value
      rows_to_exclude (str, optional): Some criteria to exclude the rows of the dataframe based on whether the substring is found within the column header string value. Defaults to None.

    Returns:
      A filtered pandas dataframe that is a copy of the original input dataframe
      """

    filtered_df = df.copy()
    if row_filter:
        mask = filtered_df.index.str.contains(row_filter)
        filtered_df = filtered_df[mask]

    if rows_to_exclude:
        exclude_mask = filtered_df.index.str.contains(rows_to_exclude)
        filtered_df = filtered_df[~exclude_mask]

    return filtered_df


def filter_io_cols(df, col_filter, cols_to_exclude=None):
  """
    Takes in a dataframe and filters it based on inclusion and exclusion filtering critera

    Args:
      df (dataframe): input pandas dataframe
      row_filter (str): Some criteria to filter the columns of the dataframe based on whether the substring is found within the column header string value
      rows_to_exclude (str, optional): Some criteria to exclude the columns of the dataframe based on whether the substring is found within the column header string value. Defaults to None.

    Returns:
      A filtered pandas dataframe that is a copy of the original input dataframe
      """
  filtered_df = df.copy()
  if col_filter:
    filtered_df = filtered_df.filter(like=col_filter)

  if cols_to_exclude:
    cols = [col for col in filtered_df.columns if cols_to_exclude not in col]
    filtered_df = filtered_df[cols]

  return filtered_df

def clean_dataframe(df, metadata_identifier="Report Time:"):
  """
  Cleans the dataframe by dropping rows containing report metadata.

  Args:
    df: The input pandas DataFrame.
    metadata_identifier: A string that identifies the start of
                         metadata rows. Defaults to "Report Time:".

  Returns:
    A cleaned pandas DataFrame with report metadata rows removed.
  """
  # Drop columns with empty string as name
  df = df.drop(columns=[''], errors='ignore')

  # Find the index of the row containing the metadata identifier in the first column (iloc[:, 0])
  # This assumes the metadata identifier is in the first column before setting headers
  metadata_index = df[df.iloc[:, 0].astype(str) == metadata_identifier].index[0]


  # Drop rows starting from the metadata index
  cleaned_df = df.drop(df.index[metadata_index:])

  # Replace empty strings with NaN
  cleaned_df = cleaned_df.replace('', np.nan)

  # Drop rows with all NaN values
  cleaned_df = cleaned_df.dropna(how='all')

  return cleaned_df

def overlap_col_cleaner(df):
  '''Docstring: This function takes in a Dataframe truncates the irrelevant parts of the column names and then replaces any hyphenated values where no reach overlap was observed to a 0.0 float data type. Ouput: Dataframe'''
  new_col_list = []

  for col in df.columns:
    col = col.split(':')[0]
    new_col_list.append(col)

  df.columns = new_col_list

  df = df.apply(lambda x: pd.to_numeric(x.astype(str).str.replace('-', '0.0', regex=False), errors='coerce'))

  return df

class OverlapInsights(BaseModel):
    high_overlap_buys: List[str] = Field(description = "The top three overlapping pairs of insertion orders or advertisers. Those with the highest % overlap e.g in the format: insertion order 1 + insertion order 2: overlap percentage")
    low_overlap_buys: List[str] = Field(description = "The bottom three overlapping pairs of insertion orders or advertisers. Those with the lowest non-zero % overlap e.g in the format: insertion order 1 + insertion order 2: overlap percentage")
    other_interesting_insights: str = Field(description = "If there is a pattern that can be derived from insertion order or advertiser naming conventions and degree of % overlap. If no pattern return None")
