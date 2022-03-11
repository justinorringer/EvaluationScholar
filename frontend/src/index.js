import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import {
  Header,
  Footer,
  Query,
  Input,
  Issues,
  Jobs,
  Tags
} from "./components";


ReactDOM.render(
  <Router>
    <Header />
    <Routes>
      <Route path="/" element={<Query />} />
      <Route path="/input" element={<Input />} />
      <Route path="/issues" element={<Issues />} />
      <Route path="/jobs" element={<Jobs />} />
      <Route path="/tags" element={<Tags />} />
    </Routes>
    <Footer />
  </Router>,

  document.getElementById("root")
);
//ReactDOM.render(
  //<React.StrictMode>
    //<App />
  //</React.StrictMode>,
  //document.getElementById('root')
//);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
