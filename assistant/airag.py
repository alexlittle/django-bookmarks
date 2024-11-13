import os
import ssl
import http
import requests
import socket
from urllib import error
import urllib3

from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_core.runnables import RunnablePassthrough
from langchain_chroma import Chroma
from langchain_ollama.llms import OllamaLLM
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import PromptTemplate
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from notes.models import Note

os.environ['USER_AGENT'] = 'Alex Laptop'
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class NotesAssistant():

    vs = None
    llm = None
    llm_model = "llama3.2:latest"
    collection_name = "notes"
    embedding_model = "sentence-transformers/all-mpnet-base-v2"
    vs_data_dir = os.path.join(BASE_DIR, "vs-data")
    chunk_size = 1000
    chunk_overlap = 200

    def __init__(self):
        self.vs = Chroma(
            collection_name=self.collection_name,
            embedding_function=HuggingFaceEmbeddings(model_name=self.embedding_model),
            persist_directory=self.vs_data_dir
        )

    def load_url(self,url):
        try:
            loader = WebBaseLoader(web_paths=(url,), )
            docs = loader.load()
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap)
            splits = text_splitter.split_documents(docs)

            return True, splits
        except (ssl.CertificateError,
                http.client.RemoteDisconnected,
                ConnectionResetError,
                socket.timeout,
                http.client.BadStatusLine,
                error.URLError,
                error.HTTPError,
                requests.exceptions.ConnectTimeout,
                socket.gaierror,
                urllib3.exceptions.NameResolutionError,
                urllib3.exceptions.ProtocolError,
                requests.exceptions.ConnectionError):
            print("failed to connect to {}".format(url))
            return False, None

    def init_chat(self):
        self.llm = OllamaLLM(model=self.llm_model, temperature=0)

    def pre_populate(self):
        # get all urls
        notes = Note.objects.all().exclude(url__isnull=True).exclude(url__exact='')
        for note in notes:
            print(note.url)
            self.add_note(note.url)

    def add_note(self, url):
        note = Note.objects.get(url=url)
        if not note.assistant_loaded:
            print("Adding: {}".format(url))
            success, splits = self.load_url(url)
            if success:
                self.vs.add_documents(splits)
                print("added")
                note.assistant_loaded = True
                note.save()
        else:
            print("Already added {}".format(url))

    def get_prompt_template(self, template):
        template_file = os.path.join(BASE_DIR,'prompttemplates/') + template + ".txt"
        with open(template_file, 'r') as file:
            return file.read()

    def format_docs(self, docs):
        return "\n\n".join(doc.page_content for doc in docs)

    def query(self, question, template='recommend'):

        rag_prompt = PromptTemplate.from_template(self.get_prompt_template(template))

        retriever = self.vs.as_retriever(search_kwargs={"k": 10})

        rag_chain = (
                {"context": retriever | self.format_docs, "question": RunnablePassthrough()}
                | rag_prompt
                | self.llm
                | StrOutputParser()
        )

        return rag_chain.invoke(question)