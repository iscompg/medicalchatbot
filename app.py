from flask import Flask, render_template, jsonify, request
from src.helper import donwload_embeddings
from langchain_pinecone import PineconeVectorStore
from langchain_groq import ChatGroq
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from src.prompt import *
import os 
from dotenv import load_dotenv

app =Flask(__name__, template_folder='templates')


load_dotenv()

PINECONE_API_KEY= os.getenv("PINECONE_API_KEY")
GROQ_API_KEY=os.getenv("GROQ_API_KEY")

embeddings= donwload_embeddings()

index_name="medical-chatbot" 

docsearch = PineconeVectorStore.from_existing_index(
    index_name=index_name,
    embedding=embeddings
)


retriever=docsearch.as_retriever(search_type= "similarity", search_kwargs={"k":3}) #return 3 releavmt responses

chatmodel= ChatGroq(model="llama-3.1-8b-instant",
                    temperature=0.3
                    )

prompt= ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
    ]
)

question_answer_chain= create_stuff_documents_chain(chatmodel, prompt)
rag_chain= create_retrieval_chain(retriever, question_answer_chain)



@app.route('/')
def index():
    return render_template('frontpage.html')

@app.route('/get', methods=['POST'])
def chat():
    data = request.get_json()
    msg=data["message"]
    print(msg)
    response=rag_chain.invoke({"input": msg})
    
    return jsonify({
        "response": response["answer"]
                })
    
    
    
if __name__=='__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)
