from dotenv import load_dotenv
import os 
from pinecone import Pinecone
from pinecone import ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from src.helper import load_pdf_files, filter_to_minimal_docs, text_split, donwload_embeddings



load_dotenv("/Users/ishaniarora/medicalchatbot/.env")

PINECONE_API_KEY= os.getenv("PINECONE_API_KEY")
GROQ_API_KEY=os.getenv("GROQ_API_KEY")


extracted_data=load_pdf_files(data='data/')
filter_data= filter_to_minimal_docs(extracted_data)
text_chunk= text_split(filter_data)
embeddings=donwload_embeddings()

pc=Pinecone(api_key=PINECONE_API_KEY)

index_name="medical-chatbot"  

if not pc.has_index(index_name):
    pc.create_index(
        name=index_name, 
        dimension= 384,   #dimension of embeddings
        metric= "cosine",   #cosine similarity
        spec= ServerlessSpec(cloud="aws", region="us-east-1")
    )
    
index= pc.Index(index_name)



def push_records(index_name, embeddings, text_chunk=None):
#push records - do not run again if run once 

    if text_chunk is not None:
        docsearch = PineconeVectorStore.from_documents(
            documents=text_chunk,
            embedding=embeddings,
            index_name=index_name
        )
        print("adding new text")
        
    else:
        #if data is already existing in the index then run this

        docsearch = PineconeVectorStore.from_existing_index(
            index_name=index_name,
            embedding=embeddings
        ) 
        print("text updated already")
        
    return docsearch


records= push_records(index_name, embeddings)