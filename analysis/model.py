from dotenv import load_dotenv
import os
load_dotenv()
from google import genai
from google.genai import types
from analysis.helpers import OverlapInsights



import streamlit as st

def get_gemini_api_key():
    """Retrieves the Gemini API key from Streamlit secrets or environment variables."""
    # 1. Check Streamlit Secrets (for Cloud Deployment)
    if "GEMINI_API_KEY" in st.secrets:
        return st.secrets["GEMINI_API_KEY"]
    
    # 2. Fallback to Environment Variables (for Local Development)
    return os.environ.get("GEMINI_API_KEY", "Key Not Found")

sys_instruct = f"""You are a highly experienced DV360 Specialist. You specialize in crafting and optimizing programmatic advertising strategies that directly drive incremental sales. You have a deep understanding of the digital advertising landscape.

Expertise: Advanced knowledge of programmatic advertising, DV360 platform, audience targeting, campaign optimization, and data analysis. Proven ability to drive incremental sales and demonstrate ROI.

Keep in mind when preparing insights that reach cannot be summed.  High Overlap (Duplicate Reach) is good for building frequency, whereas low overlap (Exclusive Reach) is good for building reach.

Be assertive and confident but approachable and conversational. Use clear, concise language. Aim for a tone that conveys authority and trustworthiness.  Write succinctly and condense paragraphs avoiding jargon or overly formal language.

Ensure output includes:

- A brief introduction that summarizes purpose.
- A bullet-point list of key findings or recommendations.



When prompt starts with "--" please refine the text provided using the above information."""

#vd_data_csv,

def create_gemini_report(mu_data_csv, overlap_data_csv, prompt):
  #loading credentials for Gemini API call
  creds = get_gemini_api_key()

  client = genai.Client(api_key=creds)

  response = client.models.generate_content(
    model="gemini-3-pro-preview",
    config=types.GenerateContentConfig(
        system_instruction=sys_instruct
    ),
    contents=prompt)
  
  return response.text

def write_overlap_insights(overlap_data_csv, prompt):
  #loading credentials for Gemini API call
  creds = get_gemini_api_key()

  client = genai.Client(api_key=creds)

  response = client.models.generate_content(
    model="gemini-3-pro-preview",
    config=types.GenerateContentConfig(
        system_instruction=sys_instruct,
        response_mime_type="application/json",
        response_json_schema=OverlapInsights.model_json_schema(),
    ),
    contents=prompt)
  
  return response.text

