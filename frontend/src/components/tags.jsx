import React from "react";
import axios from 'axios';

function Tags() {

    //Variable to hold list of current authors in the system
    let authors = [];
    //Variable to hold list of papers related to an author
    let tags = [];

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
        const authorList = document.getElementById("authorList");
        authorList.innerHTML = "";
        console.log(authorList);
        authors.forEach(author => {
            let option = document.createElement("li");
            let label = document.createElement("label");
            label.className = "container";
            let input = document.createElement("input");
            input.className = "checkbox";
            input.type = "checkbox";
            let span = document.createElement("span");
            span.className = "checkmark";
            span.style = "padding-left: 8px";
            option.appendChild(label);
            label.appendChild(input);
            label.appendChild(span);
            span.innerText = author.name;
            label.value = author.id;
            authorList.appendChild(option);
        });
    }

    const getTags = async () => {
        console.log("inside getTags()");
        try {
            const response = await axios.get('/api/tags', {mode:'cors'});
            console.log(response.data);
            if (response.status === 200)
                tags = response.data;
            console.log({response, tags})
        }
        catch (e) {
            console.log(e.getMessage);
        }
        console.log(tags);
        const tagList = document.getElementById("tagList");
        tagList.innerHTML = "";
        console.log(tagList);
        tags.forEach(tag => {
            let option = document.createElement("li");
            let label = document.createElement("label");
            label.className = "container";
            let input = document.createElement("input");
            input.className = "checkbox";
            input.type = "checkbox";
            let span = document.createElement("span");
            span.className = "checkmark";
            span.style = "padding-left: 8px";
            option.appendChild(label);
            label.appendChild(input);
            label.appendChild(span);
            span.innerText = tag.name;
            label.value = tag.id;
            tagList.appendChild(option);
        });
    }

    function createTag() {
        const tagName = document.getElementById("tagBox").value;
        console.log(tagName);
        if (tagName === null) {
            return;
            //alert?
        }
        //Function to create an author in the database through an axios call.
        const makeTag = async () => {
            const response = await axios({
            method: "post",
            url: '/api/tags',
            headers: {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json',

            },
            
            //make sure to serialize your JSON body
            data: JSON.stringify({
                name: tagName,
            }), mode: 'cors'
            }, true);
            
            console.log(response);
            const data = await response.data;
            getTags();
        }
        makeTag();
        document.getElementById("tagBox").value = "";
    }

    getAuthors();
    getTags();

  //Return the related HTML of the page.
  return (
    <div className="container">
        <div className="container pt-4">
            <h2>Assign Tags to Authors</h2>
        </div>
        <div className="container border border-dark my-3 p-4 rounded">
            <h3>
                Authors
            </h3>
            <div className="row">
                <div className="col-12">
                    <ul className="col-count-3" id="authorList">
                        <li>
                            <label className="container">
                                <input type="checkbox" />
                                <span className="checkmark"></span>
                                Author 1
                            </label>
                        </li>
                        <li>
                            <label className="container">
                                <input type="checkbox" />
                                <span className="checkmark"></span>
                                Author 2
                            </label>
                        </li>
                    </ul>
                </div>
            </div>
        </div>
        <div className="container border border-dark my-3 p-4 rounded">
            <div className="row">
                <h3>
                    Tags
                </h3>
                <div className="form-group px-5" >
                    <input type="type" className="form-control" id="tagBox" placeholder="Tag" />
                </div>
                <button type="button" className="btn btn-danger btn-sm" onClick={createTag}>Create</button>
            </div>

            <div className="row">
                <div className="col-12">
                    <ul className="col-count-3" id="tagList">
                        <li>
                            <label className="container">Tag 1
                                <input type="checkbox" />
                                <span className="checkmark"></span>
                            </label>
                        </li>
                        <li>
                            <label className="container">Tag 2
                                <input type="checkbox" />
                                <span className="checkmark"></span>
                            </label>
                        </li>
                    </ul>
                </div>
            </div>
        </div>

        <div className="container">
            <button type="button" className="btn btn-danger btn-sm float-right">Submit</button>
        </div>
    </div>
  );
}

export default Tags;