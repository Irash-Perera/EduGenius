import streamlit as st
import requests
import os
import urllib.parse

from langfuse.decorators import observe, langfuse_context


@observe()
def get_wolframalpha_response(prompt):
    appid = os.getenv('WA_APPID', os.getenv("WOLFRAM_APP_ID"))
    query = urllib.parse.quote_plus(f"solve {prompt}")
                        
    query_url = f"http://api.wolframalpha.com/v2/query?" \
                f"appid={appid}" \
                f"&input={query}" \
                f"&podstate=Result__Step-by-step+solution" \
                "&format=html" \
                f"&output=json"
    
    r = requests.get(query_url).json()
    # with open('data.json', 'w') as json_file:
    #     json.dump(r, json_file)
    langfuse_context.update_current_trace(
        user_id=st.session_state.email
    )
    response = r["queryresult"]
    return response