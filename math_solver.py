import json
import streamlit as st
import requests
import os
import urllib.parse
from env import WOLFRAM_APP_ID

col1, col2 = st.columns(2)
with col1:
    st.header("Have a math problem?")
    st.subheader(" Let's solve it :red[_step-by-step_]💡", divider= 'red')
    
with col2:
    with st.expander("Disclaimer", icon =":material/error:"):
        st.markdown('''
                    - Please ask your problem in the prompt as mentioned [here](%s)
                    - Note that this demo may be unavailable if too many requests are made.''' %"https://www.wolframalpha.com/examples/mathematics/")
    
messages = st.container(height=300)
prompt = st.chat_input("Ask your math question here")
if prompt:
    appid = os.getenv('WA_APPID', WOLFRAM_APP_ID )

    query = urllib.parse.quote_plus(f"solve {prompt}")

                            
    query_url = f"http://api.wolframalpha.com/v2/query?" \
                f"appid={appid}" \
                f"&input={query}" \
                f"&podstate=Result__Step-by-step+solution" \
                "&format=mathml" \
                f"&output=json"
    try:
        r = requests.get(query_url).json()
        # with open('data.json', 'w') as json_file:
        #     json.dump(r, json_file)
            
        result = r["queryresult"]["pods"][1]["subpods"][0]["mathml"]
        
        if len(r["queryresult"]["pods"][1]["subpods"] ) > 1:
            steps = r["queryresult"]["pods"][1]["subpods"][1]["mathml"]
        messages.chat_message("user").markdown(prompt, unsafe_allow_html=True)
        messages.chat_message("assistant").markdown(f"##### Result:\n\n{result}", unsafe_allow_html=True)
        
        if len(r["queryresult"]["pods"][1]["subpods"] ) > 1:
            messages.chat_message("assistant").markdown(f"##### Possible steps to solution:\n\n{steps}", unsafe_allow_html=True)
    
    except:
        messages.chat_message("assistant").markdown("Sorry, please ask only math questions🌚", unsafe_allow_html=True)
            