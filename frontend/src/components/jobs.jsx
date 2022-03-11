import React from "react";
import axios from 'axios';

function Jobs() {
  //Return the related HTML of the page.
  return (
    <div className="body">
        <div className="container pt-3">
            <h1>Queued Jobs</h1>
        </div>
        <div className="container my-3 p-4 border border-5 border-dark">
            <h3>Job Type</h3>

            <button type="button" className="btn btn-danger btn-sm float-right">Cancel Job</button>

            <p>Importance: 0</p>
            <p>Date Scheduled: <b>Bleh</b></p>

        </div>
        <div className="container my-3 p-4 border border-5 border-dark">
            {/* <button type="button" className="close btn-small float-right" aria-label="Close">&times;</button> -->*/}

            <h3>Job Type</h3>

            <button type="button" className="btn btn-danger btn-sm float-right">Cancel Job</button>

            <p>Importance: 0</p>
            <p>Date Scheduled: <b>Bleh</b></p>
            
        </div>
    </div>
  );
}

export default Jobs;