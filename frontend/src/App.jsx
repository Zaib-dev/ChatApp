import React, { useState, useEffect } from 'react';
import axios from 'axios';

function App() {
  const [question, setQuestion] = useState("");
  const [response, setResponse] = useState("");
  const [chat, setChat] = useState([{ question: '', response: '' }]);
  const [isLoading, setIsLoading] = useState(false)
  const [isButtonClicked, setIsButtonClicked] = useState(false)
  const [socket, setSocket] = useState(null);


  useEffect(() => {
    const ws = new WebSocket('ws://localhost:8000/chats');
    setSocket(ws);

    ws.onopen = () => {
      console.log('WebSocket connected');
    };

    ws.onmessage = (event) => {
      const response = event.data;
      console.log(response)
      setResponse((previousResponse) => `${previousResponse}${response}`);
      setIsLoading(false)
      setIsButtonClicked(false)
    };

    ws.onclose = () => {
      console.log('WebSocket closed');
    };

    return () => {
      if (ws) {
        ws.close();
      }
    };
  }, []);

  const handleInputChange = event => {
    const { value } = event.target;
    setQuestion(value);
  };

  const handleSubmit = async (event) => {
    setResponse("")
    setIsButtonClicked(true)
    event.preventDefault();
    if (!socket) {
      console.error('WebSocket connection not established');
      return;
    }
    socket.send(question);
  };

  return (
    <div>
      <h1>Chat With Me</h1>
      <form onSubmit={handleSubmit}>
        <input type="text" name="question" value={question["question"]} onChange={handleInputChange} placeholder="Question" />
        <button type="submit">Click Me</button>
      </form> 
      {isButtonClicked | isLoading ? <p>Loading...</p> : <p>{response}</p>}
    </div>
  );
}

export default App;
