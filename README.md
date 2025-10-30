# AI Powered DV360 Reach Overlap Analysis

**Owner:** Conor Johnston
**Collaborator:** Tim Heywood

### Disclaimer - this is not an official Google supported product

## Instructions to Execute the Solution

Follow these steps to run the analysis:

### Step 1 - Navigate to the Colab Notebook Solution from Conor’s GitHub (DV360_Reach_Overlap_AI_Powered_Analysis_ExtVersion)

Click the ‘Open With Colab’ button to open a version of the notebook within a colab environment.

### Step 2 - Generate a Gemini API Key from Google AI Studio

1.  Navigate to this link: `https://aistudio-preprod.corp.google.com/app/apikey`
2.  Click ‘Create an API Key’ to generate some new Gemini API Keys
3.  Once you have generated your Gemini API keys, go to Secrets (Key symbol on left hand side of colab hamburger menu) and import your Gemini API Keys by clicking 'Gemini API Keys' and selecting the 'Import key from Google AI Studio' dropdown button. Note that each user must do this as Colab secrets are held at a user level to ensure a secure setup.

### Step 3 - Pull DV360 Reach Overlap Reports

DV360 Added Reach Report
Within DV360 instant reporting, filter for and duplicate report id: 1522380568
Customise DV360 Instant Report Filters:
Modify the Partner, Country and Campaign (Optional) filters to match your specific campaign or analysis requirements.
Optional: You can also create your own report from scratch, as long as it includes (order of fields does not matter):
Filters:
Partner
Campaign (optional)
Dimensions:
Partner (Optional),
Partner ID (Optional),
Country (Optional),
Advertiser (Required),
Advertiser ID (Optional),
Campaign ID (Required),
Campaign (Required),
Metrics:
Unique Reach: Added Impression Reach From Frequency Cap
Unique Reach: Impression Reach,
Unique Reach: Impression Reach (Co-Viewed)
Export the report from DV360:
Make sure to export this csv to the same Google Sheet as your other reports
Make sure that the data in your Google Sheet is in the format that is automatically detected, do not format your data 
Label the sheet tab: “Added_Reach_Raw_Data”
DV360 Spend Report
Within DV360 instant reporting, filter for and duplicate report id: 1541847924
Customise DV360 Instant Report Filters:
Modify the Partner and Campaign (Optional) filters to match your specific campaign or analysis requirements.
Optional: You can also create your own report from scratch, as long as it includes (order of fields does not matter):
Filters:
Partner
Campaign (optional)
Dimensions:
Advertiser (Required),
Advertiser ID (Optional)
Advertiser Currency (Required),
Campaign ID (Required),
Campaign (Required),
Metrics:
Revenue (Advertiser Currency)
Media Cost (Advertiser Currency)
Platform Fee (Advertiser Currency)
Export the report from DV360:
Make sure to export this csv to the same Google Sheet as your other reports
Make sure that the data in your Google Sheet is in the format that is automatically detected, do not format your data 
Label the sheet tab: “Spend_Raw_Data”
DV360 Reach Overlap Report
Access Existing Report: In the DV360 reporting UI, change the filter to 'Created by Anyone' and search for report ID 1030032295.  Screenshot example here and here
Duplicate Report: Select the report, and duplicate it.
Customize DV360 Instant Report Filters:
Modify the Partner, Country, Advertiser, and Insertion Order filters to match your specific campaign or analysis requirements. - Example screenshot here
Optional: You can also create your own report from scratch, as long as it includes (order of fields does not matter):
Filters:
Country
Advertiser
Insertion Order
Dimensions:
Country (Required),
Advertiser (Required),
Insertion Order (Required),
Metrics:
Unique Reach: Overlap Total Reach Percent (Pivoted) (Required)
Export the report from DV360:
Once report has run you can download to drive or to a csv and import into Google Sheets, screenshot examples here and here
Make sure that the data in your Google Sheet is in the format that is automatically detected, do not format your data otherwise this could impact how it comes through to the tables and produce errors for your analysis
Label the sheet tab: “Reach_Overlap”
DV360 Weekly Reach Report
Within DV360 instant reporting, filter for and duplicate report id: 1522373574
Customise DV360 Instant Report Filters:
Modify the Partner, Country, Advertiser, and Insertion Order filters to match your specific campaign or analysis requirements.
Optional: You can also create your own report from scratch, as long as it includes (order of fields does not matter):
Filters:
Country
Advertiser
Campaign (optional)
Dimensions:
Country (Required),
Partner (Required),
Advertiser (Required),
Campaign (Required),
Week (Required)
Metrics:
Unique Reach: Impression Reach (Required)
Unique Reach: Impression Reach (Co-viewed) (Required)
Unique Reach: Average Impression Frequency (Required)
Unique Reach: Incremental Impression Reach (Required)

