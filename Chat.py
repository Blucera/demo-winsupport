import streamlit as st

from core import is_domain_allowed
from core.session_manager import SessionManager
from core.rag_pipeline import RAGPipeline
from core.chat_model import ChatModel
from core.embedding_manager import EmbeddingManager

resp = is_domain_allowed()
if not resp[0]:
    st.error("This app is not allowed on this domain.")
    st.stop()

st.header("Customer Support")
st.caption("Your personal chatbot trained on your uploaded data!")

if "session_manager" not in st.session_state:
    st.session_state.session_manager = SessionManager()

if "rag_pipeline" not in st.session_state:
    chat_model = ChatModel(session_manager=st.session_state.session_manager)
    st.session_state.rag_pipeline = RAGPipeline(EmbeddingManager(), chat_model)

# Display chat history
for obj in st.session_state.session_manager.get_history():
    with st.chat_message(obj["role"]):
        st.markdown(obj["content"])

if user_input := st.chat_input("Type your message..."):
    st.session_state.session_manager.add_message(user_input, "user")
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""

        for chunk in st.session_state.rag_pipeline.ask_v2(user_input):
            full_response += chunk
            response_placeholder.markdown(full_response)

        # Save full response in history
        st.session_state.session_manager.add_message(full_response, "assistant")
