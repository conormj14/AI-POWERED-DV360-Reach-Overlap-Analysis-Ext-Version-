# AI Powered DV360 Reach Overlap Analysis

**Owner:** Conor Johnston
**Collaborator:** Tim Heywood

### Disclaimer - this is not an official Google supported product

## Instructions to Execute the Solution

Follow these steps to run the analysis:

### Step 1 - Navigate to the Colab Notebook Solution from Conor’s GitHub (Ext_Version_MU_DV360_Reach_Overlap_AI_Powered_Analysis.ipynb - This version includes media unification analysis whereas the other does not)

Click the ‘Open With Colab’ button to open a version of the notebook within a colab environment.

### Step 2 - Generate a Gemini API Key from Google AI Studio

1.  Navigate to this link: `https://aistudio-preprod.corp.google.com/app/apikey`
2.  Click ‘Create an API Key’ to generate some new Gemini API Keys
3.  Once you have generated your Gemini API keys, go to Secrets (Key symbol on left hand side of colab hamburger menu) and import your Gemini API Keys by clicking 'Gemini API Keys' and selecting the 'Import key from Google AI Studio' dropdown button. Note that each user must do this as Colab secrets are held at a user level to ensure a secure setup.

### Step 3 - Pull DV360 Reach Overlap Reports

