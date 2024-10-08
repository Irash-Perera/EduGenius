import json
import streamlit as st
import requests
import os
import urllib.parse
from dotenv import load_dotenv
# from env import WOLFRAM_APP_ID, LANGFUSE_SECRET_KEY, LANGFUSE_PUBLIC_KEY, LANGFUSE_HOST
from langfuse import Langfuse
from langfuse.decorators import observe, langfuse_context

load_dotenv()

 
# os.environ["LANGFUSE_SECRET_KEY"] = LANGFUSE_SECRET_KEY
# os.environ["LANGFUSE_PUBLIC_KEY"] = LANGFUSE_PUBLIC_KEY
# os.environ["LANGFUSE_HOST"] = LANGFUSE_HOST

st.subheader("Have a problem?")
st.subheader(" Let's solve it :red[_step-by-step_]💡", divider= 'red')

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



if st.session_state["authentication_status"]:
    col1, col2 = st.columns(2)
    with col1:
        messages = st.container(height=370)

    with col2:
        tips = st.container(height=370)
        tips.markdown("""
            <div style=" border-radius: 10px; padding: 20px; height: 300px; rgba(0, 0, 0, 0.1);">
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
                    <li>You can ask for proofs, definitions, and more</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)

    prompt = st.chat_input("Ask your math question here")
    answer="<h2> Here's what I found ✨:</h2>"
    if prompt:
        response = get_wolframalpha_response(prompt)
        
        for pod in response["pods"]:
            
            has_content = False
            # for subpod in pod["subpods"]:
            if "markup" in pod:
                has_content = True
            if has_content:
                answer+= pod["markup"]["data"]
            has_content = False
        answer+="""
        <style>
        h2{
            font-size: 1rem;
        }
        div{
            border:0px;
        }
        hr{
            margin:0px;
        }
        </style>
        """
                    
        messages.chat_message("user").markdown(prompt, unsafe_allow_html=True)
        messages.chat_message("assistant").html(f"{answer}")
             
    
                
else:
    st.header("You need to login to access this :red[_feature_]🔒")
    st.page_link("pages/home.py", label="Click here to login", icon=":material/lock_open:", use_container_width=True)