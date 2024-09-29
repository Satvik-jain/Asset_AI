from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders import UnstructuredURLLoader
import langchain_community.vectorstores
from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import requests
from bs4 import BeautifulSoup


class Rag_Pipeline():
    def __init__(self):
        load_dotenv()
        self.docs = None
        self.docsearch = None
        self.embed()

    def chunking(self):
        text_splitter = RecursiveCharacterTextSplitter(
                        chunk_size=1000,
                        chunk_overlap=600
                    )
        
        loader = DirectoryLoader('knowledge_base', glob="*.pdf", show_progress=True, use_multithreading=True)
        data = loader.load()
        docs = text_splitter.split_documents(data)
        
        url = "https://zerodha.com/varsity/module/sector-analysis/"
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        containers = soup.find_all("div", class_="container")
        href_links = []
        for container in containers:
            a_tags = container.find_all("a", class_="inv", href=True)
            for a_tag in a_tags:
                href_links.append(a_tag['href'])

        url_loader = UnstructuredURLLoader(urls = href_links, show_progress_bar = True)
        url_data = url_loader.load()
        url_docs = text_splitter.split_documents(url_data)

        self.docs = docs + url_docs

    def embed(self):
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        pc = Pinecone(api_key=os.environ.get("PINECONE_API_KEY"))
        index_name = "asset-ai"
        if index_name not in pc.list_indexes().names():
            pc.create_index(name=index_name,
                            metric="cosine",
                            dimension=768,
                            spec=ServerlessSpec(
                                cloud="aws",
                                region="us-east-1"
                        ))
            self.docsearch = langchain_community.vectorstores.Pinecone.from_documents(self.docs, embeddings, index_name=index_name)
        else:
            self.docsearch = langchain_community.vectorstores.Pinecone.from_existing_index(embedding=embeddings, index_name=index_name)

    def parse_query():
        pass
