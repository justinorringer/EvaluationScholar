import React, { useEffect, useState } from "react";
import axios from 'axios';

function Query() {
    let authors = [];
    let papers = [];

    const getAuthors = async () => {
        try {
            const response = await axios.get('/api/authors', {mode:'cors'});
            console.log(response.data);
            if (response.status === 200)
                authors = response.data;
            console.log({response, authors})
        }
        catch (e) {
            console.log(e.getMessage);
        }
        console.log(authors);
        const parentForm = document.getElementById("authorForm");
        parentForm.innerHTML = "";
        console.log(parentForm);
        authors.forEach(author => {
            let option = document.createElement("option");
            option.innerText = author.name;
            option.value = author.id;
            parentForm.appendChild(option);
        });
    }

    function query() {
        const parentForm = document.getElementById("authorForm");
        if (parentForm === null) {
            return;
        }
        var authorID = parentForm.value;
        const getPapersByAuthor = async () => {
            try {
                const response = await axios.get(`/api/authors/${authorID}/papers`, {mode:'cors'});
                if (response.status === 200)
                    papers = response.data;
                console.log({response, papers});
            }
            catch (e) {
                console.log(e.getMessage);
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
        getPapersByAuthor();
    }

    getAuthors();

  return (
    <div className="body">
      <div className="container pt-5" id="container">
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
          <table className="table table-borderless table-striped" id="paperTable" style={{display: "none"}}>
              <colgroup>
                  <col class="col-md-8"/>
                  <col class="col-md-1"/>
                  <col class="col-md-1"/>
              </colgroup>
              <thead className="thead-dark">
                  <tr>
                      <th>Article</th>
                      <th>Year</th>
                      <th>Citations</th>
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