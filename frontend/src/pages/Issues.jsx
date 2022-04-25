import React from "react";
import axios from 'axios';

export default class Issues extends React.Component{
    state = {issues: []};

    async componentDidMount(){
        axios.get(`/api/issues`, { mode: 'cors' }).then(res => {
            if(res.status == 200){
                this.setState({
                    issues: res.data
                });
            }
        }).
        catch(err => {
            if (err.response.status === 404) {
                console.log(err);
            }
        });
    }

    resolveIssue(issue_id, scholar_id) {
        axios.post(`/api/issues/${issue_id}/resolve?correct_scholar_id=${scholar_id}`, {'correct_scholar_id': scholar_id}).then(res => {
            if(res.status == 200){
                console.log("Issue resolved!");
                this.componentDidMount();
            }
        }).
        catch(err => {
            if (err.response.status === 404) {
                console.log(err);
            }
        });
    }

    deleteIssue(issue_id){
        axios.delete(`/api/issues/${issue_id}`).then(res => {
            if(res.status == 200){
                console.log("Issure deleted!");
                this.componentDidMount();
            }
        }).
        catch(err => {
            if(err.response.status === 404){
                console.log(err);
            }
        });
    }

    render() {
        return (
            <div className="container mb-5">
                <h1>Ambigious Paper Issues</h1>
                {this.state.issues.map(issue => (
                    <div key={issue.id} className="container border border-dark my-3 p-4 rounded">
                        <div className="col-md-12 text-right">
                            <button className="btn btn-danger" onClick={() => this.deleteIssue(issue.id)}>Delete Issue</button>
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
                                    <th scope="col-2"> Citations</th>
                                    <th scope="col-2"></th>
                                </tr>
                            </thead>
                            <tbody>
                                {issue.paper_choices.map(choice => (
                                    <tr key={choice.id}>
                                        <td>{choice.name}</td>
                                        <td>{choice.year}</td>
                                        <td>{choice.citations}</td>
                                        <td><button className="btn btn-danger" onClick={() => this.resolveIssue(issue.id ,choice.scholar_id)}>Select</button></td>
                                        
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
        )
    }
}