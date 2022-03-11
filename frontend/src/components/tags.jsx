import React from "react";
import axios from 'axios';

//Function to create an HTML representation of the Query page for the app
//while also handling dynamic calls to the API.
//Authors: Gage Fringer, Carter Thunes, Justin Orringer
function Tags() {

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
                    <ul className="col-count-3">
                        <li>
                            <label className="container">
                                <input type="checkbox" checked="checked"/>
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
            <h3>
                Tags
            </h3>

            <div className="row">
                <div className="col-12">
                    <ul className="col-count-3">
                        <li>
                            <label className="container">Tag 1
                                <input type="checkbox" checked="checked" />
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
            <div className="row">
                <div className="form-group">
                    <input type="type" className="form-control" id="exampleInputPassword1" placeholder="Tag" />
                </div>
                <button type="submit" className="btn btn-primary">Submit</button>
            </div>
        </div>

        <div className="container">
            <button type="button" className="btn btn-danger btn-sm float-right" style="{{margin-left: 90%}}">Submit</button>
        </div>
    </div>
  );
}

export default Tags;