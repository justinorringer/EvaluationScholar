import React, { useEffect, useState } from "react";
import axios from 'axios';

function Query() {
    let authors = [];
    let papers = [];
    let parentForm = document.getElementById("authorForm");
    let paperTableBody = document.getElementById("paperTableBody");

    const getAuthors = async () => {
        try {
            const response = await axios.get('/api/authors', {mode:'cors'});
            if (response.ok) {
                authors = response.json();
            }
            console.log({response, authors})
        }
        catch (e) {
            console.log(e.getMessage);
        }
        console.log(authors)
        authors.forEach(author => {
            let option = document.createElement("option");
            option.innerText = author.name;
            option.value = author.id;
            parentForm.appendChild(option);
        });
    }

    function query() {
        if (parentForm === null) {
            return;
        }
        var authorID = parentForm.value;
        const getPapersByAuthor = async () => {
            try {
                const response = await axios.get(`/api/authors/${authorID}/papers`, {mode:'cors'});
                if (response.ok) {
                    papers = response.json();
                }    
                console.log({response, papers});
            }
            catch (e) {
                console.log(e.getMessage);
            }
        }
        getPapersByAuthor();
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

    getAuthors();

  return (
    <div className="body">
      <div className="container pt-5">
          <div className="justify-content-center page-header">Select Author</div>
          {/* <div className="form-group">
              <input type="author" className="form-control" placeholder="G. Rothermel" />
          </div> */}
          <div className="row">
              <div className="col-10 gx-4 gy-4">
                  <div className="form-group">
                      <br />
                      <select multiple className="form-control" id="authorForm">
                      </select>
                  </div>
              </div>
              <div className="col-2 gy-4 gx-4 justify-content-right">
                  <br />
                  <button type="button" className="btn btn-danger" onClick={query}>Query</button>
              </div>
          </div>
      </div>
      <hr />

      <div className="container">
          <table className="table table-borderless table-striped" >
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
  );
}

export default Query;