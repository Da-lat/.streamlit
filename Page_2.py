import streamlit as st
from PyPDF2 import PdfReader
import google.generativeai as genai
import config

# Gemini config
api_key = config.API_KEY
genai.configure(api_key=api_key)
model = genai.GenerativeModel(config.MODEL)

st.markdown("# PDF Analysis ❄️")
st.sidebar.markdown("# PDF Analysis ❄️")
st.sidebar.markdown("Here you can upload a PDF file and analyse the text contents into key points to save time and make it more readable.")

if 'pdf' not in st.session_state:
    st.session_state['pdf'] = False
    st.session_state['text'] = None
    st.session_state['summary'] = None

def extract_text_from_pdf(pdf): 
    pdf_reader = PdfReader(pdf) 
    return ''.join(page.extract_text() for page in pdf_reader.pages)

def change_state():
    st.session_state['pdf'] = True

uploaded_file = st.file_uploader("Upload a PDF file to analyse the text contents", type="pdf", on_change=change_state)

button = st.button("Analyse")

# creating a pdf file object 
try:
    if uploaded_file and button and st.session_state.pdf == True:
        text = extract_text_from_pdf(uploaded_file)
        # st.write(text)
        response = model.generate_content("Here is a PDF file, please summarize the file into bullet points and provide a summary, act as if you are studying and you went through the file and took notes to learn and extract the key points. Here is the file: " + text)
        st.session_state.text = response.text
        st.session_state.summary = None
except:
    st.error("Invalid file, please try again")

if st.session_state.text:
    st.write(st.session_state.text)

q = st.text_input("Do you have any questions about the PDF?")
button = st.button("Ask")

if q and st.session_state.text and button:
    response = model.generate_content(f"I am providing an extracted text passage from a pdf file, please search this information and answer this question. PDF text: {st.session_state.text}. Question: {q}")
    st.session_state.summary = response.text

if st.session_state.summary:
    st.write(st.session_state.summary)
