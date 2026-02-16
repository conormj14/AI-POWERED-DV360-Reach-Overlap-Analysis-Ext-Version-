from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient import discovery
from pathlib import Path
import os
import pickle
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import requests
import json
from google.oauth2.credentials import Credentials


import streamlit as st
from google.oauth2 import service_account

# --- CONFIGURATION ---
# This scope allows for read and write access. Adjust if you only need read-only.
#'https://www.googleapis.com/auth/display-video'
#'displayvideo'

#Get the directory containing this file (the 'config' folder)
CONFIG_DIR = Path(__file__).resolve().parent
SCOPES = ['https://www.googleapis.com/auth/doubleclickbidmanager']
DBM_API_SERVICE_NAME = 'doubleclickbidmanager'
#DBM_API_SERVICE_NAME = 'displayvideo'
DBM_API_VERSION = 'v2'
DRIVE_API_SERVICE_NAME = 'drive'
DRIVE_API_VERSION = 'v3'
CLIENT_SECRETS_FILE = CONFIG_DIR / 'dv_client_secrets.json' # The file you downloaded from Google Cloud
TOKEN_PICKLE_FILE = CONFIG_DIR / 'token.pickle'

cs_json = 'dv_client_secrets.json'

base_dir = Path(__file__).parent

cs_file_path = base_dir / cs_json

def authenticate():
    """Handles OAuth 2.0 authentication and returns an authorized service object."""
    creds = None
    
    # 1. Check Streamlit Secrets (for Cloud Deployment)
    try:
        if "gcp_service_account" in st.secrets:
            # If using a Service Account (highly recommended for servers)
            creds = service_account.Credentials.from_service_account_info(
                st.secrets["gcp_service_account"],
                scopes=SCOPES
            )
        elif "google_oauth" in st.secrets:
            # If using User OAuth (reconstructing from secrets)
            creds = Credentials(
                token=None,  # Will be refreshed
                refresh_token=st.secrets["google_oauth"]["refresh_token"],
                token_uri="https://oauth2.googleapis.com/token",
                client_id=st.secrets["google_oauth"]["client_id"],
                client_secret=st.secrets["google_oauth"]["client_secret"],
                scopes=SCOPES
            )
            creds.refresh(Request())
    except Exception as e:
        # If secrets aren't set up yet, we'll fall back to local files
        pass

    # 2. Fallback to Local Files (for Local Development)
    if not creds:
        # The file token.pickle stores the user's access and refresh tokens.
        if os.path.exists(TOKEN_PICKLE_FILE):
            with open(TOKEN_PICKLE_FILE, 'rb') as token:
                creds = pickle.load(token)
                

        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
                
            else:
                flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
                # This generates the URL but does NOT try to open a browser.
                flow.run_local_server()
                #flow.run_console()

                creds = flow.credentials
            # Save the credentials for the next run
            with open(TOKEN_PICKLE_FILE, 'wb') as token:
                pickle.dump(creds, token)

    # Build and return the dbm service object
    dbm_service = build(DBM_API_SERVICE_NAME, DBM_API_VERSION, credentials=creds)

    # Build and return the drive service object
    #drive_service = build(DRIVE_API_SERVICE_NAME, DRIVE_API_VERSION, credentials=creds)


    return dbm_service



