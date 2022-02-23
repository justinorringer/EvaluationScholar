import React, { useEffect, useState } from "react";
import axios from 'axios';

function Input() {
  const [getMessage, setGetMessage] = useState({})
  
  //Base file reading works!
  
  let fileInput = null;
  let titles = [];

  let data = {
    name: "",
    institution: ""
  }

  function upload(){
    //console.log(document.getElementById("authName").value);

    let test = document.getElementById('myfile')
    fileInput = test.files[0];
    //console.log(fileInput)

    var fr = new FileReader();

    fr.addEventListener("load", () => {
      fileInput = fr.result;
      //Branch to handle different operating system line endings (Windows v. Linux)
      if(fileInput.includes("\r")){
        titles = fileInput.split("\r\n");
      } else {
        titles = fileInput.split("\n");
      }
      const titleList = document.getElementById("titleList");
      const fullsend = async () => {
        const authorId = await makeAuthor();
        console.log(authorId);
        for (const title of titles) {
          try {
            const paper = await getScrapedPaper(title);
            console.log(paper);
            const paperId = await postPaper(paper, title);
            console.log(paperId);
            await postCitation(paperId, paper);
            await joinAuthorToPaper(paperId, authorId);
            await joinPaperToAuthor(paperId, authorId);
            var titleItem = document.createElement("li");
            titleItem.className = "list-group-item list-group-item-success";
            titleItem.innerText = title + ": Added successfully!"
            titleList.appendChild(titleItem);
          } catch (e) {
            var titleItem = document.createElement("li");
            titleItem.className = "list-group-item list-group-item-danger";
            titleItem.innerText = title + ": Failed to add!"
            titleList.appendChild(titleItem);
          }
        }
        document.getElementById("success").style = "display: block !important"
      }

      fullsend();

    }, false);

    //This call activates the listener, and helps it to parse the file.
    fr.readAsText(fileInput);
  }

  //Example function to gather from Flask
  const makeAuthor = async () => {
    // try {
      const response = await axios({
        method: "post",
        url: '/api/authors',
        headers: {
          'Access-Control-Allow-Origin': '*',
          'Content-Type': 'application/json',

        },
      
        //make sure to serialize your JSON body
        data: JSON.stringify({
          name: document.getElementById("authName").value,
        }), mode: 'cors'
      }, true);      
      
      console.log(response);
      const data = await response.data;
      //setGetMessage({response, data})
      return data.id;
    // }
    // catch (e) {
      // console.log(e)
      // return null;
    // }
  }

  const getScrapedPaper = async (paperTitle) => {
    // try {
        const response = await axios.get(`/api/scraping/papers?title=${paperTitle}`, {
            mode:'cors'});
        if (response.status === 200) {
          console.log(response);
          return response.data;
        }
    // }
    // catch (e) {
        // console.log(e.getMessage);
    // }
  }

  const postPaper = async (paper, title) => {
    // try {
      const response = await axios({
        method: "post",
        url: '/api/papers',
        headers: {
          'Access-Control-Allow-Origin': '*',
          'Content-Type': 'application/json',

        },
      
        //make sure to serialize your JSON body
        data: JSON.stringify({
          name: title,
          year: paper.year
        }), mode: 'cors'
      }, true);      
      
      console.log(response);
      const data = await response.data;
      //setGetMessage({response, data})
      return data.id;
    // }
    // catch (e) {
      // console.log(e)
    // }
  }

  const postCitation = async (paperId, paper) => {
    // try {
      const response = await axios({
        method: "post",
        url: `/api/papers/${paperId}/citations/${paper.citation_count}`,
        headers: {
          'Access-Control-Allow-Origin': '*',
          'Content-Type': 'application/json',

        },
        mode: 'cors'
      }, true);      
      
      console.log(response);
    // }
    // catch (e) {
      // console.log(e)
    // }
  }

  const joinAuthorToPaper = async (paperId, authorId) => {
    // try {
      const response = await axios({
        method: "put",
        url: `/api/papers/${paperId}/authors/${authorId}`,
        headers: {
          'Access-Control-Allow-Origin': '*',
          'Content-Type': 'application/json',

        },
        mode: 'cors'
      }, true);      
      
      console.log(response);
    // }
    // catch (e) {
      // console.log(e)
    // }
  }

  const joinPaperToAuthor = async (paperId, authorId) => {
    // try {
      const response = await axios({
        method: "put",
        url: `/api/authors/${authorId}/papers/${paperId}`,
        headers: {
          'Access-Control-Allow-Origin': '*',
          'Content-Type': 'application/json',

        },
        mode: 'cors'
      }, true);      
      
      console.log(response);
    // }
    // catch (e) {
      // console.log(e)
    // }
  }


  return (
    <div className="body">
      <div className="container pt-5">
        <div className="row">
            <div className="alert alert-success alert-dismissible" role="alert" id="success" style={{display: "none"}}>
                <button className="close" type="button" data-dismiss="alert"><span>&times;</span></button> Articles done scraping
            </div>
        </div>
        <div className="row">
          <label>Author name: &nbsp;</label>
          <input type="text" id="authName"></input> 
        </div>
        <div className="row">
            <div className="justify-content-center page-header">Upload File <small>as a .CSV or .TXT file</small></div>
            <br/><br/>
        </div>
        <div className="row">
                <label for="myfile">Select a file:&nbsp;</label>
                <input type="file" id="myfile" name="myfile"/>
                <input type="submit" onClick={upload}/>
        </div>
      </div>
      <div className="container">
        <ul className="list-group" id="titleList">
        </ul>
      </div>
    </div>
    
  );
}

export default Input;