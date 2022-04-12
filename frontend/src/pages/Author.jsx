import React from "react";
import axios from 'axios';
import { useParams } from 'react-router-dom';

// Each author has an Author page with their tags and articles listed.
function Author() {

    const authorID = useParams().id;

    let authorName = "";

    let authorScholarID = "";

    //Variable to hold list of papers related to an author
    let papers = [];
    let tags = [];

    //Function to make the API call to gather the papers of a specific author.
    function getAuthor() {
        const getPapers = async () => {
            try {
                const response = await axios.get(`/api/authors/${authorID}/papers`, {mode:'cors'});
                if (response.status === 200)
                    papers = response.data;
            }
            catch (e) {
                console.log("Failed to get papers.");
            }
            const paperTableBody = document.getElementById("paperTableBody");
            const paperTable = document.getElementById("paperTable");
            if (document.getElementById("alertid")) {
                document.getElementById("alertid").remove();
            }
            if (papers.length > 0) {
                paperTableBody.innerHTML = "";
                paperTable.style = "display: block !important";
            } else {
                paperTable.style = "display: none !important";
                var alert = document.createElement("div");
                alert.className = "alert alert-warning alert-dismissable";
                alert.role="alert";
                alert.innerText = "No papers found! Upload some on the left!";
                alert.id = "alertid";
                document.getElementById("articles").appendChild(alert);
                return;
            }
            papers.forEach(paper => {
                var row = document.createElement("tr");
                var article = document.createElement("td");
                var year = document.createElement("td");
                var citations = document.createElement("td");
                article.innerText = paper.name;
                year.innerText = paper.year;
                citations.innerText = paper.latest_citation.num_cited;
                row.appendChild(article);
                row.appendChild(year);
                row.appendChild(citations);
                paperTableBody.appendChild(row);
            });
        }
        const getTags = async () => {
            try {
                const response = await axios.get(`/api/authors/${authorID}/tags`, {mode:'cors'});
                if (response.status === 200)
                    tags = response.data;
            }
            catch (e) {
                console.log("Failed to get tags.");
            }
            let tagList = document.getElementById("Tags");
            tags.forEach(tag => {
                // fill in the list of tags
                var tagElement = document.createElement("li");
                tagElement.innerText = tag.name;
                tagList.appendChild(tagElement);
            });
        }
        const getAuthorInfo = async () => {
            try {
                const response = await axios.get(`/api/authors/${authorID}`, {mode:'cors'});
                if (response.status === 200) {
                    authorName = response.data.name;
                    if (response.data.scholar_id) {
                        authorScholarID = response.data.scholar_id; 
                    } else {
                        document.getElementById("gslink").remove();
                    }
                    
                    
                    //create HTML link element for this, do same thing as author name.

                    var authorHeader = document.getElementById("authorName");
                    authorHeader.innerText = authorName;
                }
            }
            catch (e) {
                console.log("Failed to get author info.");
            }
        }
        getAuthorInfo();
        getPapers();
        getTags();
    }

    getAuthor();

    // Function for adding new articles on click
    //Variable to hold data from a file selected to be read in.

    //Object to hold the data getting pulled, both a name string and institution string

    //Method to handle the upload of a file
    //and also call other functions necessary for this page

    function upload(){
        var formData = new FormData();
        formData.append("file", document.getElementById('myfile').files[0])
        const postPaperTasks = async () => {
            try {
                const response = await axios.post(`/api/tasks/create-papers?author_id=${authorID}`, formData, {
                    headers: {
                      'Access-Control-Allow-Origin': '*',
                      'Content-Type': 'multipart/form-data',
                    },
                    mode: 'cors'
                  }, true);
                if (response.status === 201) {
                    document.getElementById("success").style = "display: block !important";
                } else {
                    document.getElementById("fail").style = "display: block !important";
                }
            }
            catch (e) {
                console.log("Failed to upload file.");
            }
        }
        postPaperTasks();
    }

    function googleScholarRedirect() {
        window.open(
            "https://scholar.google.com/citations?hl=en&oi=ao&user=" + authorScholarID,
            '_blank'
          );
    }

    function hideSuccessAlert() {
        document.getElementById("success").style = "display: none !important";
    }

    function hideFailAlert() {
        document.getElementById("fail").style = "display: none !important";
    }
        
    // HTML by Justin Orringer
    return (
      <div className="body">
        <div className="container">
            <div className="row d-flex" id="authorSidebar">
                <div className="col-3" id="authorSidebar">
                    <div className="row">
                        <img className="border" id="profile" src="/images/generic.png" alt="" />
                    </div>
                    <div className="row pt-4" id="tagHeader">
                        <h4>Tags</h4>
                    </div>
                    <div className="row pt-2">
                        <div className="container">
                            <ul id="Tags">
                            </ul>
                        </div>
                    </div>

                    <div className="row pt-2">
                        <button type="button" class="btn btn-danger" data-toggle="modal" data-target="#uploadPapersModal">
                            Upload Papers
                        </button>
                    </div>

                    <div className="modal fade" id="uploadPapersModal" tabindex="-1" role="dialog" aria-labelledby="uploadPapersModalTitle" aria-hidden="true">
                        <div className="modal-dialog modal-dialog-centered" role="document">
                            <div className="modal-content">
                            <div className="modal-header">
                                <h5 className="modal-title" id="uploadPapersModalLongTitle">Upload File with Paper Titles</h5>
                                <button type="button" className="close" data-dismiss="modal" aria-label="Close">
                                    <span aria-hidden="true">&times;</span>
                                </button>
                            </div>
                            <div className="modal-body">
                                <div className="row pl-3">
                                    <label for="myfile">Select a file:&nbsp;</label>
                                    <input type="file" id="myfile" name="myfile"/>
                                </div>
                            </div>
                            <div className="modal-footer">
                                <button type="button" className="btn btn-secondary" data-dismiss="modal">Cancel</button>
                                <button type="button" className="btn btn-success" data-dismiss="modal" onClick={upload}>Upload</button>
                            </div>
                            </div>
                        </div>
                    </div>
                    <div className="row pt-3 pr-3">
                        <div className="alert alert-success alert-dismissible" role="alert" id="success" style={{display: "none"}}>
                            <button className="close" type="button" onClick={hideSuccessAlert}><span>&times;</span></button>File uploaded successfully.
                            <pre>
                            </pre>
                            <a href="/tasks">View in 'Tasks'</a>
                        </div>
                    </div>
                    <div className="row pt-3 pr-3">
                        <div className="alert alert-danger alert-dismissible pt-2" role="alert" id="fail" style={{display: "none"}}>
                            <button className="close" type="button" onClick={hideFailAlert}><span>&times;</span></button> Error uploading file.
                        </div>
                    </div>
                </div>
                <div className="col-9" id="mainColumn">
                    <div className="row">
                        <h3 className="px-0" id="authorName"></h3>
                        <div className = "ml-auto" id="gslink">
                            <a href = "" rel="noreferrer noopener" onClick={googleScholarRedirect}>Google Scholar profile</a>
                        </div>
                    </div>
                    <div className="row pt-2" id="articles">
                        <table className="table table-borderless table-striped" id="paperTable" style={{display: "none"}}>
                            <thead className="thead-dark">
                                <tr>
                                    <th scope="col-6">Article</th>
                                    <th scope="col-2">Year</th>
                                    <th scope="col-2">Citations</th>
                                </tr>
                            </thead>
                            <tbody id = "paperTableBody">
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
      </div>
      
    );
  }
  
  export default Author;