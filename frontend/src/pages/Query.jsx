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

    //Function to make the API call to gather the papers of a specific author.
    function viewAuthor() {
        const parentForm = document.getElementById("authorForm");
        if (parentForm === null) {
            return;
        }
        var authorID = parentForm.value;
        window.location.href = `/author/${authorID}`;
    }

    getAuthors();

  //Return the related HTML of the page.
  return (
    <div className="body">
        <div className="container" id="container">
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
                    <button type="button" className="btn btn-danger" onClick={viewAuthor}>Select</button>
                </div>
            </div>
            <div className="row pl-3">
                <label>Don't see your author?</label>
                <pre> </pre>
                <a href="/createauthor">Make a new author.</a>
            </div>
        </div>
        <hr />
    </div>
  );
}

export default Query;