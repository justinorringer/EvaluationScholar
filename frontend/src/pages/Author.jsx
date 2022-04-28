import React, { useState } from "react";
import axios from 'axios';
import { useParams } from 'react-router-dom';

// Each author has an Author page with their tags and articles listed.
function Author() {

    const authorID = useParams().id;

    let authorName = "";

    let authorScholarID = "";

    let boolUploaded_papers = false;


    //Variable to hold list of papers related to an author
    let papers = [];
    let tags = [];
    let checkedPapers = [];
    let checkedPapersToBeScraped = [];
    let paperTitlesForScraping = [];


    //Function to make the API call to gather the papers of a specific author.
    function getAuthor() {
        const getPapers = async () => {
            try {
                const response = await axios.get(`/api/authors/${authorID}/papers`, { mode: 'cors' });
                if (response.status === 200)
                    papers = response.data;
            }
            catch (e) {
                console.log("Failed to get papers.");
            }
            const paperTableBody = document.getElementById("paperTableBody");
            const paperTable = document.getElementById("paperTable");
            if (document.getElementById("alertid")) {
                document.getElementById("alertid").remove();
            }
            if (papers.length > 0) {
                paperTableBody.innerHTML = "";
                paperTable.style = "display: block !important";
                papers.sort(function(a, b) { return b.latest_citation.num_cited - a.latest_citation.num_cited});
            } else {
                paperTable.style = "display: none !important";
                var alert = document.createElement("div");
                alert.className = "alert alert-warning alert-dismissable";
                alert.role = "alert";
                alert.innerText = "No papers found! Upload some on the left!";
                alert.id = "alertid";
                document.getElementById("articles").appendChild(alert);
                return;
            }
            papers.forEach(paper => {
                var row = document.createElement("tr");
                var article = document.createElement("td");
                var year = document.createElement("td");
                var citations = document.createElement("td");
                var checkBox = document.createElement("td");

                let input = document.createElement("input");
                input.className = "checkbox";
                input.type = "checkbox";
                input.id = "p" + paper.id;
                input.onclick = function () { checkedPaper(input.id, checkedPapers) };
                checkBox.appendChild(input);

                article.innerText = paper.name;
                year.innerText = paper.year;
                citations.innerText = paper.latest_citation.num_cited;
                row.appendChild(article);
                row.appendChild(year);
                row.appendChild(citations);
                row.appendChild(checkBox);
                paperTableBody.appendChild(row);
            });
        }
        const getTags = async () => {
            try {
                const response = await axios.get(`/api/authors/${authorID}/tags`, { mode: 'cors' });
                if (response.status === 200)
                    tags = response.data;
            }
            catch (e) {
                console.log("Failed to get tags.");
            }
            let tagList = document.getElementById("Tags");
            tags.forEach(tag => {
                // fill in the list of tags
                var tagElement = document.createElement("li");
                tagElement.innerText = tag.name;
                tagList.appendChild(tagElement);
            });
        }
        const getAuthorInfo = async () => {
            try {
                const response = await axios.get(`/api/authors/${authorID}`, { mode: 'cors' });
                if (response.status === 200) {
                    authorName = response.data.name;
                    boolUploaded_papers = response.data.uploaded_papers;
                    if (response.data.scholar_id) {
                        authorScholarID = response.data.scholar_id;
                    } else {
                        document.getElementById("gslink").remove();
                    }


                    //create HTML link element for this, do same thing as author name.

                    var authorHeader = document.getElementById("authorName");
                    authorHeader.innerText = authorName;

                    var flagHeader = document.getElementById("flag");

                    if (boolUploaded_papers) {
                        flagHeader.style = "display: block !important";
                    }
                }
            }
            catch (e) {
                console.log("Failed to get author info.");
            }
        }
        getAuthorInfo();
        getPapers();
        getTags();
    }

    getAuthor();

    function populateUpdateModal(papers) {
        const modalTableBody = document.getElementById("modalTableBody");
        const modalTable = document.getElementById("modalTable");

        papers.forEach(paper => {
            var row = document.createElement("tr");
            var article = document.createElement("td");
            var checkBox = document.createElement("td");

            let input = document.createElement("input");
            input.className = "checkbox";
            input.type = "checkbox";
            input.checked = "true";
            input.id = "p" + paper.id;
            input.onclick = function () { checkedPaper(input.id, papers) };
            checkBox.appendChild(input);

            article.innerText = paper.title;

            row.appendChild(article);
            row.appendChild(checkBox);
            modalTableBody.appendChild(row);
        });

    }
    //Function to get called by the download button so that a CSV is generated for the user, now tied to checkboxes
    function htmlToCSV() {

        var output = ["Article,Year,CitationCount\n"];

        var csv_file, download_link;

        let name = authorName;

        const getPapers = async () => {
            try {
                const response = await axios.get(`/api/authors/${authorID}/papers`, { mode: 'cors' });
                if (response.status === 200)
                    papers = response.data;
            }
            catch (e) {
                console.log("Failed to get papers.");
            }
        }
        getPapers();
        console.log(papers);
        /*        try {
                    const response = await axios.get(`/api/authors/${id}/papers`, {mode:'cors'});
                    if (response.status === 200)
                        papers = papers.concat(response.data);//= response.data;
                    //console.log({response, papers});
                }
                catch (e) {
                    console.log(e.getMessage);
                }
        */
        papers.forEach(paper => {
            let article = paper.name;
            let year = paper.year;
            let citations = paper.latest_citation.num_cited;

            let new_string = "\"" + article + "\"," + year + "," + citations + "\n";
            output.push(new_string);

        });

        csv_file = new Blob(output, { type: "text/csv" });

        download_link = document.createElement("a");

        download_link.download = name + ".csv";

        download_link.href = window.URL.createObjectURL(csv_file);

        download_link.style.display = "none";

        document.body.appendChild(download_link);

        download_link.click();

    }
    // Function for adding new articles on click
    //Variable to hold data from a file selected to be read in.

    //Object to hold the data getting pulled, both a name string and institution string

    //Method to handle the upload of a file
    //and also call other functions necessary for this page

    function upload() {
        var formData = new FormData();
        formData.append("file", document.getElementById('myfile').files[0])
        const postPaperTasks = async () => {
            try {
                const response = await axios.post(`/api/tasks/create-papers?author_id=${authorID}`, formData, {
                    headers: {
                        'Access-Control-Allow-Origin': '*',
                        'Content-Type': 'multipart/form-data',
                    },
                    mode: 'cors'
                }, true);
                if (response.status === 201) {
                    document.getElementById("success").style = "display: block !important";
                } else {
                    document.getElementById("fail").style = "display: block !important";
                }
            }
            catch (e) {
                console.log("Failed to upload file.");
            }
        }
        postPaperTasks();
    }

    function deleteAuthor() {
        const deleteAnAuthor = async () => {
            await axios.delete(`/api/authors/${authorID}`, { mode: 'cors' }).then(res => {
                if (res.status === 200) {
                    console.log("Deleted author");
                }
                else {
                    console.log("Error deleting author");
                }
                window.location.href = `/`;
            });
        }
        deleteAnAuthor();
    }

    function checkedPaper(id, list) {
        var checkBox = document.getElementById(id);
        if (checkBox.checked === true) {
            list.push(id.substring(1));
            console.log(list);
        } else {
            const index = list.indexOf(id.substring(1));
            list.splice(index, 1);
            console.log(list);
        }
    }

    function deletePapers() {

        const deletePaper = async () => {
            const mapPromises = checkedPapers.map(paper => {
                return axios.delete(`/api/authors/${authorID}/papers/${paper}`, { mode: 'cors' }).then(res => {
                    if (res.status === 200) {
                        console.log("Deleted paper");
                    }
                    else {
                        console.log("Error deleting paper");
                    }
                });
            });
            Promise.all(mapPromises).then(() => {
                checkedPapers = [];
                getAuthor();
            })
        }

        deletePaper();

    }

    function scrapePapersFromProfile() {
        let scrapedPapers = [];
        const scrapePaper = async () => {
            await axios.get(`/api/scraping/profiles/${authorScholarID}?all_papers=true`)
                .then(res => {
                    if (res.status === 200) {
                        scrapedPapers = res.data;

                        console.log("scraped Papers!");
                        checkedPapersToBeScraped = scrapedPapers['papers'];

                        populateUpdateModal(checkedPapersToBeScraped);


                        checkedPapersToBeScraped.forEach(paper =>
                            paperTitlesForScraping.push(paper.title));
                    }
                })
                .catch(err => {
                    if (err.response.status === 404) {
                        console.log(err);
                    }
                });
        };
        scrapePaper();
    }

    function createTaskFromList() {
        const addTasks = async () => {
            await axios.post(`/api/tasks/create-papers-list?author_id=${authorID}`, paperTitlesForScraping)
                .then(res => {
                    if (res.status === 201) {
                        console.log("Added the Papers!");
                        document.getElementById("successScraping").style = "display: block !important";
                    }
                })
                .catch(err => {
                    if (err.response.status === 404) {
                        console.log(err);
                        document.getElementById("failScraping").style = "display: block !important";
                    }
                });
        };
        addTasks();

    }

    function redirectToTags() {
        window.location.href = `/tags`;
    }


    function googleScholarRedirect() {
        window.open(
            "https://scholar.google.com/citations?hl=en&oi=ao&user=" + authorScholarID,
            '_blank'
        );
    }

    function hideSuccessAlert() {
        document.getElementById("success").style = "display: none !important";
    }

    function hideFailAlert() {
        document.getElementById("fail").style = "display: none !important";
    }

    // HTML by Justin Orringer
    return (
        <div className="body">
            <div className="container">
                <div className="row d-flex" id="authorSidebar">
                    <div className="col-3" id="authorSidebar">
                        <div className="row">
                            <img className="border" id="profile" src="/images/generic.png" alt="" />
                        </div>
                        <div className="row pt-4" id="tagHeader">
                            <h4>Tags</h4>
                            <div>
                                <button id="linkToTags" type="button" className="btn btn-success btn-sm ml-2" onClick={redirectToTags}>
                                    +
                                </button>
                            </div>
                        </div>
                        <div className="row pt-2">
                            <div className="container">
                                <ul id="Tags">
                                </ul>
                            </div>
                        </div>

                        <div className="row py-2 btn-toolbar mr-2">
                            <button id="UploadPapers" type="button" className="btn btn-primary btn-sm mr-2" data-toggle="modal" data-target="#uploadPapersModal">
                                Upload Papers
                            </button>
                            <button id="UpdatePapers" type="button" className="btn btn-primary btn-sm" data-toggle="modal" data-target="#updatePapersModal">
                                Scrape Papers
                            </button>
                        </div>

                        <div className="alert alert-warning row mr-3" role="alert" id="flag" style={{ display: 'none' }}> You have already added papers for this author.</div>

                        <div className="modal fade" id="uploadPapersModal" tabIndex="-1" role="dialog" aria-labelledby="uploadPapersModalTitle" aria-hidden="true">
                            <div className="modal-dialog modal-dialog-centered" role="document">
                                <div className="modal-content">
                                    <div className="modal-header">
                                        <h5 className="modal-title " id="uploadPapersModalLongTitle">Upload File with Paper Titles</h5>
                                        <button type="button" className="close" data-dismiss="modal" aria-label="Close">
                                            <span aria-hidden="true">&times;</span>
                                        </button>
                                    </div>
                                    <div className="modal-body">
                                        <div className="row pl-3">
                                            <label htmlFor="myfile">Select a file:&nbsp;</label>
                                            <input type="file" id="myfile" name="myfile" />
                                        </div>
                                    </div>
                                    <div className="modal-footer">
                                        <button type="button" className="btn btn-secondary" data-dismiss="modal">Cancel</button>
                                        <button id="uploadPapers" type="button" className="btn btn-success" data-dismiss="modal" onClick={upload}>Upload</button>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <div className="modal fade" id="updatePapersModal" tabIndex="-1" role="dialog" aria-labelledby="updatePapersModalTitle" aria-hidden="true">
                            <div className="modal-dialog modal-dialog-centered modal-lg" role="document">
                                <div className="modal-content">
                                    <div className="modal-header">
                                        <h5 className="modal-title" id="updatePapersModalLongTitle">Scrape Papers for Author</h5>
                                        <button type="button" className="close" data-dismiss="modal" aria-label="Close">
                                            <span aria-hidden="true">&times;</span>
                                        </button>
                                    </div>
                                    <div className="modal-body">
                                        <div className="row pl-3">
                                            <label htmlfor="myfile">Select Papers to Scrape/Add:&nbsp;</label>
                                        </div>
                                        <div className="row pl-3">
                                            <table className="table table-borderless table-striped" id="modalPaperTable">
                                                <thead className="thead-dark">
                                                    <tr>
                                                        <th className="col-8" scope="col">Article</th>
                                                        <th className="col-2" scope="col">Scrape/Add</th>
                                                    </tr>
                                                </thead>
                                                <tbody id="modalTableBody">
                                                </tbody>
                                            </table>
                                        </div>
                                    </div>
                                    <div className="modal-footer">
                                        <button type="button" className="btn btn-secondary" data-dismiss="modal">Cancel</button>
                                        <button type="button" className="btn btn-info" onClick={scrapePapersFromProfile}>Search Google Scholar</button>
                                        <button type="button" className="btn btn-success" data-dismiss="modal" onClick={createTaskFromList}>Add Selected Papers</button>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <div className="modal fade" id="deleteAuthorModal" tabIndex="-1" role="dialog" aria-labelledby="deleteAuthorModalTitle" aria-hidden="true">
                            <div className="modal-dialog modal-dialog-centered" role="document">
                                <div className="modal-content">
                                    <div className="modal-header">
                                        <h5 className="modal-title" id="deleteAuthorModalLongTitle">Delete Author?</h5>
                                        <button type="button" className="close" data-dismiss="modal" aria-label="Close">
                                            <span aria-hidden="true">&times;</span>
                                        </button>
                                    </div>
                                    <div className="modal-body">
                                        <div className="row pl-3">
                                            <h5>Are you sure you want to delete the author?</h5>
                                        </div>
                                    </div>
                                    <div className="modal-footer">
                                        <button type="button" className="btn btn-secondary" data-dismiss="modal">Cancel</button>
                                        <button id="deleteAuthor" type="button" className="btn btn-danger" data-dismiss="modal" onClick={deleteAuthor}>Delete Author</button>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <div className="row pt-3 pr-3">
                            <div className="alert alert-success alert-dismissible" role="alert" id="successScraping" style={{ display: "none" }}>
                                <button className="close" type="button" onClick={hideSuccessAlert}><span>&times;</span></button>Added selected papers.
                                <pre>
                                </pre>
                                <a href="/tasks">View in 'Tasks'</a>
                            </div>
                        </div>
                        <div className="row pt-3 pr-3">
                            <div className="alert alert-danger alert-dismissible pt-2" role="alert" id="failScraping" style={{ display: "none" }}>
                                <button className="close" type="button" onClick={hideFailAlert}><span>&times;</span></button> Error adding selected papers.
                            </div>
                        </div>

                        <div className="row pt-3 pr-3">
                            <div className="alert alert-success alert-dismissible" role="alert" id="success" style={{ display: "none" }}>
                                <button className="close" type="button" onClick={hideSuccessAlert}><span>&times;</span></button>File uploaded successfully.
                                <pre>
                                </pre>
                                <a href="/tasks">View in 'Tasks'</a>
                            </div>
                        </div>
                        <div className="row pt-3 pr-3">
                            <div className="alert alert-danger alert-dismissible pt-2" role="alert" id="fail" style={{ display: "none" }}>
                                <button className="close" type="button" onClick={hideFailAlert}><span>&times;</span></button> Error uploading file.
                            </div>
                        </div>
                    </div>
                    <div className="col-9" id="mainColumn">
                        <div className="row">
                            <h3 className="px-0" id="authorName"></h3>
                            <div className="pl-2" id="deleteAuthor">
                                <button type="button" className="btn btn-danger btn-sm" data-toggle="modal" data-target="#deleteAuthorModal">x</button>
                            </div>
                            {/* <button type="button" className="close btn-xl" aria-label="Close">
                                <span aria-hidden="true">&times;</span>
                            </button> */}
                            <div className="ml-auto" id="gslink">
                                <a href="" rel="noreferrer noopener" onClick={googleScholarRedirect}>Google Scholar profile</a>
                            </div>
                        </div>
                        <div className="row pt-2" id="articles">
                            <table className="table table-borderless table-striped mb-0" id="paperTable" style={{ display: "none" }}>
                                <thead className="thead-dark">
                                    <tr>
                                        <th className="col-8" scope="col">Article</th>
                                        <th className="col-1" scope="col">Year</th>
                                        <th className="col-1" scope="col">Citations</th>
                                        <th className="col-1" scope="col">Check</th>
                                    </tr>
                                </thead>
                                <tbody id="paperTableBody">
                                </tbody>
                            </table>
                        </div>
                        <div className="row py-4 btn-toolbar">
                            {/* <div className="ml-auto" id="deleteAuthor">
                            <button type="button" className="btn btn-danger" data-toggle="modal" data-target="#deleteAuthorModal">Delete Author</button>
                        </div> */}
                            <div className="d-flex justify-content-start">
                                <button type="button" className="btn btn-primary" onClick={htmlToCSV}>
                                    Export
                                </button>
                            </div>
                            <div className="ml-auto d-flex justify-content-end" id="deletePapers">
                                <button type="button" className="btn btn-danger" onClick={deletePapers}>Remove Checked Papers</button>
                            </div>
                        </div>
                        <div className="row py-2">
                            {/* <div className="ml-auto">
                            <button type="button" className="btn btn-primary" onClick={htmlToCSV}>
                                Export
                            </button>
                        </div> */}
                        </div>
                    </div>
                </div>
            </div>
        </div>

    );
}

export default Author;