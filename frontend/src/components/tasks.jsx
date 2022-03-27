import React from "react";
import axios from 'axios';

function Tasks() {
  //Return the related HTML of the page.

  /*
              <h3>Job Type</h3>
            <button type="button" className="btn btn-danger btn-sm float-right">Cancel Job</button>

            <p>Importance: 0</p>
            <p>Date Scheduled: <b>Bleh</b></p>

                        
  */
  return (
    <div className="body">
        <div className="container">
            <h3>Queued Paper Updates</h3>
        </div>
        <div className="container pt-3">
        <table className="table table-borderless table-striped">
              <colgroup>
                  <col class="col-md-7"/>
                  <col class="col-md-2"/>
                  <col class="col-md-1"/>
              </colgroup>
              <thead className="thead-dark">
                <tr>
                  <th>
                    Paper Title
                  </th>
                  <th>
                    Update Time
                  </th>
                  <th>
                    Delete
                  </th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>
                    First Paper
                  </td>
                  <td>
                    01-01-0001 12:00
                  </td>
                  <td>
                    X
                  </td>
                </tr>
                <tr>
                  <td>
                    Second Paper
                  </td>
                  <td>
                    01-02-0001 12:00
                  </td>
                  <td>
                    X
                  </td>
                </tr>
              </tbody>
            </table>

        </div>
    </div>
  );
}

export default Tasks;