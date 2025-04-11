import streamlit as st
from dotenv import load_dotenv
import os
from supply_chain_assistant import SupplyChainAssistant

# Load environment variables
load_dotenv()

# Set Streamlit page config
st.set_page_config(page_title="Supply Chain Assistant", layout="wide")

# Custom CSS styling
st.markdown("""
    <style>
    /* Chat message container */
    .chat-message {
        padding: 12px 20px;
        border-radius: 12px;
        margin-bottom: 10px;
        max-width: 90%;
        line-height: 1.6;
    }
    .chat-message.user {
        background-color: #e0f7fa;
        align-self: flex-end;
        margin-left: auto;
        font-weight: 500;
    }
    .chat-message.assistant {
        background-color: #f1f8e9;
        border-left: 4px solid #8bc34a;
        margin-right: auto;
    }

    .header {
        border-bottom: 2px solid #ddd;
        padding-bottom: 8px;
        margin-bottom: 20px;
    }

    .instructions {
        background-color: #f9f9f9;
        border-left: 5px solid #2196F3;
        padding: 16px;
        border-radius: 10px;
        margin-bottom: 20px;
    }

    </style>
""", unsafe_allow_html=True)

# Title and intro
st.markdown("<h1 class='header'>🔗 Supply Chain GraphRAG Assistant</h1>", unsafe_allow_html=True)
st.markdown("""
<div class="instructions">
    <strong>Welcome!</strong> Ask anything about your supply chain network. You may not ask any followup question. For example:
    <ul>
        <li>Find suppliers that deal with <em>steel</em> and have at least <strong>20000</strong> supply capacity.</li>
        <li>Find me manufacturers supply <em>electronics</em>. </li>
        <li>Find top 5 suppliers by capacity who deal with <em>plastic</em>.</li>
    </ul>
    🤖 This assistant combines <strong>graph knowledge</strong> and <strong>AI reasoning</strong> to get smart results!
</div>
""", unsafe_allow_html=True)

# Initialize assistant and messages
if "assistant" not in st.session_state:
    st.session_state.assistant = SupplyChainAssistant()

if "messages" not in st.session_state:
    st.session_state.messages = []

# Render past messages
for msg in st.session_state.messages:
    role = msg["role"]
    content = msg["content"]
    css_class = f"chat-message {role}"
    st.markdown(f"<div class='{css_class}'>{content}</div>", unsafe_allow_html=True)

# Prompt input
if prompt := st.chat_input("Ask your supply chain question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.markdown(f"<div class='chat-message user'>{prompt}</div>", unsafe_allow_html=True)

    for m in st.session_state.messages:
        print(f"MESSAGES {m}")


    try:
        with st.spinner("Analyzing your query..."):
            assistant_response = st.session_state.assistant.query(f"{prompt}")
            st.markdown(f"<div class='chat-message assistant'>{assistant_response}</div>", unsafe_allow_html=True)

        st.session_state.messages.append({"role": "assistant", "content": assistant_response})
    except: 
        request_not_processed = "Could not process the request, please try later...."
        st.markdown(f"<div class='chat-message assistant'>{request_not_processed}</div>", unsafe_allow_html=True)
        st.session_state.messages.append({"role": "assistant", "content": request_not_processed})