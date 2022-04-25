import React from 'react';
import axios from 'axios';

function Tasks() {
    async function deleteTask(id) {
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

    let create_papers = [];

    const getCreateTasks = async () => {

        console.log("getCreateTasks starts");
        try {
            const response = await axios.get('/api/tasks?type=create_paper_task', { mode: 'cors' });
            console.log(response.data);
            if (response.status === 200)
                create_papers = response.data;
            console.log({ response, create_papers })
        }
        catch (e) {
            console.log(e);
        }

        const createTableBody = document.getElementById("createTableBody");
        const createTable = document.getElementById("createTable");

        createTableBody.innerHTML = "";

        create_papers.forEach(paper => {
            hideAlert();
            createTable.style = "display: block !important";
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

    async function updateLabel() {
        try {
            const response = await axios.get('/api/task_manager/update_period', { mode: 'cors' });
            console.log(response.data);
            if (response.status === 200)
                var label = document.getElementById("updateCounter");
            label.innerHTML = "Current Update Period: " + response.data.value + " days";
        }
        catch (e) {
            console.log(e);
        }
    }

    updateLabel();

    async function performUpdate() {
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
    }

    function hideAlert() {
        document.getElementById("alert").style = "display: none !important";
    }

    return (
        <div className="body">
            <div className="container pt-3">
                <h3>Queued Paper Creations</h3>
            </div>
            <div className="container pt-3">
                <table className="table table-borderless table-striped" id="createTable" style={{display: "none"}}>
                    <colgroup>
                        <col class="col-md-7" />
                        <col class="col-md-3" />
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
                    </tbody>
                </table>
                <div className="row pt-3 pr-3">
                    <div className="alert alert-warning alert-dismissible pt-2" role="alert" id="alert" style={{ display: "block" }}>
                        <button className="close" type="button" onClick={hideAlert}><span>&times;</span></button> No tasks found. Upload or search for papers for an author to see scheduled tasks.
                    </div>
                </div>
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
        </div>
    );
}

export default Tasks;