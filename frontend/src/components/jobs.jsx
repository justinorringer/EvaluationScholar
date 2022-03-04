import React from "react";
import axios from 'axios';

function Jobs() {
  //Return the related HTML of the page.
  return (
    <div className="body">
        <div className="container pt-3">
            <h1>Queued Jobs</h1>
        </div>
        <div className="container border-warning my-3 p-4">
            <h3>Job Type</h3>

            <p>Importance: 0</p>
            <p>Date Scheduled: <b>Bleh</b></p>

            <button type="button" className="btn btn-danger btn-sm float-right">Cancel Job</button>
        </div>
        <div className="container border-warning my-3 p-4">
            {/* <button type="button" className="close btn-small float-right" aria-label="Close">&times;</button> -->*/}

            <h3>Job Type</h3>

            <p>Importance: 0</p>
            <p>Date Scheduled: <b>Bleh</b></p>

            <button type="button" className="btn btn-danger btn-sm float-right">Cancel Job</button>
        </div>
    </div>
  );
}

export default Jobs;