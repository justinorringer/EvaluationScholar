import React from "react";
import axios from 'axios';
import { useParams } from 'react-router-dom';

// Each author has an Author page with their tags and articles listed.
function Author() {

    const authorID = useParams().id;

    //Variable to hold list of papers related to an author
    let papers = [];

    //Function to make the API call to gather the papers of a specific author.
    function getAuthor() {
        const getPapers = async () => {
            try {
                const response = await axios.get(`/api/authors/${authorID}/papers`, {mode:'cors'});
                if (response.status === 200)
                    papers = response.data;
                console.log({response, papers});
            }
            catch (e) {
                console.log(e);
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
                alert.innerText = "No papers found for this author!";
                alert.id = "alertid";
                document.getElementById("container").appendChild(alert);
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
                    papers = response.data;
                console.log({response, papers});
            }
            catch (e) {
                console.log(e);
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
                alert.innerText = "No papers found for this author!";
                alert.id = "alertid";
                document.getElementById("container").appendChild(alert);
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
        const getAuthorName = async () => {
            try {
                const response = await axios.get(`/api/authors/${authorID}`, {mode:'cors'});
                if (response.status === 200)
                    papers = response.data;
                console.log({response, papers});
            }
            catch (e) {
                console.log(e);
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
                alert.innerText = "No papers found for this author!";
                alert.id = "alertid";
                document.getElementById("container").appendChild(alert);
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
        getPapers();
        getTags();
        getAuthorName();
    }

    getAuthor();
    
    // HTML by Justin Orringer
    return (
      <div className="body">
        <div className="container">
            <div className="row" id="authorSidebar">
                <div className="col-3" id="authorSidebar">
                    <div className="row">
                        <img className="border" id="profile" src="src\generic.png" alt="" />
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
                        <form action="/action_page.php">
                            <h4 for="myfile">Upload Articles</h4>
                            <input type="file" id="myfile" name="myfile" />
                            <input type="submit" />
                        </form>
                    </div>
                </div>
                <div className="col-9" id="mainColumn">
                    <div className="row pt-5">
                        <h3 className="px-0">{{authorName}}</h3>
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