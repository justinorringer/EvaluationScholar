import React from "react";
import axios from 'axios';

//Authors: Carter Thunes, Justin Orringer
function CreateAuthor() {
    
    let authors = [];

    //Function to scrape authors in google scholar.
    const getScrapedAuthors = async () => {
        document.getElementById("wait").innerText = "Searching...";
        let name = document.getElementById("authName").value;
        const response = await axios.get(`/api/scraping/profiles?name=${name}`, {
            mode:'cors'});
        if (response.status === 200) {
            console.log(response);
            authors = response.data;
            const parentList = document.getElementById("authorList");
            parentList.innerHTML = "";
            console.log(authors);
            authors.forEach(author => {
                console.log(author);
                let a = document.createElement("a");
                a.className = "list-group-item list-group-item-action flex-column align-items-start";
                a.id = author.name + '+' + author.id;
                a.onclick = function() { createAuthor(a.id) };
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
        }
        document.getElementById("wait").innerText = "";
    }
    
    function createAuthor(name_id) {
        const arr = name_id.split("+");
        console.log(arr);
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
                name: arr[0],
                scholar_id: arr[1]
            }), mode: 'cors'
            }, true);
            
            console.log(response);
            const authorID = response.data.id;
            window.location.href = `/author/${authorID}`;
        }
        makeAuthor();
    }

  //Return the related HTML of the page.
  return (
    <div className="body">
        <div className="container">
            <div className="row pl-3">
                <label>Enter Author Name: &nbsp;</label>
                <input className="mx-3" type="text" id="authName"></input>
                <button type="button" class="btn btm-sm btn-danger" onClick={getScrapedAuthors}>Search Google Scholar</button>
                <span className="ml-3" id="wait"></span>
            </div>
        </div>

        <div className="container pt-4" id="optionsLabel">
            <h4>Author Options:</h4>
        </div>
        <div className="container border my-3 p-4">
            <div className="list-group" id="authorList">
            </div>
        </div>
    </div>
    
  );
}

export default CreateAuthor;