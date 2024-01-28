import os
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv, dotenv_values 

load_dotenv()
app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with your frontend URL
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

class Chat(BaseModel):
    question: str

chats = []

@app.get("/chats/", response_model=List[Chat])
async def read_tasks():
    return chats

@app.post("/chats/")
async def create_response(question: Chat):
    prompt = ChatPromptTemplate.from_template("Answer the following question to the best of your ability: {question}")
    model = ChatOpenAI()
    output_parser = StrOutputParser()
    chain = prompt | model | output_parser

    # response = chain.invoke({"question": question})
    # print(response)
    # return response
    async for chunk in chain.astream({"question": question}):
        print(chunk)









