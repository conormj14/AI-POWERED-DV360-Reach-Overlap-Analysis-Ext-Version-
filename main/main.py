"""This example creates and runs a query, downloading the resulting report."""

import argparse
import sys
from googleapiclient.errors import HttpError
from retry.api import retry_call
#import util
from config.authentication import authenticate, get_gcloud_token_and_creds, authenticate_v2
from pathlib import Path
import json
from googleapiclient.discovery import build
#from googleapiclient.http import MediaIoBaseDownload
import pandas as pd

# The following values control retry behavior while the report is processing.
# Minimum amount of time between polling requests. Defaults to 5 seconds.
MIN_RETRY_INTERVAL = 5
# Maximum amount of time between polling requests. Defaults to 5 minutes.
MAX_RETRY_INTERVAL = 5 * 60
# Maximum number of requests to make when polling. Defaults to 100 requests.
MAX_RETRY_COUNT = 100

#REPORT_TEMPLATES = ['added_reach.json', 'raw_spend.json', 'reach_overlap.json', 'weekly_reach.json']

DBM_API_SERVICE_NAME = 'doubleclickbidmanager'
DBM_API_VERSION = 'v2'
DRIVE_API_SERVICE_NAME = 'drive'
DRIVE_API_VERSION = 'v3'



def poll_report(getRequest):
    """Polls the given report and returns it if finished.

    Args:
      getRequest: the Bid Manager API queries.reports.get request object.

    Returns:
      The finished report.

    Raises:
      RuntimeError: If report is not finished.
    """

    print("⏳ Polling report...")

    # Get current status of operation.
    report = getRequest.execute()

    # Check if report is done.
    if (
        report["metadata"]["status"]["state"] != "DONE"
        and report["metadata"]["status"]["state"] != "FAILED"
    ):
        raise RuntimeError(
            "Report polling unsuccessful. Report is still running."
        )

    return report

def main(start_year, start_month, start_day, end_year, end_month, end_day, partner_id, advertiser_id, campaign_id, country):
    """Main function to create, run, and check a DV360 report."""
    
    service = authenticate()

    #service = authenticate_v2()

    #service = get_gcloud_token_and_creds(gcloud_token)

    print("✅ Authentication Successful")

    report_dir = Path(__file__).resolve().parent.parent / "reports" 

    gcs_paths = {}
 
    for report_template in report_dir.iterdir():

        report_name = str(report_template.as_posix())
        report_name = report_name.split('/')[-1]

        with open(report_template, 'r') as f:
            report = json.load(f)

        report['metadata']['dataRange']['customStartDate']['year'] = start_year
        report['metadata']['dataRange']['customStartDate']['month'] = start_month
        report['metadata']['dataRange']['customStartDate']['day'] = start_day
        report['metadata']['dataRange']['customEndDate']['year'] = end_year
        report['metadata']['dataRange']['customEndDate']['month'] = end_month
        report['metadata']['dataRange']['customEndDate']['day'] = end_day
        #report['metadata']['filters'][0]['value'] = partner_id
        #filters is a list of dictionaries with each dict containing the DBM API report filters 
        filters = report['params']['filters']

        #print(report_name)
        #print(filters)

        #filters = []

        for id in partner_id:
             filters.append({
                 "type": "FILTER_PARTNER",
                 "value": id
             })
        for id in advertiser_id:
             filters.append({
                 "type": "FILTER_ADVERTISER",
                 "value": id
             })
        
        if report_name == 'weekly_reach.json':
             for id in campaign_id:
                filters.append({
                    "type": "FILTER_MEDIA_PLAN",
                    "value": id
                })
        
        if report_name != 'spend_raw.json':
             for id in country:
                 filters.append({
                    "type": "FILTER_COUNTRY",
                    "value": id
                })

         #create query responseobject
        query_response = service.queries().create(body=report).execute()
   
        #Log query creation.
        print(f'Query {query_response["queryId"]} was created.')

        # Run query asynchronously.
        report_response = (
            service.queries()
            .run(queryId=query_response["queryId"], synchronous=False)
            .execute()
        )

        # Log information on running report.
        print(
            f'Query {report_response["key"]["queryId"]} is running, report '
            f'{report_response["key"]["reportId"]} has been created and is '
            "currently being generated."
        )

        # Configure the queries.reports.get request.
        get_request = (
            service.queries()
            .reports()
            .get(
                queryId=report_response["key"]["queryId"],
                reportId=report_response["key"]["reportId"],
            )
        )
        

        # Get current status of operation with exponential backoff retry logic.
        report = retry_call(
            poll_report,
            fargs=[get_request],
            exceptions=RuntimeError,
            tries=MAX_RETRY_COUNT,
            delay=MIN_RETRY_INTERVAL,
            max_delay=MAX_RETRY_INTERVAL,
            backoff=2,
            jitter=(0, 60),
        )

        if report["metadata"]["status"]["state"] == "FAILED":
            print(f'Report {report["key"]["reportId"]} finished in error.')
            sys.exit(1)

        print(
            f'Report {report["key"]["reportId"]} generated successfully. Now '
            "downloading."
        )

        gcs_url_path = report["metadata"]["googleCloudStoragePath"] 
        
        
        
       

        #dataframe_name = report_name + "_df"
        
        gcs_paths[report_name] = gcs_url_path

    print(gcs_paths)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Processes DV360 report templates from a Google Drive folder using a gcloud access token.")
    
    #parser.add_argument("--gcloud_token", type=str, required=True, help="gCloud token for authentication")

    # 2. Date Inputs (Required and must be integers)
    # Start Date
    
    parser.add_argument("--start_year", type=str, required=True, help="Start year for the report (e.g., 2024).")
    parser.add_argument("--start_month", type=str, required=True, help="Start month for the report (1-12).")
    parser.add_argument("--start_day", type=str, required=True, help="Start day for the report (1-31).")
    
    # End Date
    parser.add_argument("--end_year", type=str, required=True, help="End year for the report (e.g., 2024).")
    parser.add_argument("--end_month", type=str, required=True, help="End month for the report (1-12).")
    parser.add_argument("--end_day", type=str, required=True, help="End day for the report (1-31).")

    # 3. Filter Inputs (IDs are usually integers, Country is a string)
    parser.add_argument("--partner_id", nargs='+', type=str, required=True, help="The Partner ID to filter the report by.")
    
    # Advertiser ID and Campaign ID might be optional depending on the report template, 
    # but based on your main function logic, they are currently required.
    parser.add_argument("--advertiser_id", nargs='+', type=str, required=True, help="The Advertiser ID to filter the report by.")
    parser.add_argument("--campaign_id", nargs='+', type=str, required=True, help="The Campaign/Media Plan ID to filter the report by.")
    
    # Country is a string (e.g., 'US', 'CA')
    parser.add_argument("--country", nargs='+', type=str, required=True, help="The 2-letter country code (e.g., 'US', 'GB') to filter the report by.")

    # Parse the arguments
    args = parser.parse_args()
    
    # Call main function with ALL parsed arguments
    main(
        #args.gcloud_token,
        args.start_year,
        args.start_month,
        args.start_day,
        args.end_year,
        args.end_month,
        args.end_day,
        args.partner_id,
        args.advertiser_id,
        args.campaign_id,
        args.country
    )



