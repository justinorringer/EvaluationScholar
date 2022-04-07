import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import {
  Query,
  Issues,
  Tasks,
  Tags,
  Author,
  Papers,
  CreateAuthor,
  Visualize
} from "./pages";
import {
  Header,
  Footer
} from "./components";


ReactDOM.render(
  <Router>
    <Header />
    <Routes>
      <Route path="/" element={<Query />} />
      <Route path="/issues" element={<Issues />} />
      <Route path="/tasks" element={<Tasks />} />
      <Route path="/tags" element={<Tags />} />
      <Route path="/author/:id" element={<Author />} />
      <Route path="/papers" element={<Papers />} />
      <Route path="/createauthor" element={<CreateAuthor />} />
      <Route path="/visualize" element={<Visualize />} />
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