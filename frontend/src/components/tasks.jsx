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
      async function deleteTask(id){
          console.log("attempt to delete " + id);

          const response = await axios({
            method: "delete",
            url: '/api/tasks/' + id,
            headers: {
              'Access-Control-Allow-Origin': '*',
              'Content-Type': 'application/json',
    
            },
          
            mode: 'cors'
          }, true);

          console.log(response);
          getCreateTasks();
      }

      //No way to actually test this in production quite yet...
      let create_papers = [];
      //Function to make an API call to gather a list of all current authors.
      const getCreateTasks = async () => {
        console.log("getCreateTasks starts");
        try {
            const response = await axios.get('/api/tasks?type=create_paper_task', {mode:'cors'});
            console.log(response.data);
            if (response.status === 200)
                create_papers = response.data;
            console.log({response, create_papers})
        }
        catch (e) {
            console.log(e);
        }

        

        const createTableBody = document.getElementById("createTableBody");
        const createTable = document.getElementById("createTable");

        createTableBody.innerHTML = "";

        create_papers.forEach(paper => {
          //console.log(paper.paper.name);
          //console.log(paper.date);
          var row = document.createElement("tr");
          var paperName = document.createElement("td");
          var deleteButton = document.createElement("td");
          var buttonInner = document.createElement("button");
          paperName.innerText = paper.paper_title;
          paperName.id = paper.id;

          buttonInner.type = "button";
          buttonInner.innerText = "Cancel";
          buttonInner.className = "btn btn-danger btn-sm";
          buttonInner.value = paper.id;

          buttonInner.onclick = () => { deleteTask(paper.id); };

          deleteButton.appendChild(buttonInner);

          row.appendChild(paperName);
          row.appendChild(deleteButton);
          createTableBody.appendChild(row);
        });
        console.log("getCreateTasks ends");
      } 

      getCreateTasks();

      let papers = [];
      //Function to make an API call to gather a list of all current authors.
      const getTasks = async () => {
        console.log("getTasks starts");
        try {
            const response = await axios.get('/api/tasks?type=update_citations_task', {mode:'cors'});
            console.log(response.data);
            if (response.status === 200) {
              papers = response.data;
              const taskTableBody = document.getElementById("taskTableBody");
              const taskTable = document.getElementById("taskTable");

              papers.forEach(paper => {
                console.log(paper.paper.name);
                console.log(paper.date);
                var row = document.createElement("tr");
                var paperName = document.createElement("td");
                var updateTime = document.createElement("td");
                //var deleteButton = document.createElement("td");
                //var buttonInner = document.createElement("button");
                paperName.innerText = paper.paper.name;
                updateTime.innerText = paper.date;

                //buttonInner.type = "button";
                //buttonInner.innerText = "Delete";
                //buttonInner.className = "btn btn-danger btn-sm";

                //deleteButton.appendChild(buttonInner);

                row.appendChild(paperName);
                row.appendChild(updateTime);
                //row.appendChild(deleteButton);
                taskTableBody.appendChild(row);
              });
              console.log("getTasks ends");
            }

            console.log({response, papers})
        }
        catch (e) {
            console.log(e);
        }
      } 

      getTasks();

      async function updateLabel(){
        try {
          const response = await axios.get('/api/task_manager/update_period', {mode:'cors'});
          console.log(response.data);
          if (response.status === 200)
            var label = document.getElementById("updateCounter");
            label.innerHTML = "Current Update Period: " + response.data.value + " days";
          console.log({response, papers})
        }
        catch (e) {
          console.log(e);
        }
      }

      updateLabel();

      async function performUpdate(){
        var period = document.getElementById("updatePeriod").value;

        const response = await axios({
          method: "put",
          url: '/api/task_manager/update_period',
          headers: {
            'Access-Control-Allow-Origin': '*',
            'Content-Type': 'application/json',
  
          },
        
          //make sure to serialize your JSON body
          data: JSON.stringify({
            value: period,
          }), mode: 'cors'
        }, true);

        console.log(response);

        updateLabel();
        //var label = document.getElementById("updateCounter");
        //label.innerHTML = "Current Update Period: " + period + " days";
      }

  return (
    <div className="body">
        <div className="container pt-3">
            <h3>Queued Paper Creations</h3>
        </div>
        <div className="container pt-3">
        <table className="table table-borderless table-striped" id="createTable">
              <colgroup>
                  <col class="col-md-7"/>
                  <col class="col-md-3"/>
              </colgroup>
              <thead className="thead-dark">
                <tr>
                  <th>
                    Paper Title
                  </th>
                  <th>
                    Cancel
                  </th>
                </tr>
              </thead>
              <tbody id="createTableBody">
                <tr>
                  <td>
                    First Paper
                  </td>
                  <td>
                    <button type="button" className="btn btn-danger btn-sm">Cancel</button>
                  </td>
                </tr>
              </tbody>
            </table>
        </div>
        
        <div className="container pt-3">
          <table>
            <tr>
              <td>
                <label id="updateCounter">Current Update Period: ___ days</label> 
              </td>
            </tr>
            <tr>
              <td>
                <label>New Update Period (in Days): </label>
              </td>
              <td>
                <input type="text" placeholder="Insert Number Here" id="updatePeriod"></input>
              </td>
              <td>
                <button type="button" onClick={performUpdate} className="btn btn-sm btn-danger">
                  Edit
                </button>
              </td>
            </tr>
          </table>
        </div>

        <div className="container pt-3">
            <h3>Queued Paper Updates</h3>
        </div>
        <div className="container pt-3">
        <table className="table table-borderless table-striped" id="taskTable">
              <colgroup>
                  <col class="col-md-7"/>
                  <col class="col-md-3"/>
              </colgroup>
              <thead className="thead-dark">
                <tr>
                  <th>
                    Paper Title
                  </th>
                  <th>
                    Update Time
                  </th>
                </tr>
              </thead>
              <tbody id="taskTableBody">
              </tbody>
            </table>

        </div>
    </div>
  );
}

export default Tasks;