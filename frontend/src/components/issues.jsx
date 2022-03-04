import React from "react";
import axios from 'axios';

function Issues() {
  //Return the related HTML of the page.
  return (
    <div className="body">
        <div className="container pt-4">
            <h2>Issues</h2>
        </div>
        <div className="container border my-3 p-4">
            {/**<button type="button" className="close btn-small float-right" aria-label="Close">&times;</button>*/}

            <h3>Ambiguous Search</h3>

            <p>Inputed Title: Ambiguous</p><br />

            <h5>Select the Best Match</h5>
            <input type="radio" aria-label="Checkbox for following text input" /> Option 1<br />
            <input type="radio" aria-label="Checkbox for following text input" /> Option 2<br />
            <input type="radio" aria-label="Checkbox for following text input" /> Option 3 <br />
            <input type="radio" aria-label="Checkbox for following text input" /> None of the Suggested <br /><br />

            <button type="button" className="btn btn-success btn-sm float-right">Correct</button>
            <button type="button" className="btn btn-danger btn-sm float-right pl-1">Dismiss</button>
        </div>

        <div className="container border my-3 p-4">
            <h3>Paper Not Found</h3>

            <p>Inputed Title: Paper?</p><br />

            <input type="text" className="form-control" id="validationServer01" placeholder="Correct Title" required></input>
            <div className="valid-feedback">
                Looks good!
            </div>

            <br />

            <button type="button" className="btn btn-success btn-sm float-right">Correct</button>
            <button type="button" className="btn btn-danger btn-sm float-right">Dismiss</button>
        </div>
    </div>
  );
}

export default Issues;