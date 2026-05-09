from langchain_community.document_loaders import PyMuPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List
from langchain_core.documents import Document
from langchain_community.embeddings import HuggingFaceEmbeddings



#Extract text from pdf files 

def load_pdf_files(data):
    loader=DirectoryLoader(
        data, 
        glob="*.pdf", 
        loader_cls= PyMuPDFLoader
    )
    
    documents= loader.load()
    return documents



# given a set of data return only source in the metadata and the original page content 
 
def filter_to_minimal_docs(docs: List[Document])-> List[Document]:
    ## returns only the source na dthe original content
    print(len(docs))
    print(type(docs))
    
    minimal_docs: List[Document]=[]
    for doc in docs:
        src= doc.metadata.get("source")
        minimal_docs.append(
            Document(
                page_content=doc.page_content, 
                metadata={"source":src}
            )
        )
    return minimal_docs



# split data into text chunks 

def text_split(minimal_docs):
    text_splitter=RecursiveCharacterTextSplitter(
        chunk_size= 500,
        chunk_overlap=20
    )
    
    texts_chunk= text_splitter.split_documents(minimal_docs)
    return texts_chunk



#download embedding model from hugging face

def donwload_embeddings():
    #download and return the hugging face embedding model
    
    model_name= "sentence-transformers/all-MiniLM-L6-v2"
    embeddings= HuggingFaceEmbeddings(
        model_name= model_name
    )
    
    return embeddings