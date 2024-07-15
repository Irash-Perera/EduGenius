import json
import streamlit as st
import requests
import os
import urllib.parse
from env import WOLFRAM_APP_ID, LANGFUSE_SECRET_KEY, LANGFUSE_PUBLIC_KEY, LANGFUSE_HOST
from langfuse import Langfuse
from langfuse.decorators import observe

 
os.environ["LANGFUSE_SECRET_KEY"] = LANGFUSE_SECRET_KEY
os.environ["LANGFUSE_PUBLIC_KEY"] = LANGFUSE_PUBLIC_KEY
os.environ["LANGFUSE_HOST"] = LANGFUSE_HOST

st.header("Have a math problem?")
st.subheader(" Let's solve it :red[_step-by-step_]💡", divider= 'red')

@observe(capture_input=True, capture_output=True)
def get_wolframalpha_response(prompt):
    appid = os.getenv('WA_APPID', WOLFRAM_APP_ID )
    query = urllib.parse.quote_plus(f"solve {prompt}")
                        
    query_url = f"http://api.wolframalpha.com/v2/query?" \
                f"appid={appid}" \
                f"&input={query}" \
                f"&podstate=Result__Step-by-step+solution" \
                "&format=mathml" \
                f"&output=json"
    
    r = requests.get(query_url).json()
    # with open('data.json', 'w') as json_file:
    #     json.dump(r, json_file)
      
    response = r["queryresult"]
    return response



if st.session_state["authentication_status"]:
    col1, col2 = st.columns(2)
    with col1:
        messages = st.container(height=350)

    with col2:
        tips = st.container(height=350)
        tips.markdown("""
            <div style="background-color: #0E1117; border-radius: 10px; padding: 20px; height: 300px; box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.1);">
                <h5 style="text-align: left;">Don't get the answer as expected? Here are some tips🤖:</h5>
                <ul style="margin-left: 20px;">
                    <li>Make sure you ask a math question</li>
                    <li>Add these keywords to your question according to your needs:
                        <ul>
                            <li><strong>solve</strong> : for solving equations</li>
                            <li><strong>factor</strong> : for factorizing expressions</li>
                            <li><strong>simplify</strong> : for simplifying expressions</li>
                            <li><strong>compute</strong> : for computing values</li>
                        </ul>
                    </li>
                    <li>If you are still stuck, try asking the question in a different way</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
        
    prompt = st.chat_input("Ask your math question here")
    if prompt:
        response = get_wolframalpha_response(prompt)
        markdown_text = ""
        for pod in response["pods"]:
            
            has_content = False
            for subpod in pod["subpods"]:
                if "mathml" in subpod:
                    has_content = True
            if has_content:
                markdown_text += f"###### {pod['title']}\n\n"
                for subpod in pod["subpods"]:
                    if "mathml" in subpod:
                        markdown_text += f"\n{subpod['mathml']}\n\n"
            has_content = False
                    
        messages.chat_message("user").markdown(prompt, unsafe_allow_html=True)
        messages.chat_message("assistant").markdown(f"##### Result:\n\n{markdown_text}", unsafe_allow_html=True)
                
    
                
else:
    st.header("You need to login to access this :red[_feature_]🔒")
    st.page_link("home.py", label="Click here to login", icon=":material/lock_open:", use_container_width=True)