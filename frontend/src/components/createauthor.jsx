import React from "react";
import axios from 'axios';

//Authors: Carter Thunes, Justin Orringer
function CreateAuthor() {
    
  //Return the related HTML of the page.
  return (
    <div className="body">
        <div className="container">
            <div className="row pl-3">
                <label>Enter Author Name: &nbsp;</label>
                <input className="mx-3" type="text" id="authName"></input>
                <button type="button" class="btn btm-sm btn-danger">Search Google Scholar</button>
            </div>
        </div>

        <div className="container pt-4" id="optionsLabel">
            <h4>Author Options:</h4>
        </div>
        <div className="container border my-3 p-4">
            <div className="list-group">
                <a className="list-group-item list-group-item-action flex-column align-items-start">
                    <div className="d-flex w-100 justify-content-between">
                        <h5 className="mb-1 py-2">Author Name</h5>
                        <small className="text-muted">Insitution</small>
                    </div>
                </a>
                <a className="list-group-item list-group-item-action flex-column align-items-start">
                    <div className="d-flex w-100 justify-content-between">
                        <h5 className="mb-1 py-2">Author Name</h5>
                        <small className="text-muted">Insitution</small>
                    </div>
                </a>
                <a className="list-group-item list-group-item-action flex-column align-items-start">
                    <div className="d-flex w-100 justify-content-between">
                        <h5 className="mb-1 py-2">Author Name</h5>
                        <small className="text-muted">Insitution</small>
                    </div>
                </a>
            </div>
        </div>
    </div>
    
  );
}

export default CreateAuthor;