<h4>DV360 Added Reach Report</h4>
<ol>
<li>Within DV360 instant reporting, filter for and duplicate report id: <strong>1522380568</strong></li>
<li>Customise DV360 Instant Report Filters:</li>
<ul>
<li>Modify the <em>Partner</em>, <em>Country</em> and <em>Campaign (Optional)</em> filters to match your specific campaign or analysis requirements.</li>
<li><em>Optional: </em>You can also create your own report from scratch, as long as it includes (order of fields does not matter):</li>
<ol>
<li><strong>Filters:</strong></li>
<ol>
<li>Partner</li>
<li>Campaign (optional)</li>
</ol>
<li><strong>Dimensions:</strong></li>
<ol>
<li>Partner (Optional),</li>
<li>Partner ID (Optional),</li>
<li>Country (Optional),</li>
<li>Advertiser (Required),</li>
<li>Advertiser ID (Optional),</li>
<li>Campaign ID (Required),</li>
<li>Campaign (Required),</li>
</ol>
<li><strong>Metrics:</strong></li>
<ol>
<li>Unique Reach: Added Impression Reach From Frequency Cap</li>
<li>Unique Reach: Impression Reach,</li>
<li>Unique Reach: Impression Reach (Co-Viewed)</li>
</ol>
</ol>
</ul>
<li><strong>Export the report from DV360:</strong></li>
<ul>
<li>Make sure to export this csv to the same Google Sheet as your other reports</li>
<li><strong>Make sure that the data in your Google Sheet is in the format that is automatically detected, do not format your data</strong></li>
<li>Label the sheet tab: &ldquo;<strong>Added_Reach_Raw_Data</strong>&rdquo;</li>
</ul>
</ol>
<h4>DV360 Spend Report</h4>
<ol>
<li>Within DV360 instant reporting, filter for and duplicate report id: <strong>1541847924</strong></li>
<li>Customise DV360 Instant Report Filters:</li>
<ul>
<li>Modify the <em>Partner</em> and <em>Campaign (Optional)</em> filters to match your specific campaign or analysis requirements.</li>
<li><em>Optional: </em>You can also create your own report from scratch, as long as it includes (order of fields does not matter):</li>
<ol>
<li><strong>Filters:</strong></li>
<ol>
<li>Partner</li>
<li>Campaign (optional)</li>
</ol>
<li><strong>Dimensions:</strong></li>
<ol>
<li>Advertiser (Required),</li>
<li>Advertiser ID (Optional)</li>
<li>Advertiser Currency (Required),</li>
<li>Campaign ID (Required),</li>
<li>Campaign (Required),</li>
</ol>
<li><strong>Metrics:</strong></li>
<ol>
<li>Revenue (Advertiser Currency)</li>
<li>Media Cost (Advertiser Currency)</li>
<li>Platform Fee (Advertiser Currency)</li>
</ol>
</ol>
</ul>
<li><strong>Export the report from DV360:</strong></li>
<ul>
<li>Make sure to export this csv to the same Google Sheet as your other reports</li>
<li><strong>Make sure that the data in your Google Sheet is in the format that is automatically detected, do not format your data</strong></li>
<li>Label the sheet tab: &ldquo;<strong>Spend_Raw_Data</strong>&rdquo;</li>
</ul>
</ol>
<h4>DV360 Reach Overlap Report</h4>
<ol>
<ol>
<li><strong>Access Existing Report:</strong> In the DV360 reporting UI, change the filter to 'Created by Anyone' and search for report ID <strong>1030032295</strong>. <a href="https://screenshot.googleplex.com/3CXjVcH4rtdpnkL">Screenshot example here</a> and <a href="https://screenshot.googleplex.com/5ThofL3BNNwH4iH">here</a></li>
<li><strong>Duplicate Report:</strong> Select the report, and duplicate it.</li>
<li><strong>Customize DV360 Instant Report Filters:</strong></li>
<ul>
<li>Modify the <em>Partner</em>, <em>Country</em>, <em>Advertiser</em>, and <em>Insertion Order</em> filters to match your specific campaign or analysis requirements. - <a href="https://screenshot.googleplex.com/5k3jN6sPXbF7yUU">Example screenshot here</a></li>
<li><em>Optional: </em>You can also create your own report from scratch, as long as it includes (order of fields does not matter):</li>
<ol>
<li><strong>Filters:</strong></li>
<ol>
<li>Country</li>
<li>Advertiser</li>
<li>Insertion Order</li>
</ol>
<li><strong>Dimensions:</strong></li>
<ol>
<li>Country (Required),</li>
<li>Advertiser (Required),</li>
<li>Insertion Order (Required),</li>
</ol>
<li><strong>Metrics:</strong></li>
<ol>
<li>Unique Reach: Overlap Total Reach Percent (Pivoted) (Required)</li>
</ol>
</ol>
</ul>
</ol>
</ol>
<ul>
<li><strong><strong>Export the report from DV360:</strong></strong></li>
</ul>
<ol>
<ul>
<li>Once report has run you can download to drive or to a csv and import into Google Sheets, screenshot examples <a href="https://screenshot.googleplex.com/B76bQ78ZkmM2ZpY">here</a> and <a href="https://screenshot.googleplex.com/9JVeYVCm6FxAF88">here</a></li>
<li><strong>Make sure that the data in your Google Sheet is in the format that is automatically detected, do not format your data</strong> otherwise this could impact how it comes through to the tables and produce errors for your analysis</li>
<li>Label the sheet tab: &ldquo;<strong>Reach_Overlap</strong>&rdquo;</li>
</ul>
</ol>
<h4>DV360 Weekly Reach Report</h4>
<ol>
<li>Within DV360 instant reporting, filter for and duplicate report id: <strong>1522373574</strong></li>
<li>Customise DV360 Instant Report Filters:</li>
<ul>
<li>Modify the <em>Partner</em>, <em>Country</em>, <em>Advertiser</em>, and <em>Insertion Order</em> filters to match your specific campaign or analysis requirements.</li>
<li><em>Optional: </em>You can also create your own report from scratch, as long as it includes (order of fields does not matter):</li>
<ol>
<li><strong>Filters:</strong></li>
<ol>
<li>Country</li>
<li>Advertiser</li>
<li>Campaign (optional)</li>
</ol>
<li><strong>Dimensions:</strong></li>
<ol>
<li>Country (Required),</li>
<li>Partner (Required),</li>
<li>Advertiser (Required),</li>
<li>Campaign (Required),</li>
<li>Week (Required)</li>
</ol>
<li><strong>Metrics:</strong></li>
<ol>
<li>Unique Reach: Impression Reach (Required)</li>
<li>Unique Reach: Impression Reach (Co-viewed) (Required)</li>
<li>Unique Reach: Average Impression Frequency (Required)</li>
<li>Unique Reach: Incremental Impression Reach (Required)</li>
</ol>
</ol>
</ul>
</ol>
<ol>
<li><strong>Export the report from DV360:</strong></li>
<ul>
<li>Make sure to export this csv to the same Google Sheet as your other reports</li>
<li><strong>Make sure that the data in your Google Sheet is in the format that is automatically detected, do not format your data</strong></li>
<li>Label the sheet tab: &ldquo;<strong>Weekly_Reach</strong>&rdquo;</li>
</ul>
</ol>
<h3><strong>Step 2 - Configure the Colab Filters</strong></h3>
<ol>
<li>Open the <a href="https://colab.sandbox.google.com/drive/1cGfK3tspHhJZesSfTOiTVjguFYY3xFWC">Colab Notebook</a></li>
<li>Configure the following parameters within the Colab notebook. These parameters control how the data is processed and visualized: (<strong>NOTE: </strong>filters are case-sensitive, if the visualisations do not load check the exact spelling of the values in the Insertion Order field).</li>
<ol>
<li>CLIENT_NAME: <em>Optional.</em> Placeholder value for email at the end of the notebook</li>
<li>YOUR_NAME: <em>Optional.</em> Placeholder value for email at the end of the notebook</li>
<li>RECEIVER_NAME: <em>Optional.</em> Placeholder value for email at the end of the notebook</li>
<li>GOOGLE_SHEET_NAME: <strong>Required.</strong> Enter the <em>exact name</em> of the Google Sheet containing your DV360 Reach Overlap data.</li>
<li>INCLUDE_ROWS_CONTAINING: <em>Optional.</em> Include only rows (insertion orders or advertisers) whose names <em>contain</em> this substring.</li>
<li>EXCLUDE_ROWS_CONTAINING: <em>Optional.</em> Exclude rows (insertion orders or advertisers) whose names <em>contain</em> this substring.</li>
<li>INCLUDE_COLS_CONTAINING: <em>Optional.</em> Include only columns (pivoted metrics for insertion orders or advertisers) whose names <em>contain</em> this substring.</li>
<li>EXCLUDE_COLS_CONTAINING: <em>Optional.</em> Exclude columns (pivoted metrics for insertion orders or advertisers) whose names <em>contain</em> this substring.</li>
<li>COMPARISON_DIMENSION: <strong>Required.</strong> Choose the entity to compare in the heatmap:</li>
<ol>
<li>Insertion Order (default)</li>
<li>Advertiser</li>
</ol>
<li>ALL_IOs_CHART_SIZE: Adjust the size of the first heatmap (showing all entities):</li>
<ol>
<li>Small</li>
<li>Medium</li>
<li>Large (default)</li>
</ol>
<li>FILTERED_IOS_CHART_SIZE: Adjust the size of the second heatmap (showing only filtered entities):</li>
<ol>
<li>Small</li>
<li>Medium</li>
<li>Large (default)</li>
</ol>
<li>VENN_DIAGRAM_IO_ONE: Optional, the name value of the IO or Advertiser which shows up as the first Venn Diagram circle</li>
<li>VENN_DIAGRAM_IO_TWO: Optional, the name value of the IO or Advertiser which shows up as the second Venn Diagram circle</li>
</ol>
</ol>
<p>For example the following configuration would compare all IO&rsquo;s within the pulled report whose IO name contained BVOD and not YouTube. This would give a comparison of BVOD reach overlap for the defined data set:&nbsp;</p>
<h3><strong>Step 3 - Run the Colab Notebook</strong></h3>
<ol>
<li>Go to the top of the notebook.</li>
<li>Click <strong>Runtime &gt; Run all</strong>.</li>
<ol>
<li><em>Shortcut:</em> You can also press <strong>Ctrl+F9</strong> (Windows) or <strong>Cmd+F9</strong> (macOS).</li>
</ol>
<li>Note: You will be asked to authenticate the linkage of the sheet to this notebook - click allow on this prompt and run again if necessary<br /><br /></li>
</ol>
<p><strong>Step 4 - Use the Results</strong></p>
<p>Copy and paste the generated heatmaps and AI-powered insights into your preferred presentation (<a href="https://docs.google.com/presentation/d/1pRVue3KOlYuIHAvrNV93MPyt0vRmNtrqH9tflIAM6eI/copy?resourcekey=0-uRSRf-G0qYPDANkeowymvA#slide=id.g2d45478f3ab_0_276">Example Reach Overlap Analysis</a>) or email.</p>
<h2><strong>Notes</strong></h2>
<ul>
<ul>
<li><strong>Case Sensitivity:</strong> The text input filters are case-sensitive.</li>
</ul>
</ul>
<ul>
<li><strong><strong>Do not format data in your Google Sheet: </strong>The code is designed to work with the raw unformatted output from DV360 as it comes into your trix, if you format it, you could hit errors that hinder the data coming through into the tables (pandas dataframes) within Colab.</strong></li>
</ul>
<ul>
<li><strong>Interactive Google Sheet:</strong> The embedded Google Sheet within the Colab is interactive. Changes made in the Colab are reflected in the original Google Sheet, and vice-versa.</li>
<li>T<strong>he Exclusive and Duplicate reach bar charts are interactive</strong>: you can hover over bars to get values or zoom into the chart by clicking and dragging. Double click to exit back to the full view version of the graph. Both of these charts show all entities within the report. You can also control the zoom level or download the graph to a png file to then copy to a slide or alternatively screenshot it</li>
<li><strong>Filtering Behavior:</strong> The inclusion/exclusion filters <em>only</em> affect the second heatmap (filtered entities). The first heatmap always displays all rows and columns.</li>
<li><strong>Heatmap Interpretation:</strong> Read heatmaps from left to right. For example, if Row 1 is "Netflix" and Column 1 is "Disney," a value of 45% means 45% of users exposed to a Netflix ad were <em>also</em> exposed to a Disney ad. This is <em>not</em> necessarily reciprocal.</li>
<li><strong>Regenerate AI Insights:</strong> Click the "Play" button next to the AI insights section to generate a new response from Gemini without re-running the entire analysis.</li>
<li><strong>DV360 Help:</strong> For more information, refer to the<a href="https://support.google.com/displayvideo/answer/2823503?hl=en">DV360 Reach Overlap Help Center Article</a>.</li>
</ul>
<h2><strong>How Media Unification Quantification Analysis Can Help Advertisers</strong></h2>
<ul>
<li>A comparison of added reach and thus the value of these impressions saved due to frequency capping is a useful value to compare against the DV360 DSP fees so that you can show the value of cross channel frequency capping within DV360</li>
<li>Weekly unique reach and incremental reach can explain how advertisers can take campaign optimisations to increase or try to decrease incremental reach of new users depending on their marketing objectives e.g widening targeting settings to reach more new users (higher weekly incremental reach) and thus increased overall reach.</li>
</ul>
<h2><strong>How Reach Overlap Analysis Can Help Advertisers</strong></h2>
<p>The usefulness of reach overlap analysis depends on the advertiser's marketing objectives and KPIs:</p>
<ul>
<li><strong>Low Overlap:</strong> Beneficial for advertisers aiming to maximize unique reach.</li>
<li><strong>High Overlap:</strong> Can be positive for advertisers prioritizing increased frequency.</li>
<li><strong>High Overlap with High CPMs:</strong> May indicate inefficiency if the same audience is reached by different insertion orders with significantly different costs.</li>
<li><strong>Higher Exclusive reach:</strong> is better for more overall unique reach</li>
<li><strong>Higher Duplicate reach:</strong> is better for higher ad frequency but it can also be a sign of media buying inefficiency if the desired frequency is already being reached. Recommendations in this scenario could be to shift budget away from such advertisers or IOs or to change targeting or audience lists.</li>
</ul>
<p>This analysis can inform budget optimization recommendations. For instance, you might suggest:</p>
<ul>
<li>Investing more in IOs with low overlap to boost unique reach.</li>
<li>Focusing on low-overlap, low-cost-per-unique-user IOs for efficient reach expansion.</li>
</ul>
<p>The Gemini AI insights provide a starting point, which you can refine and expand upon based on your expertise.</p>

