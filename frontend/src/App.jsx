import React, { useState, useEffect } from 'react';
import axios from 'axios';

function App() {
  const [question, setQuestion] = useState("");
  const [response, setResponse] = useState("");
  const [chat, setChat] = useState([{ question: '', response: '' }]);
  const [isLoading, setIsLoading] = useState(true)
  const [isButtonClicked, setIsButtonClicked] = useState(false)

  useEffect(() => {
    axios.get('http://localhost:8000/chats/')
      .then(response => {
        setResponse(response.data)
      })
      .catch(error => {
        console.error('Error fetching tasks:', error);
      });
  }, []);

  const handleInputChange = event => {
    const { name, value } = event.target;
    setQuestion(value);
  };

  const handleSubmit = async (event) => {
    setIsButtonClicked(true)
    event.preventDefault();
    try {
      const response = await axios.post('http://localhost:8000/chats/', { question: question });
      console.log(response.data); // Handle response from backend
      setResponse(response.data)
      setIsLoading(false)
    } catch (error) {
      console.error('Error sending input to backend:', error);
    }
  };

  return (
    <div>
      <h1>Chat With Me</h1>
      <form onSubmit={handleSubmit}>
        <input type="text" name="question" value={question["question"]} onChange={handleInputChange} placeholder="Question" />
        <button type="submit">Click Me</button>
      </form> 
      {isButtonClicked && isLoading ? <p>Loading...</p> : <p>{response}</p>}
    </div>
  );
}

export default App;
