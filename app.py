import streamlit as st
from src.orchestrator import run_orchestrator


st.set_page_config(
    page_title="SeShat - Cruise Assistant",
    page_icon="🚢",
    layout="centered"
)

r
st.title(" SeShat AI")
st.markdown("### Intelligent Egypt Cruise Assistant")
st.markdown("---")

# --- SIDEBAR CONTROLS ---
with st.sidebar:
    st.header("⚙️ Controls")
    if st.button("🗑️ Reset Conversation", type="primary"):
        st.session_state.messages = []
        st.rerun()
    
    st.markdown("""
    **capabilities:**
    - Find Cruises by Budget
    - Filter by Duration
    - Compare Nile vs Red Sea
    - ℹAnswer Safety & FAQ
    """)


#Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Welcome! I can help you find the perfect Egypt cruise. Try asking: \n\n*\"Find a 5-day luxury Nile cruise under $1500\"*"}
    ]

#Display Previous Messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

#Handle User Input
if prompt := st.chat_input("Ask about cruises, prices, or itineraries..."):
    
    #Display User Message
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
)
    with st.chat_message("assistant"):
        with st.spinner(" Analyzing Request..."):
            try:
               
                response = run_orchestrator(prompt)
                st.markdown(response)
            except Exception as e:
                error_msg = f" System Error: {str(e)}"
                st.markdown(error_msg)
                response = error_msg
                
    #Save Assistant Response
    st.session_state.messages.append({"role": "assistant", "content": response})