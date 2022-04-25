import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Checkbox from '@mui/material/Checkbox';
import TextField from '@mui/material/TextField';
import Autocomplete from '@mui/material/Autocomplete';
import CheckBoxOutlineBlankIcon from '@mui/icons-material/CheckBoxOutlineBlank';
import CheckBoxIcon from '@mui/icons-material/CheckBox';

const icon = <CheckBoxOutlineBlankIcon fontSize="small" />;
const checkedIcon = <CheckBoxIcon fontSize="small" />;

function Tags() {

    const [authors, setAuthors] = useState([]);

    const [selectedAuthors, setSelectedAuthors] = useState([]);

    const [tags, setTags] = useState([]);

    const [selectedTags, setSelectedTags] = useState([]);

    /**
     * Function to sort alphabetically an array of objects by some specific key.
     * 
     * @param {String} property Key of the object to sort.
     * @author https://ourcodeworld.com/articles/read/764/how-to-sort-alphabetically-an-array-of-objects-by-key-in-javascript
     */
     function alphabeticSort(property) {
        let sortOrder = 1;

        if (property[0] === "-") {
            sortOrder = -1;
            property = property.substr(1);
        }

        return function (a, b) {
            if (sortOrder == -1) {
                return b[property].localeCompare(a[property]);
            } else {
                return a[property].localeCompare(b[property]);
            }
        }
    }

    useEffect(() => {
        axios.get("api/authors")
            .then(response => {
                setAuthors(response.data.sort(alphabeticSort("name")));
                
            }).
            catch(err => {
                console.log(err);
                document.getElementById("fail").style = "display: block !important";
                document.getElementById("failspan").innerText = "Error Getting Authors";
            }
        );
        getTags();
    }, []);

    const getTags = async () => {
        axios.get("api/tags")
            .then(response => {
                setTags(response.data.sort(alphabeticSort("name")));
            }).
            catch(err => {
                console.log(err);
                document.getElementById("fail").style = "display: block !important";
                document.getElementById("failspan").innerText = "Error Getting Tags";
            }
        );
    }

    function createTag() {
        const tagName = document.getElementById("tagBox").value;
        if (tagName === null) {
            return;
            //alert?
        }
        //Function to create a tag in the database through an axios call.
        const makeTag = async () => {
            const response = await axios({
                method: "post",
                url: '/api/tags',
                headers: {
                    'Content-Type': 'application/json',
                },
                data: JSON.stringify({
                    name: tagName,
                })
                }, true);

            if (response.status === 201) {
                document.getElementById("success").style = "display: block !important";
                document.getElementById("successspan").innerText = "Tags Created Successfully";
            }
            else {
                document.getElementById("fail").style = "display: block !important";
                document.getElementById("failspan").innerText = "Error Creating Tag";
            }
            getTags();
        }
        makeTag();
        document.getElementById("tagBox").value = "";
    }

    function assignTags() {
        const assign = async () => {
            const response = await axios({
                method: "put",
                url: `/api/tags/authors`,
                headers: {
                    'Content-Type': 'application/json',
                },
                data: JSON.stringify({
                    authors: selectedAuthors.map(a => a.id),
                    tags: selectedTags.map(t => t.id)
                  })
              }, true);
            if (response.status === 200) {
                document.getElementById("success").style = "display: block !important";
                document.getElementById("successspan").innerText = "Tags Assigned Successfully";
            }
            else {
                document.getElementById("fail").style = "display: block !important";
                document.getElementById("failspan").innerText = "Error: Failed to Assign Tags";
            }
        }
        assign();
    }

    function unassignTags() {
        const unassign = async () => {
            const response = await axios({
                method: "delete",
                url: `/api/tags/authors`,
                headers: {
                    'Content-Type': 'application/json',
                },
                data: JSON.stringify({
                    authors: selectedAuthors.map(a => a.id),
                    tags: selectedTags.map(t => t.id)
                  })
              }, true);
            if (response.status === 200) {
                document.getElementById("success").style = "display: block !important";
                document.getElementById("successspan").innerText = "Tags Unassigned Successfully";
            }
            else {
                document.getElementById("fail").style = "display: block !important";
                document.getElementById("failspan").innerText = "Error: Failed to Unassign Tags";
            }
        }
        unassign();
    }

    function deleteTags(){
        const deleteTag = async () => {
            const mapPromises = selectedTags.map(tag => {
                return axios.delete(`/api/tags/${tag.id}`).then(res => {
                    if (res.status != 200) {
                        document.getElementById("fail").style = "display: block !important";
                        document.getElementById("failspan").innerText = "Error: Failed to Delete Tags";
                    }
                });
            });
            Promise.all(mapPromises).then(() => {
                //would prefer to just call getTags(), but can't rerender Tags box, so deleted tags stay checked
                window.location.href = `/tags`;
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

    //Return the related HTML of the page.
    return (
        <div className="body">
            <div className="container">
                <div className="container">
                    <h3>Assign Tags to Authors</h3>
                </div>
                <div className="row">
                    <div className="alert alert-success alert-dismissible" role="alert" id="success" style={{ display: "none" }}>
                        <button className="close" type="button" data-dismiss="alert" onClick={hideSuccessAlert}><span>&times;</span></button> <span id="successspan">Tags Assigned Successfully.</span>
                    </div>
                </div>
                <div className="row">
                    <div className="alert alert-danger alert-dismissible" role="alert" id="fail" style={{ display: "none" }}>
                        <button className="close" type="button" data-dismiss="alert" onClick={hideFailAlert}><span>&times;</span></button> <span id="failspan">Error: No Tags Assigned.</span>
                    </div>
                </div>
                <div className="container border border-dark my-3 p-4 rounded">
                    <h4>
                        Authors
                    </h4>
                    <Autocomplete
                        multiple
                        id="checkboxes-authors"
                        options={authors}
                        disableCloseOnSelect
                        getOptionLabel={(option) => option.name}
                        renderOption={(props, option, { selected }) => (
                            <li {...props}>
                                <Checkbox
                                    icon={icon}
                                    checkedIcon={checkedIcon}
                                    style={{ marginRight: 8 }}
                                    checked={selected}
                                />
                                {option.name}
                            </li>
                        )}
                        onChange={(event, value) => setSelectedAuthors(value)}
                        style={{ width: 500 }}
                        renderInput={(params) => (
                            <TextField {...params} label="Select Authors" placeholder="Select Authors" />
                        )}
                    />
                </div>
                <div className="container border border-dark my-3 p-4 rounded">
                    <div className="row px-2 pb-2 d-flex">
                        <h4>
                            Tags
                        </h4>
                        <div className="d-flex px-3 align-items-right ml-auto">
                            <input type="type" className="form-control mr-2" id="tagBox" placeholder="New Tag" />
                            <button type="button" className="btn btn-danger btn-sm" onClick={createTag}>Create</button>
                        </div>
                    </div>
                    <div className="row px-2 pb-2 d-flex">
                        <Autocomplete
                            multiple
                            id="checkboxes-tags"
                            options={tags}
                            disableCloseOnSelect
                            getOptionLabel={(option) => option.name}
                            renderOption={(props, option, { selected }) => (
                                <li {...props}>
                                    <Checkbox
                                        icon={icon}
                                        checkedIcon={checkedIcon}
                                        style={{ marginRight: 8 }}
                                        checked={selected}
                                    />
                                    {option.name}
                                </li>
                            )}
                            onChange={(event, value) => setSelectedTags(value)}
                            style={{ width: 500 }}
                            renderInput={(params) => (
                                <TextField {...params} label="Select Tags" placeholder="Select Tags" />
                            )}
                        />
                        <button type="button" className="btn btn-danger btn-sm ml-2" onClick={deleteTags}>Delete</button>
                    </div>

                </div>

                <div className="container d-flex justify-content-end">
                    <button type="button" className="btn btn-danger btn-sm mr-2" onClick={assignTags}>Assign</button>
                    <button type="button" className="btn btn-danger btn-sm" onClick={unassignTags}>Unassign</button>
                </div>
            </div>
        </div>
    );
}

export default Tags;