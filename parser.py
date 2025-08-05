import streamlit as st
from config import GEMINI_API_KEY, MODEL_ID
from google import genai
from google.genai import types

st.title("LLM Resume Q&A App")
st.write("Upload one or more resume PDFs and ask questions!")

uploaded_files = st.file_uploader("Upload Resume PDFs", type=["pdf"], accept_multiple_files=True)
question = st.text_input("Ask a question about the resumes:")

if uploaded_files and question:
    client = genai.Client(api_key=GEMINI_API_KEY)
    system_prompt_qa = ("""Act as a Q&A bot on uploaded resumes to help fill job applications. """
                        "Be very clear and say 'I do not know' if you do not know the answer or can't back up with solid proof from the given resume pdfs.")
    chat_config = types.GenerateContentConfig(system_instruction=system_prompt_qa)
    chat = client.chats.create(model=MODEL_ID, config=chat_config)

    pdf_parts = []
    for file in uploaded_files:
        pdf_bytes = file.read()
        pdf_parts.append(types.Part.from_bytes(data=pdf_bytes, mime_type='application/pdf'))

    pdf_parts.append(question)
    response = chat.send_message(pdf_parts)
    st.markdown(response.text)