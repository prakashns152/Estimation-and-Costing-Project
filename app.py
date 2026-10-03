import streamlit as st
import os
from dotenv import load_dotenv
from utils.vector_store import query_rates
import google.generativeai as genai

# Load environment variables securely from .env file
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY", "")

# Page Configuration (Centered chat layout like Gemini/ChatGPT)
st.set_page_config(
    page_title="Aishwaryam Group | Costing & Estimation Portal",
    page_icon="🏢",
    layout="centered"
)

# Custom Styling for Aishwaryam Branding
st.markdown("""
    <style>
    .header-title {
        color: #0A192F;
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 700;
        margin-bottom: 0px;
    }
    .sub-tag {
        color: #D4AF37;
        font-weight: 600;
        letter-spacing: 1px;
        text-transform: uppercase;
        font-size: 13px;
    }
    </style>
""", unsafe_allow_html=True)

# App Header
st.markdown('<p class="sub-tag">Aishwaryam Group | Engineering Division</p>', unsafe_allow_html=True)
st.markdown('<h1 class="header-title">Costing and Estimation Chatbot</h1>', unsafe_allow_html=True)
st.markdown("<p style='color: gray; margin-bottom: 20px;'>Your Senior Costing & Estimation Expert Agent (India Real Estate).</p>", unsafe_allow_html=True)

# Sidebar for Document Uploader (Keeps main chat area clean and full-width)
with st.sidebar:
    st.markdown("### 📂 Document Uploader")
    st.markdown("Upload any construction drawing, blueprint, or architectural PDF/Image.")
    
    uploaded_file = st.file_uploader("Choose a document file", type=["pdf", "png", "jpg", "jpeg"], label_visibility="collapsed")
    
    current_file_path = None
    
    if uploaded_file is not None:
        current_file_path = os.path.join(".", uploaded_file.name)
        with open(current_file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(f"Successfully uploaded: **{uploaded_file.name}**")
        
        if uploaded_file.type in ["image/png", "image/jpeg", "image/jpg"]:
            st.image(uploaded_file, caption="Uploaded Preview", use_column_width=True)
    else:
        if os.path.exists("Drawing.pdf"):
            current_file_path = "Drawing.pdf"
            st.info("Active Drawing: **Drawing.pdf**")

# Initialize Session State for Chat History
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I am your Senior Costing & Estimation Expert Agent (India Real Estate). Upload any construction drawing on the left sidebar, and ask me to calculate quantities and costs for any component!"}
    ]

# Render Full-Width Chat History (User right, Assistant left)
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat Input Box (Pinned automatically at the bottom after every answer)
if user_query := st.chat_input("Type your question here (e.g., 'Calculate cement quantity and cost')..."):
    if not API_KEY:
        st.error("Error: GEMINI_API_KEY is missing from your .env file configuration.")
    else:
        # Append and display user message
        st.session_state.messages.append({"role": "user", "content": user_query})
        with st.chat_message("user"):
            st.markdown(user_query)

        # Generate Assistant response
        with st.chat_message("assistant"):
            with st.spinner("Analyzing drawing dimensions and computing market rates..."):
                try:
                    # Retrieve rate benchmarks
                    docs, metas = query_rates(user_query, n_results=3)
                    rate_context = "\n".join(docs)
                    
                    client = genai.Client(api_key=API_KEY)
                    
                    file_ref = None
                    if current_file_path and os.path.exists(current_file_path):
                        file_ref = client.files.upload(file=current_file_path)
                    
                    chat_prompt = f"""
                    You are an elite Senior Costing and Estimation Engineer working in Indian Real Estate (Aishwaryam Group).
                    You have access to the uploaded construction drawing and the following market rate benchmarks:
                    {rate_context}
                    
                    Answer the user's question with 100% mathematical precision, showing step-by-step quantity takeoffs (such as area calculations, cement bags, steel quantity, painting volumes, or tile requirements) and calculate the total estimated cost in Indian Rupees (₹ / INR) based on current Indian market standards.
                    
                    User Question: {user_query}
                    """
                    
                    contents_payload = [file_ref, chat_prompt] if file_ref else [chat_prompt]
                    
                    response = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=contents_payload
                    )
                    answer = response.text
                    
                    st.markdown(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                    
                except Exception as e:
                    error_msg = f"An error occurred: {e}"
                    st.markdown(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})