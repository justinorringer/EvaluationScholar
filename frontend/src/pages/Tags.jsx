import React from "react";
import axios from 'axios';

function Tags() {

    //Variable to hold list of current authors in the system
    let authors = [];
    //Variable to hold list of papers related to an author
    let tags = [];

    let checkedAuthors = [];
    let checkedTags = [];

    //Function to make an API call to gather a list of all current authors.
    const getAuthors = async () => {
        try {
            const response = await axios.get('/api/authors', {mode:'cors'});
            console.log(response.data);
            if (response.status === 200)
                authors = response.data;
            else {
                document.getElementById("fail").style = "display: block !important";
                document.getElementById("fail").innerText = "Error Connecting to the Database";
            }
            console.log({response, authors})
        }
        catch (e) {
            console.log(e.getMessage);
            document.getElementById("fail").style = "display: block !important";
            document.getElementById("fail").innerText = "Error Connecting to the Database";
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
            input.id = "a" + author.id;
            input.onclick = function() { checkedAuthor(input.id) };
            let span = document.createElement("span");
            span.className = "checkmark";
            span.style = "padding-left: 8px";
            option.appendChild(label);
            label.appendChild(input);
            label.appendChild(span);
            span.innerText = author.name;
            authorList.appendChild(option);
        });
    }

    const getTags = async () => {
        console.log("inside getTags()");
        try {
            const response = await axios.get('/api/tags', {mode:'cors'});
            console.log(response.data);
            if (response.status === 200) {
                tags = response.data;
            }
            else {
                document.getElementById("fail").style = "display: block !important";
                document.getElementById("fail").innerText = "Error Connecting to the Database";
            }
            console.log({response, tags})
        }
        catch (e) {
            console.log(e.getMessage);
            document.getElementById("fail").style = "display: block !important";
            document.getElementById("fail").innerText = "Error Connecting to the Database";
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
            input.id = "t" + tag.id;
            input.onclick = function() { checkedTag(input.id) };
            let span = document.createElement("span");
            span.className = "checkmark";
            span.style = "padding-left: 8px";
            option.appendChild(label);
            label.appendChild(input);
            label.appendChild(span);
            span.innerText = tag.name;
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
            
            if (response.status === 200) {
                document.getElementById("success").style = "display: block !important";
                document.getElementById("success").innerText = "Tags Created Successfully";
            }
            else {
                document.getElementById("fail").style = "display: none !important";
                document.getElementById("fail").innerText = "Error Creating Tag";
            }
            console.log(response);
            const data = await response.data;
            getTags();
        }
        makeTag();
        document.getElementById("tagBox").value = "";
    }

    function checkedAuthor(id) {
        var checkBox = document.getElementById(id);
        console.log(checkedAuthors);
        if (checkBox.checked == true){
            checkedAuthors.push(id.substring(1));
            console.log(checkedAuthors);
        } else {
            const index = checkedAuthors.indexOf(id.substring(1));
            checkedAuthors.splice(index, 1);
            console.log(checkedAuthors);
        }
    }

    function checkedTag(id) {
        var checkBox = document.getElementById(id);
        console.log(checkedTags);
        if (checkBox.checked == true){
            checkedTags.push(id.substring(1));
            console.log(checkedTags);
        } else {
            const index = checkedTags.indexOf(id.substring(1));
            checkedTags.splice(index, 1);
            console.log(checkedTags);
        }
    }

    function assignTags() {
        const assign = async () => {
            const response = await axios({
                method: "put",
                url: `/api/tags/authors`,
                headers: {
                  'Access-Control-Allow-Origin': '*',
                  'Content-Type': 'application/json',
                },
                data: JSON.stringify({
                    authors: checkedAuthors,
                    tags: checkedTags
                  }),
                mode: 'cors'
              }, true);
            console.log(response);
            if (response.status === 200) {
                document.getElementById("success").style = "display: block !important";
                document.getElementById("success").innerText = "Tags Assigned Successfully";
            }
            else {
                document.getElementById("fail").style = "display: block !important";
                document.getElementById("fail").innerText = "Error: Failed to Assign Tags";
            }
            checkedAuthors.forEach((id) => {
                var elementid = "a" + id;
                var checkBox = document.getElementById(elementid);
                checkBox.checked = false;
            });
            checkedTags.forEach((id) => {
                var elementid = "t" + id;
                var checkBox = document.getElementById(elementid);
                checkBox.checked = false;
            });
            checkedAuthors = [];
            checkedTags = [];
        }
        assign();
    }

    function unassignTags() {
        const unassign = async () => {
            const response = await axios({
                method: "delete",
                url: `/api/tags/authors`,
                headers: {
                  'Access-Control-Allow-Origin': '*',
                  'Content-Type': 'application/json',
                },
                data: JSON.stringify({
                    authors: checkedAuthors,
                    tags: checkedTags
                  }),
                mode: 'cors'
              }, true);
            console.log(response);
            if (response.status === 200) {
                document.getElementById("success").style = "display: block !important";
                document.getElementById("success").innerText = "Tags Assigned Successfully";
            }
            else {
                document.getElementById("fail").style = "display: block !important";
                document.getElementById("fail").innerText = "Error: Failed to Unassign Tags";
            }
            checkedAuthors.forEach((id) => {
                var elementid = "a" + id;
                var checkBox = document.getElementById(elementid);
                checkBox.checked = false;
            });
            checkedTags.forEach((id) => {
                var elementid = "t" + id;
                var checkBox = document.getElementById(elementid);
                checkBox.checked = false;
            });
            checkedAuthors = [];
            checkedTags = [];
        }
        unassign();
    }

    function deleteTags(){
        const deleteTag = async () => {
            const mapPromises = checkedTags.map(tag => {
                return axios.delete(`/api/tags/${tag}`, { mode: 'cors' }).then(res => {
                    if (res.status == 200) {
                        console.log("Deleted tag");
                    }
                    else {
                        console.log("Error deleting tag");
                    }
                });
            });
            Promise.all(mapPromises).then(() => {
                checkedTags = [];
                getTags();
            })
        }
        deleteTag();
    }

    function hideSuccessAlert() {
        document.getElementById("success").style = "display: none !important";
    }

    function hideFailAlert() {
        document.getElementById("fail").style = "display: none !important";
    }

    getAuthors();
    getTags();

    //Return the related HTML of the page.
    return (
        <div className="body">
            <div className="container">
                <div className="container">
                    <h3>Assign Tags to Authors</h3>
                </div>
                <div className="row">
                    <div className="alert alert-success alert-dismissible" role="alert" id="success" style={{ display: "none" }}>
                        <button className="close" type="button" onClick={hideSuccessAlert}><span>&times;</span></button> Tags Assigned Successfully.
                    </div>
                </div>
                <div className="row">
                    <div className="alert alert-danger alert-dismissible" role="alert" id="fail" style={{ display: "none" }}>
                        <button className="close" type="button" onClick={hideFailAlert}><span>&times;</span></button> Error: No Tags Assigned.
                    </div>
                </div>
                <div className="container border border-dark my-3 p-4 rounded">
                    <h3>
                        Authors
                    </h3>
                    <div className="row">
                        <div className="col-12">
                            <ul className="col-count-3" id="authorList">
                            </ul>
                        </div>
                    </div>
                </div>
                <div className="container border border-dark my-3 p-4 rounded">
                    <div className="row px-2 pb-2 d-flex">
                        <h3>
                            Tags
                        </h3>
                        <div className="d-flex px-3 align-items-right ml-auto">
                            <input type="type" className="form-control mr-2" id="tagBox" placeholder="New Tag" />
                            <button type="button" className="btn btn-danger btn-sm" onClick={createTag}>Create</button>
                        </div>
                    </div>

                    <div className="row">
                        <div className="col-12">
                            <ul className="col-count-3" id="tagList">
                            </ul>
                        </div>
                    </div>
                </div>

                <div className="container d-flex justify-content-end">
                    <button type="button" className="btn btn-danger btn-sm mr-2" onClick={deleteTags}>Delete</button>
                    <button type="button" className="btn btn-danger btn-sm mr-2" onClick={assignTags}>Assign</button>
                    <button type="button" className="btn btn-danger btn-sm" onClick={unassignTags}>Unassign</button>
                </div>
            </div>
        </div>
    );
}

export default Tags;