'''
def authenticate_v2():
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    #This generates the URL but does NOT try to open a browser.
    #flow.run_local_server()
    #flow.run_console()

    url, state = flow.authorization_url()

    creds = flow.credentials

    

    # Build and return the dbm service object
    dbm_service = build(DBM_API_SERVICE_NAME, DBM_API_VERSION, credentials=creds)

    return dbm_service


def get_gcloud_token_and_creds(gcloud_token):
    """Creates a Credentials object from the raw gcloud access token."""
    
    # 1. Verify the token and get the scopes (optional but good practice)
    tokeninfo = requests.get(
        "https://www.googleapis.com/oauth2/v3/tokeninfo?access_token=" + gcloud_token
    ).json()
    
    if 'error' in tokeninfo:
        raise ValueError(f"Invalid gcloud token: {tokeninfo.get('error_description', 'Unknown error')}")

    # 2. Create Credentials object from the token
    # The gcloud token often includes all necessary scopes for the APIs enabled
    # for the Service Account, but we need to create the Credentials object.
    creds = Credentials(
        token=gcloud_token,
        # We don't need a client_id/secret for access tokens, only for OAuth flow
    )
    
    # The scopes need to be attached for service builders if they are not inherently in the token object
    # For gcloud tokens, the scopes are implicitly granted, but we can set them for consistency.
    # Note: If this fails, the issue is that gcloud tokens need to be created with explicit scopes
    # which is done via the gcloud command, not here. We rely on the token having the right access.

    # Build and return the dbm service object
    dbm_service = build(DBM_API_SERVICE_NAME, DBM_API_VERSION, credentials=creds)

    return dbm_service

def get_credentials(self) -> Credentials:
    """Builds a credentials object based on current authentication config.

    Note: When oauth config is enabled, this method will launch the flow if no
    credentials exist.

    Returns:
      Credentials object.
    """
    # First, check for application default credentials
    # This is the recommended approach for all use cases. However, it requires
    # a service account for impersonation purposes.
    if self.get_use_default_credentials():
      default_credentials, project_id = google.auth.default()
      if project_id != self.get_project_id():
        if self.is_debug_enabled:
          print("error - project mismatch for billing and default credentials")
          print("gcloud config set project", self.get_project_id())
          exit(1)
        else:
          self.get_logger().warning(
              "project mismatch for billing and default credentials (%s!=%s)",
              project_id,
              self.get_project_id(),
          )
      if (
          self.get_use_service_account()
          and self.get_delegated_service_account()
      ):
        return impersonated_credentials.Credentials(
            source_credentials=default_credentials,
            target_principal=self.get_delegated_service_account(),
            target_scopes=self.CONFIG_API_SCOPES,
        )
      else:
        return default_credentials
    client_secrets = self.get_client_secrets_file()
    storage = oauthFile.Storage(self.get_credentials_file())
    if self.get_use_service_account():
      credentials = ServiceAccountCredentials.from_json_keyfile_name(
          client_secrets, scopes=self.CONFIG_API_SCOPES
      )
      if self.get_delegated_service_account():
        credentials = credentials.create_delegated(
            self.get_delegated_service_account()
        )
    elif not self.get_use_colab():
      flow = client.flow_from_clientsecrets(
          client_secrets,
          scope=Config.CONFIG_API_SCOPES,
          message=tools.message_if_missing(client_secrets),
      )
      credentials = storage.get()
      if credentials is None or credentials.invalid:
        credentials = tools.run_flow(flow, storage)
    else:
      credentials = None
      if os.path.exists(self.get_credentials_file()):
        with open(
            self.get_credentials_file(), "r", encoding="utf-8"
        ) as token_file:
          token_data = json.load(token_file)
          credentials = Credentials.from_authorized_user_info(
              token_data, self.CONFIG_API_SCOPES
          )
      if credentials is None or credentials.expired:
        if (
            credentials is not None
            and credentials.expired
            and credentials.refresh_token
        ):
          credentials.refresh(Request())
        else:
          flow = InstalledAppFlow.from_client_secrets_file(
              client_secrets,
              self.CONFIG_API_SCOPES,
              redirect_uri="https://localhost:8080",
          )
          auth_url, _ = flow.authorization_url(prompt="consent")
          print("credentials expired or not created")
          print()
          print("\033[1mIn your local browser, visit...\033[0m")
          print()
          print(auth_url)
          print()
          print("""  - You may be asked to log in.
            - You may be asked to approve scopes required to run workflows.
            - After authenticating, you will land on an \033[91mERROR
              PAGE\033[0m THAT READS \033[91mThis site can’t be reached\033[0m.
            - Thats \033[1mOK\033[0m, copy the BROWSER URL from
              the \033[91mERROR PAGE\033[0m. """)

          url = input("""Click to the right of this text and
                      paste the BROWSER URL,
                      then press enter or return: """).strip()
          print()
          print("  - You should have valid credentials now")
          print()

          code = urllib.parse.parse_qs(urllib.parse.urlparse(url).query)[
              "code"
          ][0]
          flow.fetch_token(code=code)
          credentials = flow.credentials
        with open(
            self.get_credentials_file(), "w", encoding="utf-8"
        ) as token_file:
          token_file.write(credentials.to_json())
    return credentials
'''