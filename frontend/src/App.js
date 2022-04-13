import logo from './logo.svg';
import './App.css';
import React, { useEffect, useState } from 'react';

import { red } from '@mui/material/colors'
import { createTheme, ThemeProvider, styled } from '@mui/material/styles';

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

const theme = createTheme({
  palette: {
    primary: {
      main: '#CC0000',
    }
  },
  typography: {
    fontFamily: [
      "Josefin Sans",
      "sans-serif"
    ].join(",")
  }
});


function App() {
  return (
    <ThemeProvider theme={theme}>
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
      </Router>
    </ThemeProvider>
  )
}

export default App;
