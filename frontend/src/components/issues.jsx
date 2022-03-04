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

            <h3 className="float-left">Ambiguous Search</h3>

            <p>Inputed Title: <b>Ambiguous</b></p><br />

            <h5>Select the Best Match</h5>
            <input type="radio" aria-label="Checkbox for following text input"> Option 1 </input><br />
            <input type="radio" aria-label="Checkbox for following text input"> Option 2 </input><br />
            <input type="radio" aria-label="Checkbox for following text input"> Option 3 </input><br />
            <input type="radio" aria-label="Checkbox for following text input"> None of the Suggested </input><br /><br />

            <button type="button" className="btn btn-success btn-sm float-right">Correct</button>
            <button type="button" className="btn btn-danger btn-sm float-right">Dismiss</button>
        </div>

        <div className="container border my-3 p-4">
            <h3>Paper Not Found</h3>

            <p>Inputed Title: <b>Paper?</b></p><br />

            <input type="text" className="form-control" id="validationServer01" placeholder="Correct Title" required />
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