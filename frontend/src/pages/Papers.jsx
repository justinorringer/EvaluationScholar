import React, { Component, Fragment } from "react";
import axios from 'axios';
import Pagination from "../components/pagination";
import TextField from '@mui/material/TextField';

class Papers extends Component {
    state = { currentPapers: [], currentPage: 1, totalPages: 2, perPage: 10, search: '' };

    setPapers(page) {
        const { perPage } = this.state;
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
        this.setState({ search: e.target.value });
    }

    searchSubmit = e => {
        e.preventDefault();
        this.setPapers(1);
    }

    render() {
        return (
            <div className="body">
                <div className="container">
                    <h3>Papers</h3>
                    <div className="row d-flex flex-row">
                        <div className="w-100 py-3 d-flex flex-row flex-wrap align-items-center justify-content-between">
                            <div className="align-items-center">
                                <TextField label="Search Paper" className="pr-2 btn-lg" style={{ width: 500 }} value={this.state.search} onChange={this.searchChange} />
                                <button type="button" class="btn btn-danger btn-lg" onClick={this.searchSubmit}>Search</button>
                            </div>
                            <div className="align-items-center">
                                <Pagination pageNeighbors={2} currentPage={this.state.currentPage} totalPages={this.state.totalPages} onPageChanged={this.onPageChanged} />
                            </div>
                        </div>
                        <table className="table table-borderless table-striped" id="paperTable">
                            <thead className="thead-dark">
                                <tr>
                                    <th className="col-6" scope="col">Article</th>
                                    <th className="col-3" scope="col">Authors</th>
                                    <th className="col-1" scope="col">Year</th>
                                    <th className="col-1" scope="col">Citations</th>
                                    <th className="col-1" scope="col"></th>
                                </tr>
                            </thead>
                            <tbody id="paperTableBody">
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
            </div>

        );
    }
}

export default Papers;