import streamlit as st
from PyPDF2 import PdfReader

from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from langchain.document_loaders import YoutubeLoader
from apikey import geminiai_api_key
apikey = geminiai_api_key
from youtube_transcript_api import YouTubeTranscriptApi

os.environ["GOOGLE_API_KEY"] = geminiai_api_key

genai.configure(api_key=apikey)


def get_video_text(video_url):
    try:
        video_id = video_url.split("=")[1]
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)

        transcript = ""
        for i in transcript_text:
            transcript += " " +i['text']

        return transcript

    except Exception as e:
        raise e
def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text+=page.extract_text()
    return text

def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=50)
    chunks = text_splitter.split_text(text)
    return chunks
def get_vector_store(text_chunks):
    embeddings= GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_store = FAISS.from_texts(text_chunks,embedding=embeddings)
    vector_store.save_local("faiss_index")

def get_conversational_chain():
    prompt_template = '''Answer the question as detailed as possible from the provided context, make sure to provide all the details.
    Context:\n {context}?\n
    Question: \n{question}\n

    Answer:
    '''
    model = ChatGoogleGenerativeAI(model="gemini-pro",temperature=0.3)

    prompt = PromptTemplate(template = prompt_template,input_variables = ['context','questions'])
    chain = load_qa_chain(model,chain_type="stuff",prompt=prompt)

    return chain

def user_input(user_question):
    embeddings = GoogleGenerativeAIEmbeddings(model= "models/embedding-001")

    new_db = FAISS.load_local("faiss_index",embeddings,allow_dangerous_deserialization=True)
    docs = new_db.similarity_search(user_question)

    chain = get_conversational_chain()

    response = chain({
        "input_documents":docs,"question":user_question
    },
    return_only_outputs=True)

    print(response)
    st.write("Reply : ",response["output_text"])

def main():
    st.set_page_config("Chat PDF")
    st.header("Chat with Youtube Video using Gemini💁")

    user_question = st.text_input("Ask a Question from the PDF Files")

    if user_question:
        user_input(user_question)

    with st.sidebar:
        st.title("Menu:")
        video_url = st.text_input("Upload the youtube video link here")
        if st.button("Submit & Process"):
            with st.spinner("Processing..."):
                raw_text = get_video_text(video_url)
                text_chunks = get_text_chunks(raw_text)
                get_vector_store(text_chunks)
                st.success("Done")



if __name__ == "__main__":
    main()
