import React, { useState, useEffect } from "react";
import axios from 'axios';

function Issues() {

    const [issues, setIssues] = useState([]);

    const test = () => {
        axios.get(`/api/issues`)
            .then(response => {
                setIssues(response.data);
            })
            .catch(err => {
                console.log(err);
            });
    }

    useEffect(() => {
        test();
    }, []);

    checkForIssues();

    function checkForIssues() {
        if (issues.length !== 0) {
            console.log(issues.length);
            console.log(issues);
            hideAlert();
        }
    }

    function resolveIssue(issue_id, scholar_id) {
        axios.post(`/api/issues/${issue_id}/resolve?correct_scholar_id=${scholar_id}`, { 'correct_scholar_id': scholar_id })
            .then(res => {
                if (res.status === 200) {
                    console.log("Issue resolved!");
                    getIssues();
                    checkForIssues();
                }
            })
            .catch(err => {
                if (err.response.status === 404) {
                    console.log(err);
                }
            });
    };

    function dismissIssue(issue_id) {
        axios.delete(`/api/issues/${issue_id}`)
            .then(res => {
                if (res.status === 200) {
                    console.log("Issure dismissed!");
                    getIssues();
                    checkForIssues();

                }
            })
            .catch(err => {
                if (err.response.status === 404) {
                    console.log(err);
                }
            });
    }

    function getIssues() {
        axios.get(`/api/issues`)
            .then(response => {
                setIssues(response.data);
            })
            .catch(err => {
                console.log(err);
            });
    }

    function hideAlert() {
        document.getElementById("alert").style = "display: none !important";
    }

    return (
        <div className="body">
            <div className="container mb-5">
                <h3>Ambiguous Paper Issues</h3>
                <div className="row pt-3 d-flex justify-content-center">
                    <div className="alert alert-primary alert-dismissible pt-2" role="alert" id="alert" style={{ display: "block" }}>
                        <button className="close" type="button" onClick={hideAlert}><span>&times;</span></button> No issues found!
                    </div>
                </div>

                {issues.map(issue => (
                    <div key={issue.id} className="container border border-dark my-3 p-4 rounded">
                        <div className="col-md-12 text-right">
                            <button className="btn btn-danger" onClick={() => { dismissIssue(issue.id) }}>Dismiss Issue</button>
                        </div>
                        <div>
                            <h4>Paper Title - {issue.title_query}</h4>
                            <h4>Author - {issue.author.name}</h4>
                        </div>
                        <table className="table table-borderless table-striped">
                            <thead className="thead-dark">
                                <tr>
                                    <th scope="col-6"> Article</th>
                                    <th scope="col-2"> Year</th>
                                    <th scope="col-2">Co-Authors</th>
                                    <th scope="col-2"> Citations</th>
                                    <th scope="col-2"></th>
                                </tr>
                            </thead>
                            <tbody>
                                {issue.paper_choices.map(choice => (
                                    <tr key={choice.id}>
                                        <td>{choice.name}</td>
                                        <td>{choice.year}</td>
                                        <td>
                                            <ul>
                                                {choice.author_names.map(author => (
                                                    <li>{author}</li>
                                                ))}
                                            </ul>
                                        </td>
                                        <td>{choice.citations}</td>
                                        <td><button className="btn btn-danger" onClick={() => { resolveIssue(issue.id, choice.scholar_id) }}>Select</button></td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                        <div>
                        </div>
                        <br />
                    </div>
                ))}
            </div>
        </div>


    )
}
export default Issues;