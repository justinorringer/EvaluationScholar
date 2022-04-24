import React, { useState, useEffect } from 'react';
import axios from 'axios';
import TextField from '@mui/material/TextField';
import Autocomplete from '@mui/material/Autocomplete';

//Function to create an HTML representation of the Query page for the app
//while also handling dynamic calls to the API.
//Authors: Gage Fringer, Carter Thunes, Justin Orringer
function Query() {
    //Variable to hold list of current authors in the system
    const [authors, setAuthors] = useState([]);

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

    //upon page load
    useEffect(() => {
        axios.get("api/authors")
            .then(response => {
                setAuthors(response.data.sort(alphabeticSort("name")));
            }).
            catch(err => {
                console.log(err);
            }
            );
    }, []);

    //Return the related HTML of the page.
    return (
        <div className="body">
            <div className="container" id="container">
                <div className="justify-content-center page-header">Select Author</div>
                <br />
                <div className="row">
                    <div className="col-10 gx-4 gy-4">
                        <Autocomplete
                            disablePortal
                            id="combo-box-demo"
                            options={authors}
                            getOptionLabel={(option) => option.name}
                            onChange={(event, newAuthor) => {window.location.href = `/author/${newAuthor.id}`;}}
                            sx={{ width: 300 }}
                            renderInput={(params) => <TextField {...params} label="Author" />}
                        />
                    </div>
                </div>
                <br />
                <div className="row pl-3">
                    <label>Don't see your author?</label>
                    <pre> </pre>
                    <a id="toCreateAuthor" href="/createauthor">Make a new author.</a>
                </div>
            </div>
            <hr />
        </div>
    );
}

export default Query;