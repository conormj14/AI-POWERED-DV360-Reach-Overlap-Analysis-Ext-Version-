# AI Powered DV360 Reach Overlap Analysis

**Owner:** Conor Johnston
**Collaborator:** Tim Heywood

## Instructions to Execute the Solution

Follow these steps to run the analysis:

### Step 1 - Navigate to the Colab Notebook Solution from Conor’s GitHub

Click the ‘Open With Colab’ button to open a version of the notebook within a colab environment.

### Step 2 - Generate a Gemini API Key from Google AI Studio

1.  Navigate to this link: `https://aistudio-preprod.corp.google.com/app/apikey`
2.  Click ‘Create an API Key’ and copy and paste the key as a string value to the empty `creds` variable within the model configuration cell of the notebook.

### Step 3 - Pull a DV360 Reach Overlap Report

**Access Existing Report:**
In the DV360 reporting UI, change the filter to 'Created by Anyone' and search for report ID `1030032295`.
* [Screenshot example here](example_screenshot_1_link) and [here](example_screenshot_2_link)

**Duplicate Report:**
Select the report, and duplicate it.

**Customize DV360 Instant Report Filters:**
Modify the Partner, Country, Advertiser, and Insertion Order filters to match your specific campaign or analysis requirements.
* [Example screenshot here](example_screenshot_3_link)

**Optional:** You can also create your own report from scratch, as long as it includes (order of fields does not matter):

* **Filters:**
    * Country
    * Advertiser
    * Insertion Order
* **Dimensions:**
    * Country (Required)
    * Advertiser (Required)
    * Insertion Order (Required)
* **Metrics:**
    * Unique Reach: Overlap Total Reach Percent (Pivoted) (Required)

**Export and Clean:**
Export the report from DV360.
Once the report has run, you can download to Drive or to a CSV and import into Google Sheets.
* [Screenshot examples here](example_screenshot_4_link) and [here](example_screenshot_5_link)

### Step 4 - Configure the Colab Filters

Open the Colab Notebook.
Configure the following parameters within the Colab notebook. These parameters control how the data is processed and visualized: (NOTE: filters are case-sensitive, if the visualizations do not load check the exact spelling of the values in the Insertion Order field).

* `GOOGLE_SHEET_NAME`: **Required.** Enter the exact name of the Google Sheet containing your DV360 Reach Overlap data.
* `INCLUDE_ROWS_CONTAINING`: Optional. Include only rows (insertion orders or advertisers) whose names contain this substring.
* `EXCLUDE_ROWS_CONTAINING`: Optional. Exclude rows (insertion orders or advertisers) whose names contain this substring.
* `INCLUDE_COLS_CONTAINING`: Optional. Include only columns (pivoted metrics for insertion orders or advertisers) whose names contain this substring.
* `EXCLUDE_COLS_CONTAINING`: Optional. Exclude columns (pivoted metrics for insertion orders or advertisers) whose names contain this substring.
* `COMPARISON_DIMENSION`: **Required.** Choose the entity to compare in the heatmap:
    * Insertion Order (default)
    * Advertiser
* `ALL_IOs_CHART_SIZE`: Adjust the size of the first heatmap (showing all entities):
    * Small
    * Medium
    * Large (default)
* `FILTERED_IOS_CHART_SIZE`: Adjust the size of the second heatmap (showing only filtered entities):
    * Small
    * Medium
    * Large (default)

For example, the following configuration would compare all IO’s within the pulled report whose IO name contained 'BVOD' and not 'YouTube'. This would give a comparison of BVOD reach overlap for the defined data set:

GOOGLE_SHEET_NAME = "Your DV360 Reach Overlap Report"
INCLUDE_ROWS_CONTAINING = "BVOD"
EXCLUDE_ROWS_CONTAINING = "YouTube"
COMPARISON_DIMENSION = "Insertion Order"

### Step 5 - Run the Colab Notebook

1.  Go to the top of the notebook.
2.  Click `Runtime` > `Run all`.
    * **Shortcut:** You can also press `Ctrl+F9` (Windows) or `Cmd+F9` (macOS).
    * **Note:** You will be asked to authenticate the linkage of the sheet to this notebook - click allow on this prompt and run again if necessary.

### Step 6 - Use the Results

Copy and paste the generated heatmaps and AI-powered insights into your preferred presentation (Example Reach Overlap Analysis) or email.

## Notes

* **Case Sensitivity:** The text input filters are case-sensitive.
* **Interactive Google Sheet:** The embedded Google Sheet within the Colab is interactive. Changes made in the Colab are reflected in the original Google Sheet, and vice-versa.
* **The Exclusive and Duplicate reach bar charts are interactive:** you can hover over bars to get values or zoom into the chart by clicking and dragging. Double click to exit back to the full view version of the graph. Both of these charts show all entities within the report. You can also control the zoom level or download the graph to a PNG file to then copy to a slide or alternatively screenshot it.
* **Filtering Behavior:** The inclusion/exclusion filters only affect the second heatmap (filtered entities). The first heatmap always displays all rows and columns.
* **Heatmap Interpretation:** Read heatmaps from left to right. For example, if Row 1 is "Netflix" and Column 1 is "Disney," a value of 45% means 45% of users exposed to a Netflix ad were also exposed to a Disney ad. This is not necessarily reciprocal.
* **Regenerate AI Insights:** Click the "Play" button next to the AI insights section to generate a new response from Gemini without re-running the entire analysis.
* **DV360 Help:** For more information, refer to the [DV360 Reach Overlap Help Center Article](link_to_DV360_help_article).

## How Reach Overlap Analysis Can Help Advertisers

The usefulness of reach overlap analysis depends on the advertiser's marketing objectives and KPIs:

* **Low Overlap:** Beneficial for advertisers aiming to maximize unique reach.
* **High Overlap:** Can be positive for advertisers prioritizing increased frequency.
* **High Overlap with High CPMs:** May indicate inefficiency if the same audience is reached by different insertion orders with significantly different costs.
* **Higher Exclusive reach:** is better for more overall unique reach.
* **Higher Duplicate reach:** is better for higher ad frequency but it can also be a sign of media buying inefficiency if the desired frequency is already being reached. Recommendations in this scenario could be to shift budget away from such advertisers or IOs or or to change targeting or audience lists.

This analysis can inform budget optimization recommendations. For instance, you might suggest:

* Investing more in IOs with low overlap to boost unique reach.
* Focusing on low-overlap, low-cost-per-unique-user IOs for efficient reach expansion.

The Gemini AI insights provide a starting point, which you can refine and expand upon based on your expertise.

Reach out to Conor Johnston or Tim Heywood if you have any questions or feature requests.
