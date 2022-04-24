import React from "react";
import axios from 'axios';

//Authors: Carter Thunes, Justin Orringer
function CreateAuthor() {
    
    let authors = [];

    //Function to scrape authors in google scholar.
    const getScrapedAuthors = async () => {
        hideFailedAlert();
        hideNoResultsAlert();
        hideButton();
        let name = document.getElementById("authName").value;
        document.getElementById("wait").innerText = "Searching...";
        try {
            const response = await axios.get(`/api/scraping/profiles?name=${name}`, {
                mode:'cors'});
            authors = response.data;
            const parentList = document.getElementById("authorList");
            parentList.innerHTML = "";
            if (authors.length === 0) {
                document.getElementById("noresults").style = "display: block !important";
                let button = document.createElement("button");
                button.className = "btn btm-sm btn-danger";
                button.id = "button";
                button.onclick = function() { createAuthor(name, null) };
                button.innerText = "Create '" + name + "' Anyway";
                document.getElementById("container").appendChild(button);
            } else {
                authors.forEach(author => {
                    let a = document.createElement("a");
                    a.className = "list-group-item list-group-item-action flex-column align-items-start";
                    a.id = author.name + '+' + author.id;
                    a.onclick = function() { createAuthor(author.name, author.id) };
                    let div = document.createElement("div");
                    div.className = "d-flex w-100 justify-content-between";
                    let h5 = document.createElement("h5");
                    h5.className = "mb-1 py-2";
                    h5.innerText = author.name;
                    let small = document.createElement("small");
                    small.className = "text-muted";
                    small.innerText = author.institution;
                    parentList.appendChild(a);
                    a.appendChild(div);
                    div.appendChild(h5);
                    div.appendChild(small);
                });
                let label = document.createElement("label");
                label.id = "label";
                label.className = "mr-2 mt-3";
                label.innerText = "Is the author you're looking for not here? Try searching full name, partial name, or just";
                let button = document.createElement("button");
                button.className = "btn btm-sm btn-danger";
                button.id = "button";
                button.onclick = function() { createAuthor(name, null) };
                button.innerText = "Create '" + name + "'";
                document.getElementById("container").appendChild(label);
                document.getElementById("container").appendChild(button);
            }
        }
        catch (e) {
            document.getElementById("failed").style = "display: block !important";
            let label = document.createElement("label");
            label.id = "label";
            label.className = "mr-2 mt-3";
            label.innerText = "Is the author you're looking for not here? Try searching full name, partial name, or just";
            let button = document.createElement("button");
            button.className = "btn btm-sm btn-danger";
            button.id = "button";
            button.onclick = function () { createAuthor(name, null) };
            button.innerText = "Create '" + name + "'";
            document.getElementById("container").appendChild(label);
            document.getElementById("container").appendChild(button);
        }
        document.getElementById("wait").innerText = "";
    }
    
    function createAuthor(name, id) {
        //Function to create an author in the database through an axios call.
        const makeAuthor = async () => {
            try {
                const response = await axios({
                    method: "post",
                    url: '/api/authors',
                    headers: {
                        'Access-Control-Allow-Origin': '*',
                        'Content-Type': 'application/json',
        
                    },
                    
                    //make sure to serialize your JSON body
                    data: JSON.stringify({
                        name: name,
                        scholar_id: id
                    }), mode: 'cors'
                    }, true);
                const authorID = response.data.id;
                window.location.href = `/author/${authorID}`;
            } catch (e) {
                console.log("Failed to create author.");
            }
        }
        makeAuthor();
    }

    function hideFailedAlert() {
        document.getElementById("failed").style = "display: none !important";
    }

    function hideNoResultsAlert() {
        document.getElementById("noresults").style = "display: none !important";
    }

    function hideButton() {
        try {
            document.getElementById("button").remove();
            document.getElementById("label").remove();
        } catch (e) {
            console.log("Button or label doesn't exist.");
        }
    }

  //Return the related HTML of the page.
  return (
    <div className="body" id="body">
        <div className="alert alert-warning alert-dismissible" role="alert" id="failed" style={{display: "none"}}>
            <button className="close" type="button" onClick={hideFailedAlert}><span>&times;</span></button>Failed to search author, please try again.
        </div>

        <div className="container">
            <div className="row pl-3">
                <label>Enter Author Name: &nbsp;</label>
                <input className="mx-3" type="text" id="authName"></input>
                <button id="searchButton" type="button" className="btn btm-sm btn-danger" onClick={getScrapedAuthors}>Search Google Scholar</button>
                <span className="ml-3" id="wait"></span>
            </div>
        </div>

        <div className="container pt-4" id="optionsLabel">
            <h4>Author Options:</h4>
        </div>
        <div className="container border my-3 p-4" id="container">
            <div className="list-group" id="authorList">
            </div>
            <div className="alert alert-warning alert-dismissible" role="alert" id="noresults" style={{display: "none"}}>
                <button className="close" type="button" onClick={hideNoResultsAlert}><span>&times;</span></button>No results for this input, please try again.
            </div>
        </div>
    </div>
    
  );
}

export default CreateAuthor;