import streamlit as st
import requests
import os
import urllib.parse

from langfuse.decorators import observe, langfuse_context

@observe()
def get_wolframalpha_response(prompt):
    appid = os.getenv('WA_APPID', os.getenv("WOLFRAM_APP_ID"))
    query = urllib.parse.quote_plus(f"{prompt}")
      
    #TODO: Solve the issue with the API key                  
    query_url = f"https://www.wolframalpha.com/api/v1/llm-api?"\
                f"input={query}"+"&appid=37V5G6-AWKHA627HK"

    r = requests.get(query_url)
    if r.status_code == 200:
        r=r.text
    else:
        r="Sorry, I couldn't find the answer to your question. Please try again."
        
    # with open('data.json', 'w') as json_file:
    #     json.dump(r, json_file)
    # langfuse_context.update_current_trace(
    #     user_id=st.session_state.email
    # )
    return r

# # Testing
prompt = "how to multiply 2 matrices"
print(get_wolframalpha_response(prompt))
