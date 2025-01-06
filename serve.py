from fastapi import FastAPI
from dotenv import load_dotenv
import os
from langchain_groq import ChatGroq # loading model
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import langserve
from langserve import add_routes # helps to create APIs


load_dotenv()
os.environ["GROQ_API_KEY"]=os.getenv("GROQ_API_KEY")
groq_api_key = os.getenv("GROQ_API_KEY")

#creating a prompt template
generic_template = 'Only Translate the following into {language}:'
prompt = ChatPromptTemplate.from_messages(
    [
        ("system",generic_template),
        ("user", "{text}")
    ]
)

# creating a model
model = ChatGroq(model = "gemma2-9b-It", groq_api_key = groq_api_key)

# creating a string output parser
parser = StrOutputParser()

chain = prompt | model | parser


# App definition
app = FastAPI(title = "Langchain Server",
               version = "1.0",
               description = "A simple API server using Langchain Runnable server")

add_routes(
    app,
    chain,
    path = "/chain"
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host = "127.0.0.1", port = 8000)


# http://127.0.0.1:8000/docs#/
# postman