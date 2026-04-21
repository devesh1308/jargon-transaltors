# frontend/app.py
# ClauseGuard Frontend - Day 1 Version

import streamlit as st
import requests
import time

# Page setup
st.set_page_config(
    page_title="ClauseGuard",
    page_icon="🔒",
    layout="wide"
)

# Title
st.title("🔒 ClauseGuard")
st.caption("Analyze your rental agreement • 100% Offline • Private")

# Sidebar
with st.sidebar:
    st.markdown("### 📊 Analysis Settings")
    st.markdown("---")
    st.markdown("### 🔒 Privacy Notice")
    st.info("All analysis happens on your device. Nothing is sent to the cloud.")

# Main content
st.markdown("### 📄 Upload Your Document")

# File uploader
uploaded_file = st.file_uploader(
    "Choose a PDF file",
    type="pdf",
    help="Select your rental agreement PDF"
)

if uploaded_file is not None:
    st.success(f"✅ File uploaded: {uploaded_file.name}")
    
    with st.spinner("🔍 Analyzing document..."):
        time.sleep(2)
    
    # Mock data for testing
    mock_results = [
        {
            "original_text": "Tenant is responsible for all repairs including major structural damage.",
            "risk": "Predatory",
            "translation": "RED FLAG: This makes you responsible for the landlord's property."
        },
        {
            "original_text": "Security deposit will be returned within 30 days.",
            "risk": "Safe",
            "translation": "This clause appears standard."
        }
    ]
    
    # Display metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🔴 Predatory", "1")
    with col2:
        st.metric("🟡 Caution", "0")
    with col3:
        st.metric("🟢 Safe", "1")
    
    # Display clauses
    st.markdown("---")
    st.markdown("### 📝 Clause-by-Clause Analysis")
    
    for i, clause in enumerate(mock_results, 1):
        if clause["risk"] == "Predatory":
            emoji = "🔴"
        elif clause["risk"] == "Caution":
            emoji = "🟡"
        else:
            emoji = "🟢"
        
        with st.expander(f"{emoji} Clause {i}: {clause['original_text'][:50]}..."):
            st.markdown(f"**Original Text:**")
            st.text(clause["original_text"])
            st.markdown(f"**Risk Level:** {clause['risk']}")
            st.markdown(f"**Translation:**")
            st.info(clause["translation"])

else:
    st.markdown("""
    ---
    ### 👋 Welcome to ClauseGuard!
    
    **How it works:**
    1. 📤 Upload your rental agreement (PDF)
    2. 🔍 We analyze it completely offline
    3. 🚨 Risky clauses are highlighted
    4. 📧 Generate professional response emails
    
    **Your privacy is guaranteed** - no data leaves your device.
    """)

st.markdown("---")
st.caption("🔒 ClauseGuard MVP • All analysis happens locally")