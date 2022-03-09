import React from "react";
import axios from 'axios';

//Function to create an HTML representation of the Query page for the app
//while also handling dynamic calls to the API.
//Authors: Gage Fringer, Carter Thunes, Justin Orringer
function Query() {
    //Variable to hold list of current authors in the system
    let authors = [];
    //Variable to hold list of papers related to an author
    let papers = [];

    //Function to make an API call to gather a list of all current authors.
    const getAuthors = async () => {
        try {
            const response = await axios.get('/api/authors', {mode:'cors'});
            //console.log(response.data);
            if (response.status === 200)
                authors = response.data;
            //console.log({response, authors})
        }
        catch (e) {
            console.log(e.getMessage);
        }
        //console.log(authors);
        const parentForm = document.getElementById("authorForm");
        parentForm.innerHTML = "";
        //console.log(parentForm);
        authors.forEach(author => {
            let option = document.createElement("option");
            option.innerText = author.name;
            option.value = author.id;
            parentForm.appendChild(option);
        });

        const authorForm = document.getElementById("authorCheckboxes");
        authorForm.innerHTML = "";
        //console.log(authorForm);
        authors.forEach(author => {
            var row = document.createElement("tr");
            var box = document.createElement("td");
            var name = document.createElement("td");
            let input = document.createElement("input");
            let label = document.createElement("label");
            input.setAttribute('type', 'checkbox');
            label.innerText = author.name;
            input.innerText = author.name;
            input.value = author.id;
            input.id = author.name;
            //label.innerHTML = input;
            box.appendChild(input);
            name.appendChild(label);
            row.appendChild(box);
            row.appendChild(name);
            authorForm.appendChild(row);
        });
    }

    //Function to make the API call to gather the papers of a specific author.
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
                //console.log({response, papers});
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


    //Function to get called by the download button so that a CSV is generated for the user, now tied to checkboxes
    function htmlToCSV(){

        var output = ["Author,Article,Year,CitationCount\n"];

        var csv_file, download_link;

        var highest_id = 0;

        var has_checked = false;

        //Determine the highest ID of a selected author, that is our last we want to output
        authors.forEach(author => {
            if(document.getElementById(author.name).checked){
                has_checked = true;
                if(author.id > highest_id){
                    highest_id=author.id;
                }
            }
        });

        if(!has_checked){
            console.log("No papers selected");
            return;
        }

        authors.forEach(author => {
            let name = author.name;
            let id = author.id;
            var label = document.getElementById(name);
            
            if(label.checked){
                const getPapersById = async () => {
                    try {
                        const response = await axios.get(`/api/authors/${id}/papers`, {mode:'cors'});
                        if (response.status === 200)
                            papers = papers.concat(response.data);//= response.data;
                        //console.log({response, papers});
                    }
                    catch (e) {
                        console.log(e.getMessage);
                    }

                    papers.forEach(paper => {
                        let article = paper.name;
                        let year = paper.year;
                        let citations = paper.latest_citation.num_cited;
            
                        let new_string = author.name + "," + "\"" + article + "\"," + year + "," + citations + "\n";
                        output.push(new_string);
                        
                    });
                    
                    //If on that last author, then output
                    if(label.value == highest_id){
                        csv_file = new Blob(output, {type: "text/csv"});
        
                        download_link = document.createElement("a");
                    
                        download_link.download = "output.csv";
                    
                        download_link.href = window.URL.createObjectURL(csv_file);
                    
                        download_link.style.display = "none";
                    
                        document.body.appendChild(download_link);
                    
                        download_link.click();
                    }
                }
                

                getPapersById();

            }

        })     
        

        

        //Method for exporting adapted from the link below
        //https://yourblogcoach.com/export-html-table-to-csv-using-javascript/

        /*var csv_file, download_link;

        csv_file = new Blob(output, {type: "text/csv"});

        download_link = document.createElement("a");
    
        download_link.download = "output.csv";
    
        download_link.href = window.URL.createObjectURL(csv_file);
    
        download_link.style.display = "none";
    
        document.body.appendChild(download_link);
    
        download_link.click();*/
    }

  //Return the related HTML of the page.
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
                  <button id="queryButton" type="button" className="btn btn-danger" onClick={query}>Query</button>
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

      <div className="container">
          <table id="authorCheckboxes">
          </table>
      </div>

      <div className="container">
          <button type="button" onClick={htmlToCSV}>Download Results</button>
      </div>
    </div>
  );
}

export default Query;