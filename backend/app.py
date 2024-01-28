import os
from fastapi import FastAPI, WebSocket
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

class ConnectionManager:
    """Class defining socket events"""
    def __init__(self):
        """init method, keeping track of connections"""
        self.active_connections = []
    
    async def connect(self, websocket: WebSocket):
        """connect event"""
        await websocket.accept()
        self.active_connections.append(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        """Direct Message"""
        await websocket.send_text(message)
    
    def disconnect(self, websocket: WebSocket):
        """disconnect event"""
        self.active_connections.remove(websocket)

manager = ConnectionManager()

@app.websocket("/chats")
async def create_response(websocket: WebSocket):
    await manager.connect(websocket)
    prompt = ChatPromptTemplate.from_template("Answer the following question to the best of your ability: {question}")
    model = ChatOpenAI()
    output_parser = StrOutputParser()
    chain = prompt | model | output_parser

    try:
        while True:
            data = await websocket.receive_text()

            async for chunk in chain.astream({"question": data}):
                await manager.send_personal_message(chunk,websocket)
    except websockets.exceptions.WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.send_personal_message("Bye!!!",websocket)





    # response = chain.invoke({"question": question})
    # print(response)
    # return response










