import React from "react";
import axios from 'axios';

//Function to create an HTML representation for the Input page of the app.
//Authors: Gage Fringer, Carter Thunes, Justin Orringer
function Input() {
  //Variable to hold data from a file selected to be read in.
  let fileInput = null;
  //Variable to handle holding titles of papers for parsing/messages
  let titles = [];

  //Object to hold the data getting pulled, both a name string and institution string

  //Method to handle the upload of a file
  //and also call other functions necessary for this page
  function upload(){
    //Pull the value of the file being input
    let test = document.getElementById('myfile')
    fileInput = test.files[0];
    //Create a variable to read it
    var fr = new FileReader();

    //Add an event listener to handle getting the contents of the .txt or .csv
    //file when it is loaded
    fr.addEventListener("load", () => {
      fileInput = fr.result;
      //Branch to handle different operating system line endings (Windows v. Linux)
      if(fileInput.includes("\r")){
        titles = fileInput.split("\r\n");
      } else {
        titles = fileInput.split("\n");
      }
      //Work to gather the titles of papers
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

  //Function to create an author in the database through an axios call.
  const makeAuthor = async () => {
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
      return data.id;
  }

  //Function to handle making a call to the scraper to get information based on a title.
  const getScrapedPaper = async (paperTitle) => {
        const response = await axios.get(`/api/scraping/papers?title=${paperTitle}`, {
            mode:'cors'});
        if (response.status === 200) {
          console.log(response);
          return response.data;
        }
  }

  //Function to take a scraped paper and add it to the database
  const postPaper = async (paper, title) => {
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
      return data.id;
  }

  //Function to create the citation associated with a certain paper.
  const postCitation = async (paperId, paper) => {
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
  }

  //Function to handle creating an entry in the Author-Paper join table in the database.
  const joinAuthorToPaper = async (paperId, authorId) => {
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
  }

  //Function to handle creating an entry in the Paper-Author join table in the database.
  const joinPaperToAuthor = async (paperId, authorId) => {
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
  }

  //Return the related HTML of the page.
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
                <input type="submit" onClick="location.href='www.yoursite.com'"/>
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