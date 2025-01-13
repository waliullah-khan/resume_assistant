import streamlit as st 
import tempfile
import os
from dotenv import load_dotenv

# Load env vars
load_dotenv()
openai_api_key = st.secrets["OPENAI_API_KEY"]
astra_db_token = st.secrets["ASTRA_DB_APPLICATION_TOKEN"]
astra_endpoint = st.secrets["ASTRA_DB_API_ENDPOINT"]

st.markdown(
    """
    <style>
    .main {
        background-color: #F7729C;
    }
    .title {
        font-size: 3em;
        color: #4CAF50;
    }
    .subtitle {
        font-size: 1.5em;
        color: #555555;
    }
    .subtext {
        font-size: 1em;
        color: #777777;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Get the current directory
current_dir = os.path.dirname(__file__)

# Construct the file path 
resume_image = os.path.join(current_dir, 'resume.jpeg')
langflow_json = os.path.join(current_dir, 'resume_ai.json')

# Title of the app
# Center the title, header, image, and input form
st.markdown("<h1 style='text-align: center;'>Your Personal Resume Assistant</h1>", unsafe_allow_html=True)

st.markdown("<h2 style='text-align: center;'>Optimize your job searching with ResumAI</h2>", unsafe_allow_html=True)

st.markdown("<h6 style='text-align: center;'>Upload your resume and enter your desired role to get personalized job recommendations</h6>", unsafe_allow_html=True)


st.image(resume_image, width=650, use_container_width='auto')

# Center the input form
desired_role = st.text_input("Desired Role:", key="desired_role", help="Enter the job role you are looking for.")

# file upload
temp_file_path = None
uploaded_file = st.file_uploader("Upload Resume", type=["pdf"])
if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        temp_file.write(uploaded_file.getvalue())
        temp_file_path = temp_file.name

# Langflow Implementation

from langflow.load import run_flow_from_json # type: ignore
TWEAKS = {
  "ChatInput-cmQhY": {
    "files": "",
    "background_color": "",
    "chat_icon": "",
    "input_value": "Designer",
    "sender": "User",
    "sender_name": "User",
    "session_id": "",
    "should_store_message": True,
    "text_color": ""
  },
  "File-b30Rz": {
    "path": f"{temp_file_path}",
    "concurrency_multithreading": 4,
    "silent_errors": False,
    "use_multithreading": False
  },
  "Prompt-8YRJb": {
    "template": "Using the extracted {text} from the resume pdf file, please convert this to pdf format with a clear boundary as best as possible",
    "text": ""
  },
  "ParseData-pUbUm": {
    "sep": "\n",
    "template": "{text}"
  },
  "OpenAIModel-DCbmW": {
    "api_key": "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",
    "input_value": "",
    "json_mode": False,
    "max_tokens": None,
    "model_kwargs": {},
    "model_name": "gpt-4o-mini",
    "openai_api_base": "",
    "output_schema": {},
    "seed": 1,
    "stream": False,
    "system_message": "",
    "temperature": 0.1
  },
  "ParseData-jzU6S": {
    "sep": "\n",
    "template": "{text}"
  },
  "AstraDB-ZTjKe": {
    "advanced_search_filter": "{}",
    "api_endpoint": "https://3ee86012-b981-4da8-ae13-97c975d3be83-us-east-2.apps.astra.datastax.com",
    "batch_size": None,
    "bulk_delete_concurrency": None,
    "bulk_insert_batch_concurrency": None,
    "bulk_insert_overwrite_concurrency": None,
    "collection_indexing_policy": "",
    "collection_name": "job_listings",
    "embedding_choice": "Astra Vectorize",
    "embedding_provider": "OpenAI",
    "model": "text-embedding-3-large",
    "z_04_authentication": {},
    "z_03_provider_api_key": "",
    "z_02_api_key_name": "",
    "z_01_model_parameters": {},
    "keyspace": "",
    "metadata_indexing_exclude": "",
    "metadata_indexing_include": "",
    "metric": "cosine",
    "number_of_results": 4,
    "pre_delete_collection": False,
    "search_filter": {},
    "search_input": "",
    "search_score_threshold": 0,
    "search_type": "Similarity",
    "setup_mode": "Sync",
    "token": "AstraCS:ooZpfTZyBoiDdHgMyGcCxznj:6dbcce35b937828feec0cadea1b661cddfcecb3d832783963b07db7686afc8d1"
  },
  "Prompt-cEhvl": {
    "template": "Here's an improved version of your prompt that's more structured, specific, and comprehensive:\n\nYou are an expert AI Career Coach and Resume Consultant specializing in personalized job search strategies and resume optimization.\n\nYour task is to analyze three key components:\n1. A user's resume in Markdown format\n2. Their desired job role\n3. Current job matches based on vector search results\n\nProvide a detailed analysis and actionable recommendations using the following data:\n\nResume: {resume}\nDesired Role: {job_role}\nJob Matches: {job_matches}\n\nPlease provide a comprehensive analysis in the following structure:\n\n## Qualification Analysis\n- Calculate and display a **Qualification Score** (1-10) for the desired role\n- Break down the scoring criteria:\n  * Technical Skills Match\n  * Experience Relevance\n  * Educational Alignment\n  * Industry Knowledge\n  * Project Relevance\n\n## Current Job Match Analysis\n- List each matching job with individual compatibility scores\n- Provide specific reasons why the candidate qualifies for each position\n- Highlight key resume elements that align with each role\n\n## Gap Analysis & Improvement Recommendations\n- Identify missing critical skills for the desired role\n- Point out specific resume sections that need enhancement\n- Suggest additional certifications or training if needed\n- Recommend specific projects or experiences to pursue\n\n## Resume Optimization\n- Provide a keyword-optimized version of their resume\n- Highlight recommended structural changes\n- Suggest specific bullet point improvements\n- Include ATS (Applicant Tracking System) optimization tips\n\n## Action Plan\n1. Immediate improvements (0-3 months)\n2. Medium-term goals (3-6 months)\n3. Long-term career development (6+ months)\n\n## Optimized Resume\nPresent an adapted version of the resume that:\n- Aligns with {job_role} requirements\n- Maintains authenticity of experience\n- Highlights transferable skills\n- Emphasizes relevant achievements\n- Incorporates industry-specific keywords\n\nPlease provide specific examples and actionable items throughout your analysis. Use bullet points sparingly and focus on detailed, contextual explanations.\n\nNote: All recommendations should be based on current industry standards and best practices for {job_role}.",
    "resume": "",
    "job_matches": "",
    "job_role": ""
  },
  "OpenAIModel-cBhUE": {
    "api_key": "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",
    "input_value": "",
    "json_mode": False,
    "max_tokens": None,
    "model_kwargs": {},
    "model_name": "gpt-4o-mini",
    "openai_api_base": "",
    "output_schema": {},
    "seed": 1,
    "stream": False,
    "system_message": "",
    "temperature": 0.1
  },
  "ChatOutput-dbriO": {
    "background_color": "",
    "chat_icon": "",
    "data_template": "{text}",
    "input_value": "",
    "sender": "Machine",
    "sender_name": "AI",
    "session_id": "",
    "should_store_message": True,
    "text_color": ""
  }
}

# Submit
if st.button("Submit"):
  st.write(f"Your desired role is: {desired_role}") 
  st.write(f"Thank you for submitting the form, now sit tight as the agent work its magic 🙏") 
  
  with st.spinner('Loading your results...'):
    result = run_flow_from_json(flow=langflow_json,
                input_value=f"{desired_role}",
                fallback_to_env_vars=True, # False by default
                tweaks=TWEAKS)

  message = result[0].outputs[0].results['message'].data['text']
  st.write(message)


