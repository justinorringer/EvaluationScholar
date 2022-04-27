import React, {Component, Fragment} from "react";
import axios from 'axios';
import Pagination from "../components/pagination";
import TextField from '@mui/material/TextField';

class Papers extends Component {
    state = {currentPapers: [], currentPage: 1, totalPages: 2, perPage: 10, search: ''};
    
    setPapers(page) {
        const {perPage} = this.state;
        axios.get(`/api/papers?page=${page}&limit=${perPage}&include=authors&search=${this.state.search}`)
            .then(res => {
                this.setState({
                    currentPapers: res.data,
                    currentPage: page,
                    totalPages: parseInt(res.headers['total-pages'])
                });
            }).
            catch(err => {
                if (err.response.status === 404) {
                    this.setPapers(1);
                }
            }
        );
    }

    componentDidMount = () => {
        this.setPapers(1);
    }

    onPageChanged = newPage => {
        if (newPage === this.state.currentPage) {
            return;
        }

        this.setPapers(newPage);
    }

    deletePaper(id) {
        axios.delete(`/api/papers/${id}`)
            .then(res => {
                this.setPapers(this.state.currentPage);
            }).
            catch(err => {
                if (err.response.status === 404) {
                    this.setPapers(this.state.currentPage);
                }
            }
        );
    }


    searchChange = e => {
        this.setState({search: e.target.value});
    }

    searchSubmit = e => {
        e.preventDefault();
        this.setPapers(1);
    }

    render() {
        return (
            <div className="container mb-5">
                <div className="row d-flex flex-row py-5">
                    <div className="w-100 px-4 py-5 d-flex flex-row flex-wrap align-items-center justify-content-between">
                    <div className="d-flex flex-row align-items-center">
                        { this.currentPage && (
                        <span className="current-page d-inline-block h-100 pl-4 text-secondary">
                            Page <span className="font-weight-bold">{ this.currentPage }</span> / <span className="font-weight-bold">{ this.totalPages }</span>
                        </span>
                        ) }
                    </div>
                    <div className="d-flex flex-row py-4 align-items-center">
                        <Pagination pageNeighbors={2} currentPage={this.state.currentPage} totalPages={this.state.totalPages} onPageChanged={this.onPageChanged} />
                    </div>
                    </div>
                    <div className="w-100 px-4 py-5 d-flex flex-row flex-wrap">
                    {/* <div className="d-flex flex-row py-5 justify-content-center"> */}
                        <TextField label="Search Paper" inputProps={{ style: {textAlign: 'center'} }} className="col-8 px-2" value={this.state.search} onChange={this.searchChange}/>
                        <button type="button" class="col-1 btn btn-danger px-1" onClick={this.searchSubmit}>Search</button>
                    </div>
                    <table className="table table-borderless table-striped" id="paperTable">
                        <thead className="thead-dark">
                            <tr>
                                <th scope="col-6">Article</th>
                                <th scope="col-6">Authors</th>
                                <th scope="col-2">Year</th>
                                <th scope="col-2">Citations</th>
                                <th scope="col-2"></th>
                            </tr>
                        </thead>
                        <tbody id = "paperTableBody">
                            {this.state.currentPapers.map(paper => (
                                <tr key={paper.id}>
                                    <td>{paper.name}</td>
                                    <td>
                                        <ul>
                                            {paper.authors.map(author => (
                                                <li key={author.id}>{author.name}</li>
                                            ))}
                                        </ul>
                                    </td>
                                    <td>{paper.year}</td>
                                    <td>{paper.latest_citation?.num_cited}</td>
                                    <td>
                                        <button className="btn btn-danger" onClick={() => this.deletePaper(paper.id)}>Delete</button>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>
        );
      }
}

export default Papers;