Export the report from DV360:
Make sure to export this csv to the same Google Sheet as your other reports
Make sure that the data in your Google Sheet is in the format that is automatically detected, do not format your data 
Label the sheet tab: “Weekly_Reach”
Step 2 - Configure the Colab Filters
Open the Colab Notebook
Configure the following parameters within the Colab notebook. These parameters control how the data is processed and visualized: (NOTE: filters are case-sensitive, if the visualisations do not load check the exact spelling of the values in the Insertion Order field).
CLIENT_NAME: Optional. Placeholder value for email at the end of the notebook
YOUR_NAME: Optional. Placeholder value for email at the end of the notebook
RECEIVER_NAME: Optional. Placeholder value for email at the end of the notebook
GOOGLE_SHEET_NAME: Required. Enter the exact name of the Google Sheet containing your DV360 Reach Overlap data.
INCLUDE_ROWS_CONTAINING: Optional. Include only rows (insertion orders or advertisers) whose names contain this substring.
EXCLUDE_ROWS_CONTAINING: Optional. Exclude rows (insertion orders or advertisers) whose names contain this substring.
INCLUDE_COLS_CONTAINING: Optional. Include only columns (pivoted metrics for insertion orders or advertisers) whose names contain this substring.
EXCLUDE_COLS_CONTAINING: Optional. Exclude columns (pivoted metrics for insertion orders or advertisers) whose names contain this substring.
COMPARISON_DIMENSION: Required. Choose the entity to compare in the heatmap:
Insertion Order (default)
Advertiser
ALL_IOs_CHART_SIZE: Adjust the size of the first heatmap (showing all entities):
Small
Medium
Large (default)
FILTERED_IOS_CHART_SIZE: Adjust the size of the second heatmap (showing only filtered entities):
Small
Medium
Large (default)
VENN_DIAGRAM_IO_ONE: Optional, the name value of the IO or Advertiser which shows up as the first Venn Diagram circle
VENN_DIAGRAM_IO_TWO: Optional, the name value of the IO or Advertiser which shows up as the second Venn Diagram circle
For example the following configuration would compare all IO’s within the pulled report whose IO name contained BVOD and not YouTube.  This would give a comparison of BVOD reach overlap for the defined data set: 

Step 3 - Run the Colab Notebook
Go to the top of the notebook.
Click Runtime > Run all.
Shortcut: You can also press Ctrl+F9 (Windows) or Cmd+F9 (macOS).
Note: You will be asked to authenticate the linkage of the sheet to this notebook - click allow on this prompt and run again if necessary


Step 4 - Use the Results
Copy and paste the generated heatmaps and AI-powered insights into your preferred presentation (Example Reach Overlap Analysis) or email.
Notes
Case Sensitivity: The text input filters are case-sensitive.
Do not format data in your Google Sheet: The code is designed to work with the raw unformatted output from DV360 as it comes into your trix, if you format it, you could hit errors that hinder the data coming through into the tables (pandas dataframes) within Colab.
Interactive Google Sheet: The embedded Google Sheet within the Colab is interactive. Changes made in the Colab are reflected in the original Google Sheet, and vice-versa.
The Exclusive and Duplicate reach bar charts are interactive:  you can hover over bars to get values or zoom into the chart by clicking and dragging. Double click to exit back to the full view version of the graph. Both of these charts show all entities within the report. You can also control the zoom level or download the graph to a png file to then copy to a slide or alternatively screenshot it
Filtering Behavior: The inclusion/exclusion filters only affect the second heatmap (filtered entities). The first heatmap always displays all rows and columns.
Heatmap Interpretation: Read heatmaps from left to right. For example, if Row 1 is "Netflix" and Column 1 is "Disney," a value of 45% means 45% of users exposed to a Netflix ad were also exposed to a Disney ad. This is not necessarily reciprocal.
Regenerate AI Insights: Click the "Play" button next to the AI insights section to generate a new response from Gemini without re-running the entire analysis.
DV360 Help: For more information, refer to the DV360 Reach Overlap Help Center Article.
How Media Unification Quantification Analysis Can Help Advertisers
A comparison of added reach and thus the value of these impressions saved due to frequency capping is a useful value to compare against the DV360 DSP fees so that you can show the value of cross channel frequency capping within DV360
Weekly unique reach and incremental reach can explain how advertisers can take campaign optimisations to increase or try to decrease incremental reach of new users depending on their marketing objectives e.g widening targeting settings to reach more new users (higher weekly incremental reach) and thus increased overall reach.
How Reach Overlap Analysis Can Help Advertisers
The usefulness of reach overlap analysis depends on the advertiser's marketing objectives and KPIs:
Low Overlap: Beneficial for advertisers aiming to maximize unique reach.
High Overlap: Can be positive for advertisers prioritizing increased frequency.
High Overlap with High CPMs: May indicate inefficiency if the same audience is reached by different insertion orders with significantly different costs.
Higher Exclusive reach: is better for more overall unique reach
Higher Duplicate reach: is better for higher ad frequency but it can also be a sign of media buying inefficiency if the desired frequency is already being reached. Recommendations in this scenario could be to shift budget away from such advertisers or IOs or to change targeting or audience lists.
This analysis can inform budget optimization recommendations. For instance, you might suggest:
Investing more in IOs with low overlap to boost unique reach.
Focusing on low-overlap, low-cost-per-unique-user IOs for efficient reach expansion.
The Gemini AI insights provide a starting point, which you can refine and expand upon based on your expertise.
R


