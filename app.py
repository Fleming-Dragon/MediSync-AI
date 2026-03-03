import streamlit as st
import base64
from PIL import Image
from dotenv import load_dotenv

# Import our custom modules
from agent import build_medical_agent, analyze_image

load_dotenv()

# Page Setup
st.set_page_config(page_title="MediSync AI - Agentic System for Diagnosis", layout="wide")
st.title("🩺 ❉ MediSync AI - Agentic System for Diagnosis")

# Initialize Agent
if "agent" not in st.session_state:
    st.session_state.agent = build_medical_agent()

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []


if "uploader_key" not in st.session_state:
    st.session_state["uploader_key"] = 0


# SIDEBAR (INPUT)
with st.sidebar:
    st.info(
        "**Disclaimer** : \n"
        "This tool is a decision aid for healthcare professionals."
        "It does not replace an official medical diagnosis."
    )
    st.markdown("---")
    st.subheader("📁 Patient Data")
    uploaded_file = st.file_uploader(
        "Upload Medical Imaging (X-Ray/MRI)", 
        type=["jpg", "png", "jpeg"],
        key=str(st.session_state["uploader_key"])
    )
    if st.button("Clear Session"):
        st.session_state.messages = []
        st.rerun()
    st.markdown("---")


# DISPLAY CHAT HISTORY
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "image" in message:
            st.image(message["image"], width=200)
        if "source" in message:
            # Display a small badge showing where the info came from
            st.caption(f"Source: {message['source']}")

# MAIN LOGIC LOOP
if prompt := st.chat_input("Enter clinical query..."):
    
    # 1. Display User Message
    user_msg_data = {"role": "user", "content": prompt}
    
    if uploaded_file:
        image = Image.open(uploaded_file)
        user_msg_data["image"] = image # Store for display
        
        # Prepare Vision Context immediately
        uploaded_file.seek(0)
        b64_image = base64.b64encode(uploaded_file.read()).decode("utf-8")
        image_data_url = f"data:image/jpeg;base64,{b64_image}"
        
        with st.spinner("Analyzing image features..."):
            # Call the vision function from agent.py
            image_description = analyze_image(image_data_url)
            
        # Enrich the prompt for the Agent
        full_query = f"User Question: {prompt}\n\nClinical Image Analysis: {image_description}"
    else:
        full_query = prompt

    st.session_state.messages.append(user_msg_data)
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)
        if uploaded_file:
            st.image(image, width=200)
            

    # 2. Run Agent
    with st.chat_message("assistant", avatar="🩺"):
        with st.spinner("Agent processing (Retrieving -> Grading -> Thinking)..."):
            try:
                # Invoke the graph defined in agent.py
                result = st.session_state.agent.invoke({"question": full_query})
                answer = result["answer"]
                source = result.get("source", "unknown").upper()
                
                # Display Result
                st.markdown(answer)
                if source == "WEB":
                    st.caption("🌐 Source: External Web Search")
                elif source == "PDF":
                    st.caption("📄 Source: Internal Knowledge Base")
                
                # Save to History
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": answer,
                    "source": source
                })
                
            except Exception as e:
                st.error(f"System Error: {e}")
                
        if uploaded_file:
            st.session_state["uploader_key"] += 1
            st.rerun()