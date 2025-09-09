from dotenv import load_dotenv
import os
import streamlit as st
import google.generativeai as genai
import PyPDF2 # <-- ADDED: For reading PDF text
# REMOVED: PIL, pdf2image, io, base64 are no longer needed

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# MODIFIED: This function now accepts text instead of image data
def get_gemini_response(job_desc, resume_text, user_prompt):
    model = genai.GenerativeModel("gemini-1.5-pro") # Switched to a more efficient text model
    prompt = f"""
    Job Description:
    {job_desc}
    ---
    Resume Text:
    {resume_text}
    ---
    User's Request: {user_prompt}
    """
    response = model.generate_content(prompt)
    return response.text

# NEW FUNCTION: Replaces your old process_pdf function
def get_pdf_text(upload_file):
    try:
        pdf_reader = PyPDF2.PdfReader(upload_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        st.error(f"Error reading PDF: {e}")
        return None

# Configure Streamlit page
st.set_page_config(page_title="ATS Resume Expert", layout="wide")
st.title("🚀 Resume Analyzer :)")

# Create two columns
col1, col2 = st.columns(2)

# Input section in the left column
with col1:
    st.header("Input")
    job_desc = st.text_area("Paste Job Description Here")
    upload_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

    if upload_file:
        st.success("✅ Resume Uploaded Successfully")

# Output section in the right column
with col2:
    st.header("Output")
    if st.button("📄 Analyze Resume"):
        if not job_desc:
            st.warning("Please enter the job description.")
        elif not upload_file:
            st.warning("Please upload a resume in PDF format.")
        else:
            with st.spinner("Analyzing..."):
                # MODIFIED: Calling the new text extraction function
                resume_text = get_pdf_text(upload_file)
                if resume_text:
                    prompt = "Provide detailed feedback on this resume based on the job description."
                    response = get_gemini_response(job_desc, resume_text, prompt)
                    st.subheader("🔍 AI Feedback")
                    st.write(response)

    if st.button("📊 Resume & JD Matching Percentage"):
        if not job_desc:
            st.warning("Please enter the job description.")
        elif not upload_file:
            st.warning("Please upload a resume in PDF format.")
        else:
            with st.spinner("Calculating match score..."):
                # MODIFIED: Calling the new text extraction function
                resume_text = get_pdf_text(upload_file)
                if resume_text:
                    prompt = "Give a percentage score showing how well this resume matches the job description."
                    response = get_gemini_response(job_desc, resume_text, prompt)
                    st.subheader("🎯 Matching Score")
                    st.write(response)

    if st.button("💡 Suggest Improvements"):
        if not job_desc:
            st.warning("Please enter the job description.")
        elif not upload_file:
            st.warning("Please upload a resume in PDF format.")
        else:
            with st.spinner("Generating suggestions..."):
                # MODIFIED: Calling the new text extraction function
                resume_text = get_pdf_text(upload_file)
                if resume_text:
                    prompt = "Suggest improvements for the resume based on the job description."
                    response = get_gemini_response(job_desc, resume_text, prompt)
                    st.subheader("💡 Improvement Suggestions")
                    st.write(response)

st.markdown("---")