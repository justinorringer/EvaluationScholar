import logo from './logo.svg';
import './App.css';
import React, { useEffect, useState } from 'react';


function App() {
  const [getMessage, setGetMessage] = useState({})

  const makeAPICall = async () => {
    try {
      const response = await fetch('http://localhost/');
      const data = await response.json();
      //console.log({response, data})
      setGetMessage({response, data})
      console.log(getMessage.response.status)
    }
    catch (e) {
      console.log(e)
    }
  }
  useEffect(() => {
    makeAPICall();
  }, [])
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>React + Flask Tutorial</p>
        <div>{getMessage.status === 200 ? 
          <h3>{getMessage.data}</h3>
          :
          <h3>LOADING</h3>}</div>
      </header>
    </div>
  );
}

export default App;
