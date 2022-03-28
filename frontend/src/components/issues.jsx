import React from "react";
import axios from 'axios';

function Issues() {
  //Return the related HTML of the page.
  return (
    <div className="body">
        <div className="container">
            <h2>Issues</h2>
        </div>
        <div className="container my-3 p-4 border border-5 border-dark">
            {/**<button type="button" className="close btn-small float-right" aria-label="Close">&times;</button>*/}

            <h3>Ambiguous Search</h3>

            <p>Inputed Title: Ambiguous</p><br />

            <button type="button" className="btn btn-success btn-sm float-right">Correct</button>
            <button type="button" className="btn btn-danger btn-sm float-right pl-1">Dismiss</button>

            <h5>Select the Best Match</h5>
            <input type="radio" aria-label="Checkbox for following text input" /> Option 1<br />
            <input type="radio" aria-label="Checkbox for following text input" /> Option 2<br />
            <input type="radio" aria-label="Checkbox for following text input" /> Option 3 <br />
            <input type="radio" aria-label="Checkbox for following text input" /> None of the Suggested <br /><br />

        </div>

        <div className="container my-3 p-4 border border-5 border-dark">
            <h3>Paper Not Found</h3>

            <p>Inputed Title: Paper?</p><br />

            <input type="text" className="form-control" id="validationServer01" placeholder="Correct Title" required></input>
            
            <button type="button" className="btn btn-success btn-sm float-right">Correct</button>
            <button type="button" className="btn btn-danger btn-sm float-right">Dismiss</button>
            
            <div className="valid-feedback">
                Looks good!
            </div>

            <br />
            
        </div>
    </div>
  );
}

export default Issues;